"""YAML config parser for drt project and sync definitions."""

from pathlib import Path

import yaml

from drt.config.models import ProjectConfig, SyncConfig


def load_project(project_dir: Path = Path(".")) -> ProjectConfig:
    """Load and validate drt_project.yml."""
    config_path = project_dir / "drt_project.yml"
    if not config_path.exists():
        raise FileNotFoundError(
            f"drt_project.yml not found in {project_dir}. Run `drt init` first."
        )
    with config_path.open() as f:
        data = yaml.safe_load(f)
    return ProjectConfig.model_validate(data)


def load_syncs(project_dir: Path = Path(".")) -> list[SyncConfig]:
    """Load and validate all sync YAML files from syncs/."""
    syncs_dir = project_dir / "syncs"
    if not syncs_dir.exists():
        return []
    syncs = []
    for path in sorted(syncs_dir.glob("*.yml")):
        with path.open() as f:
            data = yaml.safe_load(f)
        syncs.append(SyncConfig.model_validate(data))
    return syncs
