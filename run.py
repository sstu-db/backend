import uvicorn
from database import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SERVER_HOST,
        port=int(SERVER_PORT),
        reload=True  # Enable auto-reload during development
    )
