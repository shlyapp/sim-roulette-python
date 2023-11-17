from fastapi import FastAPI
from queue import Queue, Empty
from threading import Thread
from time import sleep


app = FastAPI()
counter = 0
queue = Queue()


def consumer(queue):
    while True:
        try:
            item = queue.get()
        except Empty:
            continue
        else:
            print(f"Обработка элемента {item}")
            sleep(5)
            print(f"Обработан элемент {item}")
            queue.task_done()


consumer_thread = Thread(
    target=consumer,
    args=(queue,),
    daemon=True
)


@app.post("/add_task/")
async def add_task():
    global counter
    queue.put(counter)
    print(f"В очередь на обработку добавлен элемент {counter}")
    counter += 1


@app.get("/task/{id}")
async def get_task():
    pass
