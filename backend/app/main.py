from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# With a bit more time I could have added the logic to a postgresql db for the sake of data perstistancy
poll_data = [
    {
        "id": 1,
        "question": "Did the Netherlands get robbed at the euro 2024?",
        "options": ["Yes", "yes but with lower y", "no", "yes, lol"],
        "votes": {
            "Yes": 0,
            "yes but with lower y": 0,
            "no": 0,
            "yes, lol": 0
        }
    },
    {
        "id": 2,
        "question": "Do you like a good jucy kapsalon?",
        "options": ["Yes", "yes but with lower y", "no", "yes, lol"],
        "votes": {
            "Yes": 0,
            "yes but with lower y": 0,
            "no": 0,
            "yes, lol": 0
        }
    }
]

class Vote(BaseModel):
    question_id: int
    option: str

#gets all the polls
@app.get("/polls")
async def get_polls():
    return [{"id": poll["id"], "question": poll["question"]} for poll in poll_data]

@app.get("/poll/{question_id}")
async def get_poll(question_id: int):
    poll = next((poll for poll in poll_data if poll["id"] == question_id), None)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@app.post("/vote")
async def submit_vote(vote: Vote):
    poll = next((poll for poll in poll_data if poll["id"] == vote.question_id), None)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    if vote.option not in poll["options"]:
        raise HTTPException(status_code=400, detail="Invalid option")
    poll["votes"][vote.option] += 1
    return {"message": "Vote submitted successfully"}

@app.get("/results/{question_id}")
async def get_results(question_id: int):
    poll = next((poll for poll in poll_data if poll["id"] == question_id), None)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll["votes"]