import matplotlib.pyplot as plt

def plot_reviews_data(data):
    word_counts = [len(word_list) for word_list in data]

    count_dict = {}
    for count in word_counts:
        count_dict[count] = count_dict.get(count, 0) + 1

    x = list(count_dict.keys())
    y = list(count_dict.values())

    plt.bar(x, y, color='cornflowerblue')
    plt.xlabel('Number of words')
    plt.ylabel('Quantity')
    plt.title('Statistics on the number of words in the data')
    plt.show()

def plot_history_model(history):
    # Plot history loss
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='train loss')
    plt.plot(history.history['val_loss'], label='val loss')
    plt.xlabel("epoch")
    plt.ylabel("Cross-entropy loss")
    plt.legend()
    plt.show()

    # Plot history accuracy
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['accuracy'], label='train accuracy')
    plt.plot(history.history['val_accuracy'], label='val accuracy')
    plt.xlabel("epoch")
    plt.ylabel("accuracy")
    plt.legend()
    plt.show()