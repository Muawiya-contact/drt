"""Pydantic models for drt project and sync configuration."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    type: Literal["bigquery", "snowflake", "postgres", "duckdb"]
    project: str | None = None
    dataset: str | None = None
    credentials: str | None = None


class ProjectConfig(BaseModel):
    name: str
    version: str = "0.1"
    source: SourceConfig


class RateLimitConfig(BaseModel):
    requests_per_second: int = 10


class DestinationConfig(BaseModel):
    type: Literal["rest_api"]
    url: str
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "POST"
    headers: dict[str, str] = Field(default_factory=dict)
    body_template: str | None = None
    auth: dict[str, Any] | None = None


class SyncConfig(BaseModel):
    name: str
    description: str = ""
    model: str
    destination: DestinationConfig
    sync: "SyncOptions" = Field(default_factory=lambda: SyncOptions())


class SyncOptions(BaseModel):
    mode: Literal["full", "incremental"] = "full"
    batch_size: int = 100
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    on_error: Literal["skip", "fail"] = "fail"
