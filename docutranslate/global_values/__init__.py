# SPDX-FileCopyrightText: 2025 QinHan
# SPDX-License-Identifier: MPL-2.0
from docutranslate.environment import DOCUTRANSLATE_PROXY_ENABLED

from .conditional_import import available_packages, conditional_import

USE_PROXY = DOCUTRANSLATE_PROXY_ENABLED
if USE_PROXY:
    print(f"USE_PROXY:{USE_PROXY}")
