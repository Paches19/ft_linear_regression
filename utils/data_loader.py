# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    data_loader.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: adpachec <adpachec@student.42madrid.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/28 10:01:12 by adpachec          #+#    #+#              #
#    Updated: 2024/05/28 11:06:35 by adpachec         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import csv

def load_training_data(filepath):
    mileages = []
    prices = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    mileages.append(float(row[0]))
                    prices.append(float(row[1]))
                except ValueError:
                    print(f"Error de conversión: {row} no puede convertirse a float")
                    continue
    except FileNotFoundError:
        print(f"Error: El archivo {filepath} no fue encontrado.")
        return [], []
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return [], []
    return mileages, prices

def save_model_parameters(params, filepath):
    try:
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Theta0', 'Theta1'])
            writer.writerow([params[0], params[1]])
    except IOError as e:
        print(f"No se pudo escribir en el archivo {filepath}: {e}")

def load_model_parameters(filepath):
    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            parameters = next(reader)
            return float(parameters[0]), float(parameters[1])
    except FileNotFoundError:
        print(f"Error: El archivo {filepath} no fue encontrado.")
        return None, None
    except ValueError:
        print(f"Error de conversión: {parameters} no pueden convertirse a float")
        return None, None
    except Exception as e:
        print(f"Error al leer el archivo {filepath}: {e}")
        return None, None 
