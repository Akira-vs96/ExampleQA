"""10. Python breakpoint() функциясын қауіпсіз демонстрациялау."""

import os


def calculate(a: int, b: int) -> int:
    result = a + b
    if os.getenv("USE_PDB") == "1":
        breakpoint()  # USE_PDB=1 болғанда pdb осы жерде ашылады.
    return result


def main() -> None:
    print("10-сұрақ: breakpoint()")
    print("Қалыпты іске қосу:", calculate(4, 5))
    print("pdb режимі: USE_PDB=1 python topic_10_python_breakpoint.py")


if __name__ == "__main__":
    main()
