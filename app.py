import uvicorn
from fastapi import FastAPI
from utils.data_preparing import preprocessing
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from pydantic import BaseModel
import pickle
import numpy as np
from typing import List

# Define Review
class Review(BaseModel):
    text: str

# Create the app object
app = FastAPI()

@app.get('/')
def index():
   return {'message': 'Welcome!'}

@app.post('/predict')
async def predict(review: Review):
    prediction = predict_sentiment(review.text)

    return {'prediction': prediction}

@app.post('/predict/batch')
async def predict_batch(reviews: List[Review]):
    predictions = []
    for review in reviews:
        sentiment = predict_sentiment(review.text)
        predictions.append({'review': review.text, 'sentiment': sentiment})

    return predictions

def predict_sentiment(text):
    word_list = preprocessing(text)
    if len(word_list) == 0:
        return 2
    model = load_model('./models/review_model.h5')

    tokenizer = None
    with open("./models/review_tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    
    max_len=200
    sequence = tokenizer.texts_to_sequences(word_list)
    padded_sequence = pad_sequences(sequence, maxlen=max_len)

    prediction = model.predict(padded_sequence)
    prediction = np.argmax(prediction, axis=1)
    positive_count = np.sum(prediction == 0)
    negative_count = np.sum(prediction == 1)
    neutral_count = np.sum(prediction == 2)

    if positive_count > negative_count and positive_count > neutral_count:
        return 'positive'
    elif negative_count > positive_count and negative_count > neutral_count:
        return 'negative'
    else:
        return 'neutral'

if __name__ == '__main__':
   #Run by: uvicorn app:app --reload
   uvicorn.run(app, host='0.0.0.0', port=8000)
