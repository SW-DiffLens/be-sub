# app/api/routes/search.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.fast_panel_request import FastNaturalSearch
from app.schemas.fast_panel_response import FastNaturalSearchResponse, ChartFastResult
from typing import List, Dict, Any, Optional
import asyncpg
import sys
import os

# AI 모듈 설정 import
from app.config.ai_config import DB_CONFIG_FOR_AI, check_ai_module_available

# AI 모듈 import 시도
try:
    from src.query_parser import QueryParser
    from src.search_mode import SearchMode, SearchModeTranslator
    from src.intelligent_chart_decider import IntelligentChartDecider
    from src.main_chart_decider import MainChartDecider
    from src.schemas import QueryFilter
    AI_MODULE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AI module not available: {e}")
    QueryParser = None
    SearchMode = None
    IntelligentChartDecider = None
    MainChartDecider = None
    QueryFilter = None
    AI_MODULE_AVAILABLE = False

# DB 정보 (기존)
from app.config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = APIRouter()

# AI 모듈 인스턴스 (지연 초기화)
_query_parser_instance = None
_intelligent_decider_instance = None
_rule_based_decider_instance = None


def get_query_parser():
    """QueryParser 인스턴스 가져오기 (지연 초기화)"""
    global _query_parser_instance
    if not AI_MODULE_AVAILABLE:
        return None
    
    if _query_parser_instance is None:
        try:
            # AI 모듈의 작업 디렉토리를 임시로 변경
            from app.config.ai_config import AI_MODULE_PATH
            import os
            original_cwd = os.getcwd()
            try:
                # AI 모듈 디렉토리로 변경하여 프롬프트 파일 경로 문제 해결
                os.chdir(str(AI_MODULE_PATH))
                _query_parser_instance = QueryParser()
            finally:
                os.chdir(original_cwd)
        except Exception as e:
            print(f"Warning: Failed to initialize QueryParser: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    return _query_parser_instance


def get_intelligent_decider():
    """IntelligentChartDecider 인스턴스 가져오기 (지연 초기화)"""
    global _intelligent_decider_instance
    if not AI_MODULE_AVAILABLE:
        return None
    
    if _intelligent_decider_instance is None:
        try:
            # AI 모듈의 작업 디렉토리를 임시로 변경
            from app.config.ai_config import AI_MODULE_PATH
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(str(AI_MODULE_PATH))
                _intelligent_decider_instance = IntelligentChartDecider(use_llm=True)
            finally:
                os.chdir(original_cwd)
        except Exception as e:
            print(f"Warning: Failed to initialize IntelligentChartDecider: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    return _intelligent_decider_instance


def get_rule_based_decider():
    """MainChartDecider 인스턴스 가져오기 (지연 초기화)"""
    global _rule_based_decider_instance
    if not AI_MODULE_AVAILABLE:
        return None
    
    if _rule_based_decider_instance is None:
        try:
            _rule_based_decider_instance = MainChartDecider()
        except Exception as e:
            print(f"Warning: Failed to initialize MainChartDecider: {e}")
            return None
    
    return _rule_based_decider_instance


def map_query_filter_to_db_columns(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    QueryParser 출력 필드를 실제 DB 컬럼명으로 매핑
    
    QueryFilter 필드 → DB 컬럼명:
    - region → residence
    - age_group → age_group (동일)
    - gender → gender (동일)
    - occupation → occupation (동일)
    - marital_status → marital_status (동일)
    - 기타 필드는 그대로 유지
    """
    mapped_filters = {}
    
    for key, value in filters.items():
        # 필드명 매핑
        if key == 'region':
            mapped_filters['residence'] = value
        else:
            mapped_filters[key] = value
    
    return mapped_filters


async def search_panels_from_db(
    filters: Dict[str, Any],
    limit: int = 100
) -> List[str]:
    """
    DB에서 패널 검색
    
    Returns:
        패널 ID 리스트
    """
    try:
        conn = await asyncpg.connect(**DB_CONFIG_FOR_AI)
        
        try:
            where_clauses = []
            params = []
            param_index = 1
            
            # 필터에서 DB 쿼리 조건 생성
            for key, value in filters.items():
                # 검색 모드 관련 키는 스킵 (DB 컬럼이 아닌 메타데이터 필터)
                if key in ['limit', 'mode', 'match_strategy', 'allow_null_fields',
                          'exact_match', 'minimum_match_ratio', 'sort_by', 'similarity_threshold']:
                    continue
                
                if value is None:
                    continue
                
                # 리스트 처리 (예: occupation: ["전문직", "사무직"])
                if isinstance(value, list):
                    if not value:
                        continue
                    placeholders = ','.join([f'${i}' for i in range(param_index, param_index + len(value))])
                    where_clauses.append(f"{key} = ANY(ARRAY[{placeholders}])")
                    params.extend(value)
                    param_index += len(value)
                # 단일 값 처리
                else:
                    where_clauses.append(f"{key} = ${param_index}")
                    params.append(value)
                    param_index += 1
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
            
            # 패널 ID 검색 (테이블 이름: panel, 컬럼: id)
            query_sql = f"""
                SELECT id as panel_id
                FROM panel
                WHERE {where_sql}
                LIMIT ${param_index}
            """
            params.append(limit)
            
            rows = await conn.fetch(query_sql, *params)
            panel_ids = [row['panel_id'] for row in rows]
            
            return panel_ids
            
        finally:
            await conn.close()
            
    except Exception as e:
        print(f"DB search error: {e}")
        raise HTTPException(status_code=500, detail=f"Database search failed: {str(e)}")


async def get_panel_stats(panel_ids: List[str]) -> Dict[str, Dict[str, int]]:
    """
    패널 리스트의 통계 계산
    
    Returns:
        {
            "age_group": {"20대": 10, "30대": 20, ...},
            "gender": {"남성": 15, "여성": 15, ...},
            ...
        }
    """
    if not panel_ids:
        return {}
    
    try:
        conn = await asyncpg.connect(**DB_CONFIG_FOR_AI)
        
        try:
            placeholders = ','.join([f'${i+1}' for i in range(len(panel_ids))])
            
            query_sql = f"""
                SELECT 
                    age_group, gender, residence, occupation, marital_status,
                    phone_brand, car_brand
                FROM panel
                WHERE id = ANY(ARRAY[{placeholders}])
            """
            
            rows = await conn.fetch(query_sql, *panel_ids)
            
            # 통계 계산 (DB 컬럼명 사용: residence)
            stats = {}
            metric_fields = ['age_group', 'gender', 'residence', 'occupation', 
                           'marital_status', 'phone_brand', 'car_brand']
            
            for field in metric_fields:
                stats[field] = {}
            
            for row in rows:
                for field in metric_fields:
                    value = row.get(field)
                    if value:
                        stats[field][value] = stats[field].get(value, 0) + 1
            
            # 통계에서 residence를 region으로 변환 (차트 생성용)
            if 'residence' in stats:
                stats['region'] = stats.pop('residence')
            
            # 빈 통계 제거
            stats = {k: v for k, v in stats.items() if v}
            
            return stats
            
        finally:
            await conn.close()
            
    except Exception as e:
        print(f"Stats calculation error: {e}")
        return {}


async def generate_charts(
    query: Optional[str],
    filters: Optional[Dict[str, Any]],
    stats: Dict[str, Dict[str, int]]
) -> List[ChartFastResult]:
    """
    검색 결과에 대한 차트 생성
    """
    if not stats or not AI_MODULE_AVAILABLE:
        # 폴백: 기본 차트
        return [ChartFastResult(
            chartType="bar",
            title="연령대 분포",
            reason="기본 분석 차트",
            xaxis="age_group",
            yaxis="count",
            panelColumn="age_group"
        )]
    
    charts = []
    
    try:
        # QueryFilter 생성
        query_filter = None
        if filters:
            try:
                query_filter = QueryFilter(**filters)
            except Exception:
                pass
        
        # LLM 기반 차트 결정 시도
        intelligent_decider = get_intelligent_decider()
        if query and intelligent_decider and query_filter:
            try:
                main_metric, main_title, reasoning = await intelligent_decider.decide_main_chart(
                    query, query_filter, stats
                )
                
                main_data = stats.get(main_metric, {})
                if main_data and len(main_data) > 1:  # 최소 2개 카테고리 필요
                    charts.append(ChartFastResult(
                        chartType="bar",
                        title=main_title,
                        reason=reasoning or f"'{query}' 쿼리 분석 결과",
                        xaxis=main_metric,
                        yaxis="count",
                        panelColumn=main_metric
                    ))
                    
                    # 서브 차트 추가
                    sub_charts_data = intelligent_decider._get_sub_charts_rule_based(
                        main_metric, stats, max_charts=3
                    )
                    for sub_chart in sub_charts_data[:2]:  # 최대 2개
                        sub_metric = sub_chart['metric']
                        sub_title = sub_chart['title']
                        sub_data = stats.get(sub_metric, {})
                        if sub_data and len(sub_data) > 1:
                            charts.append(ChartFastResult(
                                chartType="bar",
                                title=sub_title,
                                reason="추가 분석 지표",
                                xaxis=sub_metric,
                                yaxis="count",
                                panelColumn=sub_metric
                            ))
            except Exception as e:
                print(f"Intelligent chart decision failed: {e}")
                # Rule-based로 폴백
        
        # Rule-based 차트 결정 (LLM 실패 시 또는 LLM 사용 안 함)
        rule_based_decider = get_rule_based_decider()
        if not charts and rule_based_decider and query_filter:
            try:
                main_metric, main_title = rule_based_decider.decide_main_chart(
                    query_filter, stats
                )
                
                main_data = stats.get(main_metric, {})
                if main_data and len(main_data) > 1:
                    charts.append(ChartFastResult(
                        chartType="bar",
                        title=main_title,
                        reason="데이터 분포 분석",
                        xaxis=main_metric,
                        yaxis="count",
                        panelColumn=main_metric
                    ))
            except Exception as e:
                print(f"Rule-based chart decision failed: {e}")
        
        # 최종 폴백: 첫 번째 사용 가능한 통계로 차트 생성
        if not charts and stats:
            for metric, data in stats.items():
                if len(data) > 1:  # 최소 2개 카테고리
                    charts.append(ChartFastResult(
                        chartType="bar",
                        title=f"{metric} 분포",
                        reason="자동 생성된 차트",
                        xaxis=metric,
                        yaxis="count",
                        panelColumn=metric
                    ))
                    break
        
    except Exception as e:
        print(f"Chart generation error: {e}")
    
    # 최소한 하나는 반환
    if not charts:
        charts = [ChartFastResult(
            chartType="bar",
            title="연령대 분포",
            reason="기본 차트",
            xaxis="age_group",
            yaxis="count",
            panelColumn="age_group"
        )]
    
    return charts[:3]  # 최대 3개


@router.post("/search/natural", response_model=FastNaturalSearchResponse)
async def natural_search(request: FastNaturalSearch):
    """
    자연어 검색 - AI 모듈 통합
    
    입력: "30대 여성 서울 거주 전문직"
    출력: 패널 ID 리스트 + 차트
    """
    
    # AI 모듈 확인 및 지연 초기화
    query_parser = get_query_parser()
    if not AI_MODULE_AVAILABLE or not query_parser:
        raise HTTPException(
            status_code=503,
            detail="AI module not available. Please ensure ai submodule is properly initialized and API keys are set."
        )
    
    try:
        # 1. QueryParser로 자연어 파싱
        search_mode = SearchMode.STRICT if request.mode == "strict" else SearchMode.FLEXIBLE
        parsed_filters = query_parser.parse_to_dict(request.question, search_mode)
        
        # 디버그: 파싱된 필터 로그 출력
        print(f"[DEBUG] Parsed filters: {parsed_filters}")
        
        # 2. 필터에 count 추가 (요청에서)
        limit = 100
        if request.filters and request.filters.count:
            limit = request.filters.count
            parsed_filters['limit'] = limit
        
        # 3. QueryFilter 필드를 DB 컬럼명으로 매핑 (region → residence)
        db_filters = map_query_filter_to_db_columns(parsed_filters)
        print(f"[DEBUG] Mapped to DB columns: {db_filters}")
        
        # 4. DB에서 검색
        panel_ids = await search_panels_from_db(db_filters, limit)
        
        if not panel_ids:
            # 검색 결과 없음
            return FastNaturalSearchResponse(
                accuracy=0.0,
                panelList=[],
                accuracyList=[],
                charts=[ChartFastResult(
                    chartType="bar",
                    title="검색 결과 없음",
                    reason="조건에 맞는 패널을 찾을 수 없습니다",
                    xaxis="",
                    yaxis="count",
                    panelColumn=""
                )]
            )

        # 4. 패널 통계 계산
        stats = await get_panel_stats(panel_ids)
        
        # 5. 차트 생성
        charts = await generate_charts(request.question, parsed_filters, stats)
        
        # 6. 응답 생성
        # accuracy는 임시로 계산 (실제로는 벡터 유사도 등으로 계산 필요)
        accuracy = 0.95 if len(panel_ids) > 0 else 0.0
        accuracy_list = [accuracy - (i * 0.01) for i in range(min(len(panel_ids), 7))]
        
        return FastNaturalSearchResponse(
            accuracy=accuracy,
            panelList=panel_ids,
            accuracyList=accuracy_list,
            charts=charts
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# DB 활용 예시 (기존 유지)
@router.get("/search/test", response_model=List[Dict[str, Any]])
async def get_items(db: AsyncSession = Depends(get_db)):
    """Member 테이블의 데이터를 불러옵니다."""
    result = await db.execute(text("SELECT * FROM member"))
    return result.mappings().all()
