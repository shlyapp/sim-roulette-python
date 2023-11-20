import uvicorn
import logging

from .main import app, consumer_thread

logging.basicConfig(
    filename="sim-roulette-python/api/logs.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    logging.info("FastAPI start")
    consumer_thread.start()
    main()
