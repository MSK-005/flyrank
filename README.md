# FlyRank Assignment 1
## Setting Up
Install the prerequisite libraries by using the command:
```pip install -r requirements.txt```
After that, run the server:
```fastapi dev```
This will start the server on `http://localhost:8000/`
## Creating a Task
We create a task by sending a POST request, with the title mentioned in the payload. SwaggerUI allows us to test our CRUD API's endpoints without manually writing `curl` commands. In this example, we create a task to "wash the dishes." Note that there were already 3 tasks created in memory before we created this task.
![Creating our task](/docs/swagger/create_task.png "Creating our task")

## Seeing All of Our Created Tasks
To fetch anything from an API, we make a GET request. Since we are requesting to see all created tasks regardless of their IDs, this endpoint will return just that.
![Viewing all created tasks](/docs/swagger/get_all_tasks.png "Viewing all tasks")

## Updating a Task
To update anything, we send a PUT request, along with the ID of the item we want to update. In this example, we send a PUT request to update the status of the task we created in "Creating a task" section. In that example, the status of the task was by default set to false. Now we change it to true, to indicate the task is done.
![Updating our task](/docs/swagger/update_task_1.png "Updating our task (1)")
![Updating our task](/docs/swagger/update_task_2.png "Updating our task (2)")

## Deleting a Task
To delete anything, we send a DELETE request to the server, along with the ID of the item to delete. In this example, we delete the task we created in the "Creating a task" section.
![Deleting our task](/docs/swagger/delete_task.png "Deleting our task")

## Sample Request & Response (`curl -i`)
The request:
```
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```
The response:
```
HTTP/1.1 201 Created
date: Mon, 03 Aug 2026 08:36:04 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":3,"title":"Buy milk","done":false}
```
## All Endpoints
| Method | Endpoint | Description | Success Code | Error Codes |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API metadata | `200 OK` | — |
| `GET` | `/health` | Health check | `200 OK` | — |
| `GET` | `/tasks` | List tasks (supports `?search_string=` & `?done=`) | `200 OK` | — |
| `GET` | `/tasks/{id}` | Get task by ID | `200 OK` | `404` |
| `POST` | `/tasks` | Create task | `201 Created` | `400` |
| `PUT` | `/tasks/{id}` | Update task | `200 OK` | `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete task | `204 No Content` | `404` |
| `GET` | `/stats` | Aggregate stats | `200 OK` | — |
| `POST` | `/reset` | Re-seed in-memory storage | `200 OK` | — |

## The Mortality Experiment
Since all tasks were created in memory and not stored in a database, when we reset the server, all of our created tasks will be lost. The memory is not a good place to store data that needs to exist permanently. For that, we need a database.

# Assignment 2 - Adding a Database
## Data Now Lives Permanently
Previously, all data was stored in memory, and any server restarts meant loss of data. Now with the introduction of a database, our data stays safe and lives on. To monitor our database, we use [DB Browser for SQLite](https://sqlitebrowser.org/). We use the following SQL command to change the completion status of a task with ID 2.
```
UPDATE tasks SET done = 1 WHERE id = 2;
```

To check if the changes have been made, we make a `curl` request.
```
curl http://localhost:8000/tasks
```
The response:
```
[
    {"id":1,"title":"Complete CN assignment","done":0},
    {"id":2,"title":"Write data ingestion logic","done":1},
    {"id":3,"title":"Walk the dog","done":0}
]
```
The request returns all tasks, and we can see the task with ID = 2 has changed its completion status.