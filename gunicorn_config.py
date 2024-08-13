bind = "unix:/run/gunicorn.sock"
workers = 3
wsgi_app = "Stella.wsgi:application"  # 프로젝트 이름이 Stella라고 가정
