from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ecowave.config import Settings, is_placeholder
from ecowave.db import get_schema_version, log_validation


@dataclass
class CheckItem:
    label: str
    ok: bool
    message: str


@dataclass
class CheckResult:
    mode: str
    items: list[CheckItem] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(item.ok for item in self.items)

    def to_text(self) -> str:
        lines = [f"EcoWave config check — mode={self.mode}"]
        for item in self.items:
            status = "OK" if item.ok else "FAIL"
            lines.append(f"{item.label:<24} {status:<5} {item.message}")
        lines.append(f"RESULT {'OK' if self.ok else 'FAILED'}")
        return "\n".join(lines)


def _dir_check(path: Path) -> CheckItem:
    try:
        path.mkdir(parents=True, exist_ok=True)
        return CheckItem(str(path), True, "directory exists or was created")
    except Exception as exc:
        return CheckItem(str(path), False, f"cannot create directory: {exc}")


def check_config(settings: Settings, mode: str) -> CheckResult:
    if mode not in {"strict", "exploratory"}:
        raise ValueError("mode must be strict or exploratory")

    items: list[CheckItem] = []

    fred_ok = not is_placeholder(settings.fred_api_key)
    if mode == "strict":
        items.append(CheckItem("FRED_API_KEY", fred_ok, "required in strict mode"))
    else:
        items.append(CheckItem("FRED_API_KEY", True, "placeholder allowed in exploratory; strict will fail" if not fred_ok else "configured"))

    ecb_ok = not is_placeholder(settings.ecb_api_base)
    items.append(CheckItem("ECB_API_BASE", ecb_ok, "required endpoint"))

    for path in [
        settings.db_path.parent,
        settings.data_raw_dir,
        settings.data_processed_dir,
        settings.events_dir,
        settings.reports_dir,
        settings.figures_dir,
    ]:
        items.append(_dir_check(path))

    schema_version = get_schema_version(settings.db_path)
    # 0.2.0 is upgraded in place by db.migrate_db() at pipeline start; both
    # versions are acceptable so existing databases keep working without
    # forcing a re-init.
    accepted_versions = {"0.5.0"}
    db_ok = schema_version in accepted_versions
    if mode == "strict":
        items.append(CheckItem("SQLite schema", db_ok,
                               f"expected one of {sorted(accepted_versions)}, found {schema_version}"))
    else:
        items.append(CheckItem("SQLite schema",
                               True if schema_version in (accepted_versions | {None}) else False,
                               f"found {schema_version}; run init-db if missing"))

    result = CheckResult(mode=mode, items=items)

    if settings.db_path.exists():
        for item in items:
            if not item.ok:
                log_validation(
                    settings.db_path,
                    severity="error" if mode == "strict" else "warning",
                    component="check-config",
                    message=f"{item.label}: {item.message}",
                    mode_effect="strict_fails_exploratory_warns",
                )

    return result
