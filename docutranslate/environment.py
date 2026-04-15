# SPDX-FileCopyrightText: 2025 QinHan
# SPDX-License-Identifier: MPL-2.0
"""
集中管理所有环境变量。
所有 os.getenv() 调用应在此处统一声明，其他模块从这里导入。
"""
import json
import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv

load_dotenv()  # 自动从项目根目录的 .env 文件加载环境变量（不覆盖已有的 shell 变量）


# --- 代理配置 ---
# 是否启用系统代理，设置为 "true" 开启
DOCUTRANSLATE_PROXY_ENABLED: bool = (
    os.getenv("DOCUTRANSLATE_PROXY_ENABLED", "").lower() == "true"
)

# --- 缓存配置 ---
# 任务缓存数量
DOCUTRANSLATE_CACHE_NUM: int = int(os.getenv("DOCUTRANSLATE_CACHE_NUM", "10"))

# --- 翻译 API 默认配置 ---
# 默认 API 地址 (自定义接口的 Base URL)
DOCUTRANSLATE_BASE_URL: str = os.getenv("DOCUTRANSLATE_BASE_URL", "")

# 默认 API 密钥
DOCUTRANSLATE_API_KEY: str = os.getenv("DOCUTRANSLATE_API_KEY", "")

# 默认模型 ID
DOCUTRANSLATE_MODEL_ID: str = os.getenv("DOCUTRANSLATE_MODEL_ID", "")

# --- 限流默认配置 ---
# 默认 RPM 限制 (Requests Per Minute)，不设置则不限制
_rpm_str = os.getenv("DOCUTRANSLATE_RPM", "")
DOCUTRANSLATE_RPM: int | None = int(_rpm_str) if _rpm_str.strip() else None

# 默认 TPM 限制 (Tokens Per Minute)，不设置则不限制
_tpm_str = os.getenv("DOCUTRANSLATE_TPM", "")
DOCUTRANSLATE_TPM: int | None = int(_tpm_str) if _tpm_str.strip() else None

# 模型预设配置（JSON 字符串）
DOCUTRANSLATE_MODEL_PRESETS: str = os.getenv("DOCUTRANSLATE_MODEL_PRESETS", "").strip()

# 前端默认选中的模型预设 ID
DOCUTRANSLATE_DEFAULT_MODEL_PRESET: str = os.getenv(
    "DOCUTRANSLATE_DEFAULT_MODEL_PRESET", ""
).strip()

# 兼容旧版单模型配置时的展示名称
DOCUTRANSLATE_DEFAULT_MODEL_PRESET_LABEL: str = os.getenv(
    "DOCUTRANSLATE_DEFAULT_MODEL_PRESET_LABEL", "环境默认模型"
).strip()


def _parse_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    return int(text) if text else None


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_model_preset(preset_id: str, raw: dict[str, Any]) -> dict[str, Any]:
    base_url = _clean_text(raw.get("base_url", ""))
    model_id = _clean_text(raw.get("model_id", ""))
    if not base_url or not model_id:
        raise ValueError(
            f"模型预设 '{preset_id}' 缺少必要字段 `base_url` 或 `model_id`。"
        )

    api_key_env = _clean_text(raw.get("api_key_env", ""))
    api_key = os.getenv(api_key_env, "").strip() if api_key_env else _clean_text(
        raw.get("api_key", "")
    )
    if not api_key:
        api_key = DOCUTRANSLATE_API_KEY.strip()

    provider = _clean_text(raw.get("provider", "")) or None
    description = _clean_text(raw.get("description", "")) or None

    return {
        "id": preset_id,
        "label": _clean_text(raw.get("label") or raw.get("name") or preset_id),
        "description": description,
        "base_url": base_url,
        "api_key": api_key or "xx",
        "model_id": model_id,
        "provider": provider,
        "rpm": _parse_optional_int(raw.get("rpm", DOCUTRANSLATE_RPM)),
        "tpm": _parse_optional_int(raw.get("tpm", DOCUTRANSLATE_TPM)),
    }


@lru_cache(maxsize=1)
def get_model_presets() -> dict[str, dict[str, Any]]:
    presets: dict[str, dict[str, Any]] = {}

    if DOCUTRANSLATE_MODEL_PRESETS:
        parsed = json.loads(DOCUTRANSLATE_MODEL_PRESETS)
        if isinstance(parsed, list):
            for item in parsed:
                if not isinstance(item, dict):
                    raise ValueError("DOCUTRANSLATE_MODEL_PRESETS 列表项必须是对象。")
                preset_id = str(item.get("id") or item.get("name") or "").strip()
                if not preset_id:
                    raise ValueError(
                        "DOCUTRANSLATE_MODEL_PRESETS 的列表项必须包含 `id` 或 `name`。"
                    )
                presets[preset_id] = _normalize_model_preset(preset_id, item)
        elif isinstance(parsed, dict):
            for preset_id, item in parsed.items():
                if not isinstance(item, dict):
                    raise ValueError("DOCUTRANSLATE_MODEL_PRESETS 对象成员必须是对象。")
                normalized_id = str(preset_id).strip()
                if not normalized_id:
                    raise ValueError(
                        "DOCUTRANSLATE_MODEL_PRESETS 的对象键不能是空字符串。"
                    )
                presets[normalized_id] = _normalize_model_preset(normalized_id, item)
        else:
            raise ValueError(
                "DOCUTRANSLATE_MODEL_PRESETS 必须是 JSON 对象或 JSON 数组。"
            )

    if not presets and DOCUTRANSLATE_BASE_URL.strip() and DOCUTRANSLATE_MODEL_ID.strip():
        presets["default"] = {
            "id": "default",
            "label": DOCUTRANSLATE_DEFAULT_MODEL_PRESET_LABEL,
            "description": None,
            "base_url": DOCUTRANSLATE_BASE_URL.strip(),
            "api_key": DOCUTRANSLATE_API_KEY.strip() or "xx",
            "model_id": DOCUTRANSLATE_MODEL_ID.strip(),
            "provider": None,
            "rpm": DOCUTRANSLATE_RPM,
            "tpm": DOCUTRANSLATE_TPM,
        }

    return presets


def get_default_model_preset() -> str | None:
    presets = get_model_presets()
    if not presets:
        return None
    if DOCUTRANSLATE_DEFAULT_MODEL_PRESET:
        if DOCUTRANSLATE_DEFAULT_MODEL_PRESET not in presets:
            raise ValueError(
                "DOCUTRANSLATE_DEFAULT_MODEL_PRESET 指向了不存在的模型预设。"
            )
        return DOCUTRANSLATE_DEFAULT_MODEL_PRESET
    return next(iter(presets))


def get_public_model_presets() -> list[dict[str, str]]:
    public_presets: list[dict[str, str]] = []
    for preset_id, preset in get_model_presets().items():
        item = {"id": preset_id, "label": preset["label"]}
        if preset.get("description"):
            item["description"] = preset["description"]
        public_presets.append(item)
    return public_presets


def resolve_model_preset(preset_id: str) -> dict[str, Any]:
    preset_key = str(preset_id or "").strip()
    if not preset_key:
        raise ValueError("模型预设不能为空。")

    presets = get_model_presets()
    if preset_key not in presets:
        raise ValueError(f"未找到模型预设 '{preset_key}'。")

    return dict(presets[preset_key])
