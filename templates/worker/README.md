# worker-template

API 없이 백그라운드 작업만 수행하는 워커 서비스입니다.

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
uv run python -m app.worker
```

## 품질 체크
```bash
uv run ruff check .
uv run mypy app
uv run pytest
```
