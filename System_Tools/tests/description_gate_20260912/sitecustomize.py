import builtins, os
_original_open = builtins.open
_target = "/Users/tosimasa/Desktop/Antigravity/Yama_Story/yama_safety_validation.log"
def _open(file, mode="r", *args, **kwargs):
    if isinstance(file, (str, bytes, os.PathLike)) and os.fsdecode(file) == _target and any(c in mode for c in "wax+"):
        file = os.path.join(os.path.dirname(__file__), "safety_validation.log")
    return _original_open(file, mode, *args, **kwargs)
builtins.open = _open
