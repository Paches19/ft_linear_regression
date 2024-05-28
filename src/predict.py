# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    predict.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: adpachec <adpachec@student.42madrid.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/28 10:18:03 by adpachec          #+#    #+#              #
#    Updated: 2024/05/28 11:18:40 by adpachec         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from utils.data_loader import load_model_parameters

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def main():
    model_filepath = './data/model_parameters.csv'

    theta0, theta1 = load_model_parameters(model_filepath)

    while True:
        try:
            mileage = float(input("Ingrese el kilometraje del coche: "))

            estimated_price = estimate_price(mileage, theta0, theta1)
            print(f"El precio estimado del coche es: {estimated_price:.2f}€")
        except ValueError:
            print("Por favor, introduzca un número válido para el kilometraje o escriba 'salir' para terminar.")
            continue

        user_input = input("¿Desea realizar otra estimación? (s/n): ")
        if user_input.lower() != 's':
            break

if __name__ == "__main__":
    main()