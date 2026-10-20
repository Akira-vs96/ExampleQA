"""14. Debugging кезінде құпия деректерді логқа шығармау."""


def mask_secret(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"


def main() -> None:
    token = "qa-secret-token-2026"
    email = "student@example.kz"
    print("14-сұрақ: Debugging қауіпсіздігі")
    print("ҚАУІПТІ тәсіл көрсетілмейді: token-ді толық логтауға болмайды")
    print(f"Қауіпсіз лог: email={email}, token={mask_secret(token)}")


if __name__ == "__main__":
    main()
