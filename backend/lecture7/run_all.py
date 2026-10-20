"""7-дәрістің кодпен көрсетуге болатын демонстрацияларын іске қосу."""

from pathlib import Path
import subprocess
import sys


EXAMPLES_DIRECTORY = Path(__file__).parent / "examples"


def main() -> int:
    scripts = sorted(EXAMPLES_DIRECTORY.glob("topic_*.py"))
    print(f"7-дәріс: кодпен көрсетілетін {len(scripts)} демонстрация\n", flush=True)

    for script in scripts:
        print(f"{'=' * 72}\n{script.name}\n{'=' * 72}", flush=True)
        completed = subprocess.run([sys.executable, str(script)], check=False)
        if completed.returncode != 0:
            print(f"ҚАТЕ: {script.name}, exit code={completed.returncode}")
            return completed.returncode
        print()

    print(f"Барлық {len(scripts)} демонстрация сәтті орындалды.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
