import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
NODE_SCRIPT = BASE_DIR / "render_app.js"
PYTHON_SCRIPT = BASE_DIR / "render_pptx.py"

if sys.platform == "win32":
    VITE_CMD = BASE_DIR / "node_modules" / ".bin" / "vite.cmd"
else:
    VITE_CMD = BASE_DIR / "node_modules" / ".bin" / "vite"


def run_command(command, capture_output=False, env=None):
    print("Running:", " ".join(str(item) for item in command))
    completed = subprocess.run([str(item) for item in command], cwd=BASE_DIR, capture_output=capture_output, text=True, env=env)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
        raise SystemExit(completed.returncode)
    return completed


if __name__ == "__main__":
    run_command([VITE_CMD, "build"])
    node_result = run_command(["node", str(NODE_SCRIPT)], capture_output=True)
    screenshot_dir = None
    for line in node_result.stdout.splitlines():
        if line.startswith("SCREENSHOT_DIR="):
            screenshot_dir = line.split("=", 1)[1].strip()
            break
    if not screenshot_dir:
        raise SystemExit("Could not read SCREENSHOT_DIR from renderer output")

    child_env = os.environ.copy()
    child_env["SCREENSHOT_DIR"] = screenshot_dir
    run_command([sys.executable, str(PYTHON_SCRIPT)], env=child_env)
