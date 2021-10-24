import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from ml_utils import train_model, predict_category, retrain_model
from typing import List

# defining the main app
app = FastAPI(title="News Classifier", docs_url="/")

# calling the load_model during startup.
# this will train the model and keep it loaded for prediction.
app.add_event_handler("startup", train_model)

# class which is expected in the payload
class QueryIn(BaseModel):
    text: str

# class which is returned in the response
class QueryOut(BaseModel):
    category: str


# class which is expected in the payload while re-training
class FeedbackIn(BaseModel):
    category: str
    text: str


# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}


@app.post("/predict", response_model=QueryOut, status_code=200)
# Route to do the prediction using the ML model defined.
# Payload: QueryIn containing the parameters
# Response: QueryOut containing the flower_class predicted (200)
def predict(query_data: QueryIn):
    text = query_data.dict()['text']
    output = {"category": predict_category(text)}
    return output


@app.post("/retrain", status_code=200)
# Route to further train the model based on user input in form of feedback loop
# Payload: FeedbackIn containing the parameters and correct flower class
# Response: Dict with detail confirming success (200)
def retrain(data: List[FeedbackIn]):
    data = [item.dict() for item in data]
    retrain_model(data)
    return {"detail": "Retraining successful"}


# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=8889, reload=True)
