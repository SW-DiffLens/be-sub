# FastAPI 프로젝트 (AI 서브모듈 포함)

이 문서는 FastAPI 프로젝트에서 AI 레포를 서브모듈로 사용하는 경우의 작업, GitHub 반영, Docker 이미지 빌드 및 AWS ECR 업로드 과정을 정리합니다.

---

## 1. 서브모듈 초기화 및 최신화

프로젝트를 처음 클론하거나 서브모듈 업데이트:

```bash
# 프로젝트 클론 시
git clone <repo-url> --recurse-submodules

# 서브모듈 초기화 및 최신화
git submodule init
git submodule update
git pull --recurse-submodules
```

서브모듈 변경 사항 커밋:

```bash
git add .
git commit -m "feat: 서브모듈 업데이트"
git push origin main
```

---

## 2. FastAPI 개발 및 GitHub 반영

FastAPI 레포 작업 후:

```bash
git status
git add .
git commit -m "FastAPI 기능 추가/수정"
git push origin main
```

> 서브모듈 변경이 있는 경우, 서브모듈 커밋도 함께 반영되어야 합니다.

---

## 3. Docker 이미지 빌드 및 ECR 업로드

1. AWS ECR 로그인:

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <your-ecr-uri>
```

2. Docker 이미지 빌드:

```bash
docker buildx build --platform linux/amd64 -t difflens-fastapi .
```

3. Docker 이미지 태그:

```bash
docker tag difflens-fastapi:latest <your-ecr-uri>:latest
```

4. ECR에 이미지 푸시:

```bash
docker push <your-ecr-uri>:latest
```

---

## 4. 패키지 구조 예시

```
fastapi-project/
├─ main.py
├─ requirements.txt
├─ app/
│  ├─ api/
│  └─ ...
└─ ai/  # 서브모듈
   ├─ requirements.txt
   ├─ src/
   │  ├─ client.py
   │  ├─ profile_generator.py
   │  └─ ...
   └─ scripts/
      └─ test_prompts.py
```

---

## 5. Dockerfile 참고 사항

* FastAPI와 AI 서브모듈 각각의 `requirements.txt`를 설치해야 합니다.
* AI 서브모듈을 Docker 이미지에 포함시키고, PYTHONPATH를 설정하여 import 가능하도록 합니다.

예시 Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -r ./ai/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app/ai"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---


## 6. 주의 사항

* FastAPI 레포와 AI 서브모듈은 동일한 Python 버전을 사용해야 합니다.
* 이미지 빌드 시 반드시 AI 서브모듈 의존성이 설치되도록 해야 합니다.
* GitHub 반영 시 서브모듈 커밋 상태를 꼭 확인하세요.
