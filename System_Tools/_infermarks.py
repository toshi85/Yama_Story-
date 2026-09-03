"""ナレーション行の推測マーク（**…**）を、検査の前に落とす。

2026-09-03 新設。ユーザー指示「推測の部分は、太文字にするなどできる？今後は」。
資料に無く現実的な推論で埋めた箇所は Master.md 本文で **太字** にする。
太字は人間が読むための印なので、字数・語彙・事実の検査からは見えないようにする。
"""
import re

_NARR = re.compile(r"^(ナレーター[:：].*)$", re.M)


def strip_infer(text: str) -> str:
    return _NARR.sub(lambda m: m.group(1).replace("**", ""), text)


def strip_infer_lines(lines):
    return [strip_infer(l) for l in lines]
