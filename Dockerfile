FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

COPY ./src/ .
RUN uv sync --frozen --no-cache

WORKDIR .
EXPOSE 8000

CMD ["uv", "run", "main.py"]