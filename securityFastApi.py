import secrets
from typing import Annotated,List
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
app = FastAPI()

security = HTTPBasic()

class Activity(BaseModel):
    name: str
    location: str = None
    duration_minutes: int
    

def get_authenticated(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    provided_userid_bytes = credentials.username.encode("utf8")
    correct_userid_bytes = b"AIDiscoveries"
    compare_userid_result = secrets.compare_digest(
        provided_userid_bytes, correct_userid_bytes
    )
    provided_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"discovery"
    compare_password_result = secrets.compare_digest(
        provided_password_bytes, correct_password_bytes
    )
    if not (compare_userid_result and compare_password_result):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username





activities = []

@app.post("/activities/", response_model=Activity)
def create_activity(username:Annotated[str, Depends(get_authenticated)],activity: Activity):
    activities.append(activity)
    return activity

@app.get("/", response_model=List[Activity])
def get_activities(username:Annotated[str, Depends(get_authenticated)]):
    return activities


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")