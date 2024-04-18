from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

def predict_sentiment(text):
    model = load_model('./models/review_model.h5')

    tokenizer = None
    with open("./models/review_tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    
    max_len=200
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)

    prediction = model.predict(padded_sequence)
    prediction = np.argmax(prediction, axis=1)[0]

    return prediction