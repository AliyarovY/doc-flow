from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str = 'sqlite:////root/work/projects/docFlow/src/doc_flow/database.sqlite3'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    smtp_server: str
    smtp_port: int
    smtp_login: str
    smtp_password: str


settings = Settings(
    _env_file='/root/work/projects/docFlow/src/.env',
    _env_file_encoding='utf-8',
)
