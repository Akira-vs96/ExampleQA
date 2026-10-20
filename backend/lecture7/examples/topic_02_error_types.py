"""2. SyntaxError, Runtime Error және Logical Error айырмашылығы."""


def main() -> None:
    print("2-сұрақ: Қате түрлері")

    try:
        compile("if True print('hello')", "syntax_demo.py", "exec")
    except SyntaxError as error:
        print("SyntaxError: код синтаксисі дұрыс емес ->", error.msg)

    try:
        _ = 10 / 0
    except ZeroDivisionError as error:
        print("Runtime Error: код орындалу кезінде тоқтады ->", error)

    expected = 800
    actual = 1000 - 1000 * 20
    print(f"Logical Error: бағдарлама тоқтамады, бірақ {actual=} және {expected=}")


if __name__ == "__main__":
    main()
