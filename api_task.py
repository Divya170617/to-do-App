from http.client import HTTPException

from fastapi import FastAPI
HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()
FILENAME="tasks.json"

#Load tasks from JSON
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME,'r') as f:
            return json.load(f)
    return []

#Save tasks to JSON
def save_tasks(tasks):
    with open(FILENAME,'w') as f:
        json.dump(tasks,f,indent=2)

#Pydanic model
class Task(BaseModel):
     id: int
     title: str
     description: str
     completed: bool = False

@app.post("/add_task/")
def add_task(task: Task):
    tasks=load_tasks()
    if any(t["id"] == task.id for t in tasks):
        raise
        HTTPException(status_code=400,
detail="Task ID already eists")
    tasks.append(task.dict())
    save_tasks(tasks)
    return {"message": "Task added","task":task}

@app.get("/view_tasks/")
def view_tasks():
    return {"tasks": load_tasks()}

@app.put("/complete_task/{task_id}")
def complete_task(task_id:int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
        return {"message": "Task"
"marked as completed"}
    raise HTTPException(status_code=404,
    detail="Task not found")

@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        raise
        HTTPException(status_code=404,detail="Task not found")
        save_tasks(new_tasks)
        return {"message": "Task deleted"}










