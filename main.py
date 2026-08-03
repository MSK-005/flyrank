from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
import itertools

app = FastAPI()
_id_iter = itertools.count()

class Task(BaseModel):
    id: int = Field(default_factory=lambda: next(_id_iter))
    title: str
    done: bool = False

tasks = [
    Task(title="Complete CN assignment"),
    Task(title="Write the data ingestion logic for the GDACS API"),
    Task(title="Walk the dog")
]

@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats", "/reset"]
        }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_all_tasks(search_string: str | None = None, done: bool | None = None):
    return [task for task in tasks
            if (done is None or task.done is done)
            and (search_string is None or search_string.lower().strip() in task.title.lower())]

@app.get("/stats")
async def stats():
    total_tasks = len(tasks)
    done = len([task for task in tasks if task.done == True])
    unfinished = total_tasks - done

    return {
        "total": total_tasks,
        "done": done,
        "open": unfinished
    }

@app.get("/tasks/{id}")
async def get_task(id: int):
    task = next((item for item in tasks if item.id == id), None)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {id} was not found.")
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(res: dict):
    title = res.get('title')
    if title is None or str(title).strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is either missing or empty.")
    title = str(title).strip()
    task = Task(title=title)
    tasks.append(task)
    return task

@app.post("/reset")
async def reset_tasks():
    global _id_iter, tasks
    _id_iter = itertools.count()
    tasks = [
        Task(title="Complete CN assignment"),
        Task(title="Write the data ingestion logic for the GDACS API"),
        Task(title="Walk the dog")
    ]
    return {"message": "reset successful" }

@app.put("/tasks/{id}")
async def update_task(id: int, res: dict):
    title = res.get('title')
    done = res.get('done')
    if title is None and done is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data sent. Please update the title or the status of the task.")
    if title is not None and str(title).strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty.")
    if done is not None and not isinstance(done, bool):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The status of the task must be a boolean value.")

    task_idx = next((idx for idx, task in enumerate(tasks) if task.id == id), None)
    if task_idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found.")
    if title is not None:
        tasks[task_idx].title = str(title.strip())
    if done is not None:
        tasks[task_idx].done = done

    return tasks[task_idx]    


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    task = next((task for task in tasks if task.id == id), None)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found.")
    tasks.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)