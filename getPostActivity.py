from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()


class Activity(BaseModel):
    name: str
    location: str = None
    duration_minutes: int
    
    
activities = []

@app.post("/activities/", response_model=Activity)
def create_activity(activity: Activity):
    activities.append(activity)
    return activity

@app.get("/", response_model=List[Activity])
def get_activities():
    return activities

@app.delete("/activities/{activity_id}", response_model=Activity)
def delete_activity(activity_id: int):
    if activity_id < 0 or activity_id >= len(activities):
        raise HTTPException(status_code=404, detail="Activity not found")
    deleted_activity = activities.pop(activity_id)
    return deleted_activity

@app.put("/activities/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, updated_activity: Activity):
    if activity_id < 0 or activity_id >= len(activities):
        raise HTTPException(status_code=404, detail="Activity not found")
    activities[activity_id] = updated_activity
    return updated_activity

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")