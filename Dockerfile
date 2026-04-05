FROM python:3.12-slim AS base

LABEL maintainer="drt-hub" \
      description="Reverse ETL for the code-first data stack"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG DRT_EXTRAS=""

RUN if [ -z "$DRT_EXTRAS" ]; then \
      pip install --no-cache-dir drt-core; \
    else \
      pip install --no-cache-dir "drt-core[$DRT_EXTRAS]"; \
    fi

ENTRYPOINT ["drt"]
CMD ["--help"]
