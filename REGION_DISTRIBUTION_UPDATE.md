# 코호트 비교 API - 지역 분포 필드 추가 안내

## 📢 변경 사항

코호트 비교 API 응답에 **지역 분포 (`region_distribution`)** 필드가 추가되었습니다.

---

## 📋 추가된 필드

### 응답 구조

```typescript
interface ComparisonResponse {
  // ... 기존 필드들 ...

  // ⭐ 새로 추가된 필드
  region_distribution: RegionDistribution | null; // nullable
}

interface RegionDistribution {
  cohort_1: Record<string, number>; // 그룹 A의 지역별 비율 (%)
  cohort_2: Record<string, number>; // 그룹 B의 지역별 비율 (%)
}
```

---

## 📊 응답 예시

```json
{
  "cohort_1": { ... },
  "cohort_2": { ... },
  "comparisons": [ ... ],
  "basic_info": [ ... ],
  "characteristics": [ ... ],

  "region_distribution": {
    "cohort_1": {
      "서울": 35.0,
      "경기": 40.0,
      "부산": 15.0,
      "기타": 10.0
    },
    "cohort_2": {
      "서울": 35.0,
      "경기": 40.0,
      "부산": 15.0,
      "기타": 10.0
    }
  },

  "key_insights": { ... },
  "summary": { ... }
}
```

---

## ⚠️ 중요 사항

### 1. Nullable 필드

- `region_distribution`은 **nullable**입니다.
- 지역 데이터가 없거나 계산 실패 시 `null` 반환
- 클라이언트에서 null 체크 필수

### 2. 지역명 형식

- **시도 단위**로 집계됩니다 (서울, 경기, 부산)
- 주요 시도에 해당하지 않는 지역은 **"기타"**로 통합
- 비율은 **소수점 2자리** (예: 35.0, 40.0)

### 3. 데이터 소스

- `panel.region` 또는 `panel.residence` 필드 사용
- 둘 다 있으면 `region` 우선, 없으면 `residence` 사용
- "서울 강남구" → "서울"로 추출하여 집계

---

## 🔧 DTO 수정 가이드

### Java/Kotlin 예시

```kotlin
data class ComparisonResponse(
    // ... 기존 필드들 ...
    val regionDistribution: RegionDistribution?  // nullable 추가
)

data class RegionDistribution(
    val cohort1: Map<String, Double>,  // 지역명 → 비율 (%)
    val cohort2: Map<String, Double>
)
```

### TypeScript 예시

```typescript
interface ComparisonResponse {
  // ... 기존 필드들 ...
  region_distribution: RegionDistribution | null;
}

interface RegionDistribution {
  cohort_1: Record<string, number>;
  cohort_2: Record<string, number>;
}
```

---

## 📝 변경 일자

- **추가 일자**: 2025-11-19
- **API 버전**: 기존 버전 유지 (하위 호환)

---

## ✅ 체크리스트

- [ ] DTO에 `region_distribution` 필드 추가
- [ ] Nullable 처리 확인
- [ ] 클라이언트 UI에 지역 분포 표시 로직 추가
- [ ] 테스트 케이스 추가

---

## 문의

추가된 필드에 대한 문의사항이 있으시면 서브 서버 개발팀에 연락 부탁드립니다.
