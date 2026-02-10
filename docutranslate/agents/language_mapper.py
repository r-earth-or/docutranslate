# SPDX-FileCopyrightText: 2025 QinHan
# SPDX-License-Identifier: MPL-2.0

"""
qwen-mt模型的语言代码映射
根据官方文档：https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29615833.J_go7Hzi7p17rPSpUsoA-Iv.1.10ad6e39gqvMKt&tab=doc#/doc/?type=model&url=2860790
"""

# qwen-mt支持的语言代码映射表
# 键：常见的中文/英文语言名称（不区分大小写）
# 值：qwen-mt API要求的语言代码
QWEN_MT_LANGUAGE_MAP = {
    # 英语
    "英语": "en",
    "english": "en",
    "en": "en",
    
    # 简体中文
    "中文": "zh",
    "简体中文": "zh",
    "chinese": "zh",
    "zh": "zh",
    "zh-cn": "zh",
    "zh_cn": "zh",
    
    # 繁体中文
    "繁体中文": "zh_tw",
    "traditional chinese": "zh_tw",
    "zh-tw": "zh_tw",
    "zh_tw": "zh_tw",
    
    # 其他语言
    "俄语": "ru",
    "russian": "ru",
    "ru": "ru",
    
    "日语": "ja",
    "japanese": "ja",
    "ja": "ja",
    
    "韩语": "ko",
    "korean": "ko",
    "ko": "ko",
    
    "西班牙语": "es",
    "spanish": "es",
    "es": "es",
    
    "法语": "fr",
    "french": "fr",
    "fr": "fr",
    
    "葡萄牙语": "pt",
    "portuguese": "pt",
    "pt": "pt",
    
    "德语": "de",
    "german": "de",
    "de": "de",
    
    "意大利语": "it",
    "italian": "it",
    "it": "it",
    
    "泰语": "th",
    "thai": "th",
    "th": "th",
    
    "越南语": "vi",
    "vietnamese": "vi",
    "vi": "vi",
    
    "印度尼西亚语": "id",
    "indonesian": "id",
    "id": "id",
    
    "马来语": "ms",
    "malay": "ms",
    "ms": "ms",
    
    "阿拉伯语": "ar",
    "arabic": "ar",
    "ar": "ar",
    
    "印地语": "hi",
    "hindi": "hi",
    "hi": "hi",
    
    "希伯来语": "he",
    "hebrew": "he",
    "he": "he",
    
    "缅甸语": "my",
    "burmese": "my",
    "my": "my",
    
    "泰米尔语": "ta",
    "tamil": "ta",
    "ta": "ta",
    
    "乌尔都语": "ur",
    "urdu": "ur",
    "ur": "ur",
    
    "孟加拉语": "bn",
    "bengali": "bn",
    "bn": "bn",
    
    "波兰语": "pl",
    "polish": "pl",
    "pl": "pl",
    
    "荷兰语": "nl",
    "dutch": "nl",
    "nl": "nl",
    
    "罗马尼亚语": "ro",
    "romanian": "ro",
    "ro": "ro",
    
    "土耳其语": "tr",
    "turkish": "tr",
    "tr": "tr",
    
    "高棉语": "km",
    "khmer": "km",
    "km": "km",
    
    "老挝语": "lo",
    "lao": "lo",
    "lo": "lo",
    
    "粤语": "yue",
    "cantonese": "yue",
    "yue": "yue",
    
    # 更多欧洲语言
    "捷克语": "cs",
    "czech": "cs",
    "cs": "cs",
    
    "希腊语": "el",
    "greek": "el",
    "el": "el",
    
    "瑞典语": "sv",
    "swedish": "sv",
    "sv": "sv",
    
    "匈牙利语": "hu",
    "hungarian": "hu",
    "hu": "hu",
    
    "丹麦语": "da",
    "danish": "da",
    "da": "da",
    
    "芬兰语": "fi",
    "finnish": "fi",
    "fi": "fi",
    
    "乌克兰语": "uk",
    "ukrainian": "uk",
    "uk": "uk",
    
    "保加利亚语": "bg",
    "bulgarian": "bg",
    "bg": "bg",
    
    "塞尔维亚语": "sr",
    "serbian": "sr",
    "sr": "sr",
}


def normalize_language_code(language: str, for_qwen_mt: bool = False) -> str:
    """
    将语言名称或代码标准化为适当的格式
    
    Args:
        language: 输入的语言名称或代码
        for_qwen_mt: 是否为qwen-mt模型转换（需要特定的代码格式）
    
    Returns:
        标准化后的语言代码
    """
    if not language:
        return ""
    
    # 如果是qwen-mt模型，需要转换为标准代码
    if for_qwen_mt:
        # 首先尝试直接匹配
        normalized = language.strip().lower()
        if normalized in QWEN_MT_LANGUAGE_MAP:
            return QWEN_MT_LANGUAGE_MAP[normalized]
        
        # 如果映射表中没有，原样返回（可能已经是正确的代码）
        return language.strip()
    
    # 对于非qwen-mt模型，原样返回
    return language
