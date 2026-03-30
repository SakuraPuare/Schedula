import uvicorn
from app.application import create_app
from app.core.settings import get_settings


settings = get_settings()
app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.bind_host, port=settings.bind_port)
