# SPDX-FileCopyrightText: 2025 QinHan
# SPDX-License-Identifier: MPL-2.0
"""
集中管理所有环境变量。
所有 os.getenv() 调用应在此处统一声明，其他模块从这里导入。
"""
import os

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
