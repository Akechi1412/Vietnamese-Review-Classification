import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

def predict_sentiment(text):
    model = tf.keras.models.load_model('D:/Vietnamese-Review-Classification/models/review_model.keras')

    tokenizer = None
    with open("D:/Vietnamese-Review-Classification/models/review_tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    max_len = 200
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)

    prediction = model.predict(padded_sequence)
    predicted_class = tf.argmax(prediction, axis=-1).numpy()[0]

    print(predicted_class)

predict_sentiment('sản phẩm như cái lồn')

