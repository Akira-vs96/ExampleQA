"""Educational vulnerable functions, used only in local, explicit demonstrations."""


def login(connection, username, password):
    # BUG: user input is concatenated into the SQL statement.
    return connection.execute(
        f"SELECT username FROM users WHERE username='{username}' AND password='{password}'"
    ).fetchone()


def search_html(query):
    # BUG: untrusted text is inserted directly into HTML.
    return f"<p>Search: {query}</p>"
