"""TaskFlow demo API. Phase 1 stores tasks in memory; PostgreSQL comes later."""

from itertools import count

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="TaskFlow API", version="0.1.0")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)


class Task(TaskCreate):
    id: int
    completed: bool = False


_tasks: dict[int, Task] = {}
_next_id = count(1)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "taskflow-api", "status": "running"}


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def readiness() -> dict[str, str]:
    # Phase 1: no external dependencies. Check PostgreSQL here in Phase 2.
    return {"status": "ready"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(_tasks.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    task = Task(id=next(_next_id), title=payload.title)
    _tasks[task.id] = task
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
