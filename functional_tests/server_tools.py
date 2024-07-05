from fabric import Connection

server = ""
conn = Connection(host=server)


def _get_manage_dot_py(host):
    return f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py"


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with conn.settings(host_string=f"elspeth@{host}"):
        conn.run(f"{manage_dot_py} flush --noinput")


def _get_server_env_vars(host):
    env_lines = conn.run(f"cat ~/sites/{host}/.env").splitlines()
    return dict(l.split("=") for l in env_lines if l)


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with conn.settings(host_string=f"elspeth@{host}"):
        env_vars = _get_server_env_vars(host)
        with conn.shell_env(**env_vars):
            session_key = conn.run(f"{manage_dot_py} create_session {email}")
            return session_key.strip()
