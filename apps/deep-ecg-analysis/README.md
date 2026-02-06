# deep-ecg-analysis API

FastAPI + PostgreSQL + Redis + Sentry 기본 구성입니다.
UI 템플릿은 사용하지 않으며 API 전용 서비스입니다.

## 환경 변수
`.env.example`을 복사해 사용합니다.

```bash
cp .env.example .env
```

주요 항목:
- `APP_NAME`: 서비스 표시 이름
- `APP_ENV`: 환경 값 (예: `local`, `dev`, `prod`)
- `DATABASE_URL`: PostgreSQL 접속 문자열
- `REDIS_URL`: Redis 접속 문자열
- `SENTRY_DSN`: Sentry DSN (비워두면 비활성)
- `SENTRY_TRACES_SAMPLE_RATE`: 트레이싱 샘플링 비율
- `ENABLE_HEALTH_CHECKS`: `/health/ready`에서 DB/Redis 체크 여부

## 개발 환경
```bash
uv venv
uv sync --extra dev
```

## 로컬 의존 서비스
```bash
docker compose up -d
```

## 실행
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 마이그레이션 (Alembic)
DB가 실행 중이어야 합니다.

```bash
alembic revision -m \"init\" --autogenerate
alembic upgrade head
```

## 품질 체크
```bash
uv run ruff check .
uv run mypy app
uv run pytest
```

## 헬스체크
- `GET /health/live`
- `GET /health/ready` (DB/Redis 연결 확인)

DB/Redis 없이 테스트하려면 `ENABLE_HEALTH_CHECKS=false`로 설정하세요.
