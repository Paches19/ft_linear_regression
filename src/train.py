# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    train.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: adpachec <adpachec@student.42madrid.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/28 10:02:01 by adpachec          #+#    #+#              #
#    Updated: 2024/05/28 12:35:14 by adpachec         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import matplotlib.pyplot as plt
from utils.data_loader import load_training_data, save_model_parameters
import numpy as np
from PIL import Image
import os

def normalize(data):
	mean = np.mean(data)
	std = np.std(data)
	return [(x - mean) / std for x in data], mean, std

def denormalize(theta0, theta1, mean_x, std_x, mean_y, std_y):
	theta1 = theta1 * std_y / std_x
	theta0 = theta0 * std_y + mean_y - theta1 * mean_x
	return theta0, theta1

def create_gif(image_files, output_path):
    images = [Image.open(filename) for filename in image_files]
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=500, loop=0)
    for filename in image_files:
        os.remove(filename)
		
def gradient_descent(mileages, prices, normalized_mileages, normalized_prices, theta0, theta1, learning_rate, iterations, mean_x, std_x, mean_y, std_y):
	m = len(mileages)
	images = []
	for i in range(iterations):
		sum_errors_theta0 = 0
		sum_errors_theta1 = 0
		for j in range(m):
			error = (theta0 + theta1 * normalized_mileages[j]) - normalized_prices[j]
			sum_errors_theta0 += error
			sum_errors_theta1 += error * normalized_mileages[j]
		theta0 -= (learning_rate / m) * sum_errors_theta0
		theta1 -= (learning_rate / m) * sum_errors_theta1

		if i < 40 :
			t0, t1 = denormalize(theta0, theta1, mean_x, std_x, mean_y, std_y)
			filename = f'frame_{i}.png'
			plot_data_and_regression_line(mileages, prices, t0, t1, mean_x, std_x, mean_y, std_y, filename)
			images.append(filename)

	create_gif(images, 'training_progress.gif')
	return theta0, theta1

def plot_data_and_regression_line(mileages, prices, theta0, theta1, mean_x, std_x, mean_y, std_y, filename):
	plt.scatter(mileages, prices, color='blue')
	x_values = np.linspace(min(mileages), max(mileages))
	y_values = theta1 * x_values + theta0
	plt.plot(x_values , y_values, '-r', label='y = mx + k')
	plt.xlabel('Kilometraje')
	plt.ylabel('Precio')
	plt.title('Representacion regresion lineal')
	plt.legend()
	plt.savefig(filename)
	plt.close()

def calculate_r_squared(mileages, prices, theta0, theta1):
	mean_price = sum(prices) / len(prices)
	total_variance = sum((price - mean_price) ** 2 for price in prices)
	explained_variance = sum((theta0 + theta1 * mileage - mean_price) ** 2 for mileage in mileages)
	r_squared = explained_variance / total_variance
	return r_squared

def main():
	theta0 = 0
	theta1 = 0
	learning_rate = 0.1
	iterations = 1000
	data_filepath = './data/data.csv'
	model_filepath = './data/model_parameters.csv'

	mileages, prices = load_training_data(data_filepath)

	normalized_mileages, mean_x, std_x = normalize(mileages)
	normalized_prices, mean_y, std_y = normalize(prices)

	theta0, theta1 = gradient_descent(mileages, prices, normalized_mileages, normalized_prices, theta0, theta1, learning_rate, iterations, mean_x, std_x, mean_y, std_y)
	theta0, theta1 = denormalize(theta0, theta1, mean_x, std_x, mean_y, std_y)

	final_plot_filename = 'final_plot.png'
	plot_data_and_regression_line(mileages, prices, theta0, theta1, mean_x, std_x, mean_y, std_y, final_plot_filename)

	r2 = calculate_r_squared(mileages, prices, theta0, theta1)

	save_model_parameters([theta0, theta1], model_filepath)

	print(f"Model trained with parameters: Theta0 = {theta0}, Theta1 = {theta1}")
	print(f"Model precision: R2 = {r2}")

if __name__ == "__main__":
	main()