from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, time, timedelta
from typing import List, Optional
import uvicorn
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Reminder(BaseModel):
    message: str
    time_before_deadline: timedelta

class Todo(BaseModel):
    id: int
    title: str
    deadline: datetime
    status: str
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    time_spent: Optional[timedelta] = None
    reminders: List[Reminder] = []

todos = []

def load_todos():
    try:
        with open("todos.json", "r") as file:
            todos = json.load(file)
    except FileNotFoundError:
        todos = []

def save_todos():
    with open("todos.json", "w") as file:
        json.dump([todo.dict() for todo in todos], file)

@app.post("/todo/")
def create_todo(todo: Todo):
    todos.append(todo)
    save_todos()
    return {"message": "Todo added successfully"}

@app.get("/todo/", response_model=List[Todo])
def list_todos():
    load_todos()
    return todos

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            del todos[index]
            save_todos()
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    for index, existing_todo in enumerate(todos):
        if existing_todo.id == todo_id:
            todos[index] = todo
            save_todos()
            return {"message": "Todo updated successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    load_todos()
    uvicorn.run(app, host="127.0.0.1", port=8000)