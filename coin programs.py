import coffee_data

print(list(coffee_data.coin_value['1'].items())[0])
# Display the menu
coin_sum = 0
print("Coin Menu:")
for index, coin_data in coffee_data.coin_value.items():
    # Extract coin name and its value from the inner dictionary
    coin, value = list(coin_data.items())[0]

    # Print the index, coin name, and value with formatting
    print(f'{index}: {coin + ":":10} {value:>10.2f}')

# Prompt user for input
user_choice = input("Enter the number corresponding to the coin: ")

# Check if the user_choice is valid
if user_choice in (list(coffee_data.coin_value.keys())):
    # Get the selected coin data
    selected_coin_data = coffee_data.coin_value[user_choice]
    selected_coin, coin_value = list(selected_coin_data.items())[0]

    print(f'You selected {selected_coin}, which is worth ${coin_value:.2f}')

    # Ask for the number of coins and calculate the total value
    selected_coin_count = int(input(f"How many {selected_coin}s would you like to enter? "))
    total_value = selected_coin_count * coin_value
    print(f'Total  of {selected_coin_count} {selected_coin}(s) valued at: ${total_value:.2f}')

    # Add to the coin_sum
    coin_sum += total_value
    print(f'Your current coin total is: ${coin_sum:.2f}')
else:
    print("Invalid selection. Please choose a valid number.")
