#!/usr/bin/env python3
"""Install or download dependencies for all language implementations."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"


def run(cmd: list[str], cwd: Path) -> None:
    print(f"[bootstrap] {' '.join(cmd)} (cwd={cwd})")
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_venv() -> Path:
    """Create a virtualenv under ROOT/.venv if it does not exist."""
    python_in_venv = VENV / "bin" / "python"
    if not python_in_venv.exists():
        print("[bootstrap] Creating virtual environment:", VENV)
        run([sys.executable, "-m", "venv", str(VENV)], ROOT)

    return python_in_venv


def main() -> int:
    # 1) 确保虚拟环境存在
    venv_python = ensure_venv()

    # 2) 用虚拟环境安装 Python 依赖
    run([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], ROOT / "python")

    # 3) Node.js
    run(["npm", "install"], ROOT / "nodejs")

    # 4) Go
    run(["go", "mod", "download"], ROOT / "go")

    # 5) Rust
    run(["cargo", "fetch"], ROOT / "rust")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
