from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Thing(BaseModel):
    name: str
    id: int


@app.get("/")
def main():
    return {"this is main"}


@app.post("/thing")
def thing(thing: Thing):
    thing.id += 1
    return thing
