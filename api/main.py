from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def get_welcome():
    return {'hello', 'world'}




