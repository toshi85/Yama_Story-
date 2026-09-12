from pathlib import Path
import importlib.util
root=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location("original_five_pass_gate",root/".codex/skills/yama-five-pass/scripts/gate.py")
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
# Only relocate records to the user-authorized raw-output directory.
# All original validation functions, thresholds, hashes and ordering are unchanged.
gate.location=lambda script: script.parent/"check"/"five_pass"/script.stem
raise SystemExit(gate.main())
