from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import itertools

app = FastAPI()
_id_iter:int = itertools.count()

class Task(BaseModel):

    id:int = Field(default_factory=lambda: next(_id_iter))
    title:str
    done:bool = False

tasks = [
    Task(title="Complete the PR process for PyTorch"),
    Task(title="Write the data ingestion logic for the GDACS API"),
    Task(title="Read and understand the issue created by Mr. Harsh")
]

@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
        }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_all_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task(id: int):
    task = next((item for item in tasks if item.id == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {id} was not found.")
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(res:dict):
    title = res.get('title')
    if title is None or str(title).strip() == '':
        raise HTTPException(status_code=400, detail="Title is either missing or empty.")
    title = str(title).strip()
    task = Task(title=title)
    tasks.append(task)
    return task