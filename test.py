from utils.data_preparing import prepare_data
from utils.plotter import plot_reviews_data

x_data, y_data = prepare_data()

print(y_data[:5])

print(len(max(x_data, key=len)))

plot_reviews_data(x_data)