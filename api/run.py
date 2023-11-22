import uvicorn

from .main import app, consumer_thread


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    consumer_thread.start()
    main()
