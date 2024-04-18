import csv
from .data_prepropressing import preprocessing

def prepare_data():
    x_data = []
    y_data = []
    with open('data/reviews_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            x_data.append(preprocessing(row[0]))
            y_data.append(int(row[1]))
    
    return x_data, y_data
