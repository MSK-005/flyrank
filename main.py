from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {
        "id": 0,
        "title": "Complete the PR process for PyTorch",
        "done": False
    },
    {
        "id": 1,
        "title": "Write the data ingestion logic for the GDACS API",
        "done": False
    },
    {
        "id": 2,
        "title": "Read and understand the issue created by Mr. Harsh",
        "done": False
    }
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
    task = next((item for item in tasks if item['id'] == id), None)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {id} was not found.")
    return task