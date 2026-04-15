# SPDX-FileCopyrightText: 2025 QinHan
# SPDX-License-Identifier: MPL-2.0

from typing import Any

from pydantic import TypeAdapter

from docutranslate.core.schemas import TranslatePayload
from docutranslate.environment import resolve_model_preset


def apply_model_preset_to_payload_data(
    payload_data: dict[str, Any],
) -> dict[str, Any]:
    if payload_data.get("skip_translate"):
        return payload_data

    model_preset = str(payload_data.get("model_preset") or "").strip()
    if not model_preset:
        return payload_data

    preset = resolve_model_preset(model_preset)
    hydrated = dict(payload_data)
    hydrated["base_url"] = preset["base_url"]
    hydrated["api_key"] = preset["api_key"]
    hydrated["model_id"] = preset["model_id"]
    hydrated["provider"] = preset.get("provider")

    if hydrated.get("rpm") in (None, "") and preset.get("rpm") is not None:
        hydrated["rpm"] = preset["rpm"]
    if hydrated.get("tpm") in (None, "") and preset.get("tpm") is not None:
        hydrated["tpm"] = preset["tpm"]

    return hydrated


def apply_model_preset_to_payload(payload: TranslatePayload) -> TranslatePayload:
    payload_data = payload.model_dump()
    hydrated_data = apply_model_preset_to_payload_data(payload_data)
    if hydrated_data == payload_data:
        return payload
    return TypeAdapter(TranslatePayload).validate_python(hydrated_data)
