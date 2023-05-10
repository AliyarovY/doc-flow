import uvicorn

from doc_flow.settings import settings


uvicorn.run(
    'doc_flow.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
