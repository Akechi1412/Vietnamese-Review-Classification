from utils.data_preparing import preprocessing
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

def predict_sentiment(text):
    """
        0: positive
        1: negative
        2: neutral
    """
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
    prediction = np.argmax(prediction, axis=1)[0]

    return prediction

print(predict_sentiment('Sp bthg'))