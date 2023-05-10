from fastapi import FastAPI

from doc_flow import api


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },

]

app = FastAPI(
    title='DocFlow',
    description='Сервис обработки документов',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(api.router)
