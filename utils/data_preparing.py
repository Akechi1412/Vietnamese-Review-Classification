import csv
from .data_prepropressing import preprocessing

def prepare_data():
    print("Preparing data...")
    x_data = []
    y_data = []
    with open('data/reviews_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            word_list = preprocessing(row[0])
            label = int(row[1])
            if len(word_list) > 0:
                x_data.append(word_list)
                y_data.append(label)
    
    return x_data, y_data
