import uvicorn

from source.app import create_app
from source import settings

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.PORT,
        debug=settings.DEBUG,
        reload=settings.RELOAD,
    )
