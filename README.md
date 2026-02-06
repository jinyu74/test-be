# project-be

Back-End 프로젝트를 관리하는 Boilerplate 구성된 Monorepo 입니다. `apps/` 하위에 서비스별로 프로젝트를 추가하는 구조입니다.
이 저장소는 **API/Worker 서비스만** 다루며, 서버 사이드 UI 템플릿(Jinja2 등)은 사용하지 않습니다.

## 구조

- `apps/api`: FastAPI 기반 API 서비스
- `apps/*`: 추가 서비스(예: worker, scheduler 등)를 같은 패턴으로 확장

## 패키지 관리

- Python 패키지는 `uv`로 관리합니다.
- `uv`가 없으면 설치 후 진행하세요.

## 기본 의존성 목록

API 서비스:
- `fastapi`
- `uvicorn[standard]`
- `sqlalchemy`
- `asyncpg`
- `redis`
- `sentry-sdk`
- `alembic`

Worker 서비스:
- `sqlalchemy`
- `asyncpg`
- `redis`
- `sentry-sdk`

공통 개발 도구:
- `ruff`
- `mypy`
- `pytest`

API 테스트 도구:
- `httpx`

## 서비스 생성 가이드 (CLI)

UI가 없는 API/Worker 서비스이므로 서버 사이드 템플릿(Jinja2)은 설정하지 않습니다.  
아래 CLI가 서비스 폴더를 생성하고 필수 값(`APP_NAME`, `DATABASE_URL`, `pyproject` 이름 등)을 자동으로 치환합니다.

API 서비스 생성:

```bash
scripts/create-app deep-ecg-analysis
```

Worker 서비스 생성:

```bash
scripts/create-worker deep-ecg-analysis-worker
```

CLI는 기본적으로 `uv venv`와 `uv sync --extra dev`를 실행합니다.  
설치를 건너뛰려면 `--skip-install` 옵션을 사용하세요.

```bash
scripts/create-app deep-ecg-analysis --skip-install
```

서비스 삭제:

```bash
scripts/remove-service deep-ecg-analysis
```

삭제 확인을 건너뛰려면 `--force`를 사용합니다.

```bash
scripts/remove-service deep-ecg-analysis --force
```

생성 후 최소 확인 항목:

- `apps/<service>/pyproject.toml`의 `name`
- `apps/<service>/.env.example`의 `APP_NAME`/`DATABASE_URL`
- `apps/<service>/README.md` 서비스명/설명

## 새 프로젝트 생성 후 실행 순서

API 서비스 예시:

1. 서비스 생성

```bash
scripts/create-app deep-ecg-analysis
```

2. 개발 환경 설정 (uv)

```bash
cd apps/deep-ecg-analysis
uv venv
uv sync --extra dev
```

3. 로컬 의존 서비스 실행

```bash
docker compose up -d
```

4. 환경 변수 설정

```bash
cp .env.example .env
```

5. 실행

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Worker 서비스 예시:

1. 서비스 생성

```bash
scripts/create-worker deep-ecg-analysis-worker
```

2. 개발 환경 설정 (uv)

```bash
cd apps/deep-ecg-analysis-worker
uv venv
uv sync --extra dev
```

3. 로컬 의존 서비스 실행

```bash
docker compose up -d
```

4. 환경 변수 설정

```bash
cp .env.example .env
```

5. 실행

```bash
uv run python -m app.worker
```

## 기존 프로젝트 실행 순서

API 서비스:

1. 가상환경/의존성 동기화 (uv)

```bash
cd apps/<service>
uv venv
uv sync --extra dev
```

2. 로컬 의존 서비스 실행

```bash
docker compose up -d
```

3. 환경 변수 설정

```bash
cp .env.example .env
```

4. 실행

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Worker 서비스:

1. 가상환경/의존성 동기화 (uv)

```bash
cd apps/<service>
uv venv
uv sync --extra dev
```

2. 로컬 의존 서비스 실행

```bash
docker compose up -d
```

3. 환경 변수 설정

```bash
cp .env.example .env
```

4. 실행

```bash
uv run python -m app.worker
```

## 품질 체크 (CI 로컬 실행)

```bash
scripts/ci.sh
```

## 워커 선택 가이드 (Celery vs ARQ)

ECG 분석처럼 CPU/GPU 연산이 큰 경우에는 기본적으로 **Celery**를 추천합니다.  
간단한 async 파이프라인과 최소 인프라를 원하면 **ARQ**를 고려하세요.

선택 기준:

- Celery: 멀티 프로세스 기반 병렬 처리에 유리, 브로커/백엔드 옵션 다양
- ARQ: Redis + asyncio 기반, 구성 단순
- ARQ 사용 시 CPU 작업은 `run_in_executor` 등으로 분리 권장

## 추천 (확장 포인트)

- Observability: OpenTelemetry + Prometheus/Grafana
- Background Jobs: Celery 또는 ARQ (Redis 연동)
