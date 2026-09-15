import re
import unicodedata


_PUNCT = re.compile(r"[^\w\u3400-\u9fff]+", re.UNICODE)


def normalize_zh(text):
    text = unicodedata.normalize("NFKC", text).lower()
    return _PUNCT.sub("", text)


def normalize_zh_t2s(text):
    try:
        from opencc import OpenCC
    except ImportError as exc:
        raise RuntimeError("zh_t2s requires `pip install opencc-python-reimplemented`") from exc
    return normalize_zh(OpenCC("t2s").convert(text))


NORMALIZERS = {"none": lambda text: text, "zh": normalize_zh, "zh_t2s": normalize_zh_t2s}
