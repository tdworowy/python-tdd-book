import os
import random
from fabric import Connection

REPO_URL = 'https://github.com/tdworowy/python-tdd-book.git'
server = ''

conn = Connection(host=server)


def deploy():
    site_folder = f'/home/{conn.env.user}/sites/{conn.env.host}'
    conn.run(f'mkdir -p {site_folder}')
    with conn.cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if conn.exists('.git'):
        conn.run('git fetch')
    else:
        conn.run(f'git clone {REPO_URL} .')
    current_commit = conn.local("git log -n 1 --format=%H", capture=True)
    conn.run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not conn.exists('virtualenv/bin/pip'):
        conn.run(f'python3.8 -m venv virtualenv')
    conn.run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    conn.append('.env', 'DJANGO_DEBUG_FALSE=y')
    conn.append('.env', f'SITENAME={conn.env.host}')
    current_contents = conn.run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        conn.append('.env', f'DJANGO_SECRET_KEY={new_secret}')
        email_password = os.environ['EMAIL_PASSWORD']
        conn.append('.env', f'EMAIL_PASSWORD={email_password}')

def _update_static_files():
    conn.run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    conn.run('./virtualenv/bin/python manage.py migrate --noinput')


if __name__ == "__main__":
    deploy()
