# FlyRank Assignment 1
## Creating a task
We create a task by sending a POST request, with the title mentioned in the payload. SwaggerUI allows us to test our CRUD API's endpoints without manually writing `curl` commands. In this example, we create a task to "wash the dishes." Note that there were already 3 tasks created in memory before we created this task.
![Creating our task](/docs/swagger/create_task.png "Creating our task")

## Seeing all of our created tasks
To fetch anything from an API, we make a GET request. Since we are requesting to see all created tasks regardless of their IDs, this endpoint will return just that.
![Viewing all created tasks](/docs/swagger/get_all_tasks.png "Viewing all tasks")

## Updating a task
To update anything, we send a PUT request, along with the ID of the item we want to update. In this example, we send a PUT request to update the status of the task we created in "Creating a task" section. In that example, the status of the task was by default set to false. Now we change it to true, to indicate the task is done.
![Updating our task](/docs/swagger/update_task_1.png "Updating our task")
![Updating our task](/docs/swagger/update_task_2.png "Updating our task")

## Deleting a task
To delete anything, we send a DELETE request to the server, along with the ID of the item to delete. In this example, we delete the task we created in the "Creating a task" section.
![Deleting our task](/docs/swagger/delete_task.png)