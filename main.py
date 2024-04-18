from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle

def predict_sentiment(text):
    model = load_model('/models/review_model.keras')

    tokenizer = None
    with open("/models/tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    
    max_len=200
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)

    prediction = model.predict_classes(padded_sequence)[0][0]

    print(prediction)

predict_sentiment('Sản phẩm bình thường')

