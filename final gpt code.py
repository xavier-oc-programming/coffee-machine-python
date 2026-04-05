import coffee_data

machine_on = True
ordering_coffee = None

print(list(coffee_data.coin_value.keys()))

# Define enough_resources_check
def resource_check(order):
    for ingredient in coffee_data.MENU[order]['ingredients']:
        if coffee_data.MENU[order]["ingredients"][ingredient] > coffee_data.resources[ingredient]:
            return False
    return True


# Check if resource amount is more than order amount
while machine_on:
    user_input = input("What would you like? (espresso/latte/cappuccino): ")

    if user_input == "off":
        print("\nCoffee machine is now turning off..."
              "\nHave a nice day!")
        break

    if user_input == 'report':
        # Align text with padding
        print(f"{'Water:':<10} {coffee_data.resources['water']}ml")
        print(f"{'Milk:':<10} {coffee_data.resources['milk']}ml")
        print(f"{'Coffee:':<10} {coffee_data.resources['coffee']}g")
        print(f"{'Money:':<10} ${coffee_data.resources['money']:.2f}")

    # User defines order
    if f'{user_input}' in list(coffee_data.MENU.keys()):
        ordering_coffee = True
        print("Checking coffee order...")

    while ordering_coffee:
        # Check resources
        enough_resources = resource_check(user_input)
        if enough_resources:
            print("Sufficient resources to prepare order.")
        else:
            print("Insufficient resources to prepare order.")
            ordering_coffee = False
            break

        # Process coins
        coin_sum = 0
        print("\nCoin Menu:")
        for index, coin_data in coffee_data.coin_value.items():
            # Extract coin name and its value from the inner dictionary
            coin, value = list(coin_data.items())[0]

            # Print the index, coin name, and value with formatting
            print(f'{index}: {coin + ":":10} {value:>10.2f}')

        # Prompt user for input
        total_cost = coffee_data.MENU[user_input]['cost']
        print(f"The total cost for {user_input} is: ${total_cost:.2f}")

        while coin_sum < total_cost:
            user_choice = input("Enter the number corresponding to the coin: ")

            # Check if the user_choice is valid
            if user_choice in coffee_data.coin_value:
                # Get the selected coin data
                selected_coin_data = coffee_data.coin_value[user_choice]
                selected_coin, coin_value = list(selected_coin_data.items())[0]

                print(f'You selected {selected_coin}, which is worth ${coin_value:.2f}')

                # Ask for the number of coins and calculate the total value
                selected_coin_count = int(input(f"How many {selected_coin}s would you like to enter? "))
                total_value = selected_coin_count * coin_value
                print(f'Total value of {selected_coin_count} {selected_coin}(s): ${total_value:.2f}')

                # Add to the coin_sum
                coin_sum += total_value
                print(f'Your current coin total is: ${coin_sum:.2f}')
            else:
                print("Invalid selection. Please choose a valid number.")

        # If enough coins are inserted
        if coin_sum >= total_cost:
            change = coin_sum - total_cost
            print(f"Thank you! Preparing your {user_input}. Your change is ${change:.2f}.")

            # Update resources
            for ingredient in coffee_data.MENU[user_input]['ingredients']:
                coffee_data.resources[ingredient] -= coffee_data.MENU[user_input]['ingredients'][ingredient]
            coffee_data.resources['money'] += total_cost
            ordering_coffee = False
        else:
            print("Not enough money entered. Transaction canceled.")
            break