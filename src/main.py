from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import Field

from src.database import get_db_connection, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

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
    with get_db_connection() as connection:
        cursor = connection.cursor()
        conditions = []
        params = []
        if search_string is not None:
            conditions.append("title LIKE ?")
            params.append(f"%{search_string}%")
        if done is not None:
            conditions.append("done = ?")
            params.append(done)

        query = "SELECT * FROM tasks"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
    return [dict(result) for result in results]
    

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
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        task = cursor.fetchone()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Task not found"})

    return dict(task)

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(res: dict):
    title = res.get('title')
    if title is None or str(title).strip() == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Title is required."})
    title = str(title).strip()
    done = False
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, done))
        connection.commit()
        task_id = cursor.lastrowid

    return {
        "id": task_id,
        "title": title,
        "done": done
    }

@app.post("/reset")
async def reset_tasks():
        
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

    conditions = []
    params = []
    if title is not None:
        conditions.append("title = ?")
        params.append(title.strip())
    if done is not None:
        conditions.append("done = ?")
        params.append(1 if done else 0)
    params.append(id)

    query = f"UPDATE tasks SET {", ".join(conditions)} WHERE id = ?"
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found.")
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        new_task = cursor.fetchone()
    return (dict(new_task))


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found.")