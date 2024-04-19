from utils.data_preparing import preprocessing
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

if __name__ == '__main__':
    word_list = preprocessing('tuyệt vời')
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
        print('Positive')
    elif negative_count > positive_count and negative_count > neutral_count:
        print('Negative')
    else:
        print('Neutral')