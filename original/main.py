import coffee_data

machine_on = True
ordering_coffee = None

STARTING_RESOURCES = {
    "water":  300,
    "milk":   200,
    "coffee": 100,
}


# define enough_resources_check
def resource_check(order):
    for ingredient in coffee_data.MENU[order]['ingredients']:
        if coffee_data.MENU[order]["ingredients"][ingredient] > coffee_data.resources[ingredient]:
            return False
    return True


# define resource update
def resource_update(order):
    for ingredient in coffee_data.MENU[order]['ingredients']:
        coffee_data.resources[ingredient] -= coffee_data.MENU[order]['ingredients'][ingredient]


# Create program---[machine on]---that can execute the following functionalities
# 1) ask for command from user:
#   a) turn off
#   b) get resource report
#   b2) refill all / refill <ingredient>
#   c) PART 1: Order type of coffee
#   c) PART 2: Check if coffe can be made (sufficient resources)
#   d) Define cost of selected coffee
#   e) Create system for collecting coins
#       e) PART 1: Print Coin Reference Display menu
#       e) PART 2: Ask user for coins
#           e) PART 2A: Coin type
#           e) PART 2B: Coin amount
#           e) PART 2C: Make sum calculation
#   f) Give back change
#   g) update resources

print("\nCoffee Machine ready.")
print("  Orders  : espresso / latte / cappuccino")
print("  Commands: report / refill / refill <ingredient> / off\n")

while machine_on:
    user_input = input(">> ")

    #   a) turn off
    if user_input == "off":
        print("\nCoffee machine is now turning off..."
              "\nHave a nice day!")
        break

    #   b) get resource report
    elif user_input == 'report':
        # Align text with padding
        print(f"{'Water:':<10} {coffee_data.resources['water']}ml")
        print(f"{'Milk:':<10} {coffee_data.resources['milk']}ml")
        print(f"{'Coffee:':<10} {coffee_data.resources['coffee']}g")
        print(f"{'Money:':<10} ${coffee_data.resources['money']:.2f}")

    #   b2) refill all ingredients
    elif user_input == 'refill':
        for ingredient in STARTING_RESOURCES:
            coffee_data.resources[ingredient] = STARTING_RESOURCES[ingredient]
        print("Refilled all ingredients.")
        print(f"  Water:  {coffee_data.resources['water']}ml")
        print(f"  Milk:   {coffee_data.resources['milk']}ml")
        print(f"  Coffee: {coffee_data.resources['coffee']}g")

    #   b3) refill a single ingredient
    elif user_input.startswith('refill '):
        ingredient = user_input[7:]
        if ingredient in STARTING_RESOURCES:
            coffee_data.resources[ingredient] = STARTING_RESOURCES[ingredient]
            units = {"water": "ml", "milk": "ml", "coffee": "g"}
            print(f"Refilled {ingredient}: {coffee_data.resources[ingredient]}{units[ingredient]}")
        else:
            print(f'"{ingredient}" is not a refillable ingredient. Try: water / milk / coffee')

    #   c) order type of coffee
    #   assuming the input is in the coffee_data.py MENU dictionary (keys)--> ['espresso', 'latte', 'cappuccino']

    # checking validity of order (if it's in the menu)
    elif f'{user_input}' in (list((coffee_data.MENU.keys()))):
        ordering_coffee = True
        print("Checking coffee order...")
    else:
        print(f'Could not fulfill your command of "{user_input}".\n'
              f"Please try again.")

    #   c) PART 2: Check if coffee can be made (sufficient resources)
    while ordering_coffee:
        # check resources
        enough_resources = resource_check(user_input)
        if enough_resources:
            print("Sufficient resources to prepare order.")
        else:
            print("Insufficient resources to prepare order.")
            ordering_coffee = False
            break
        #   d) Define cost of selected coffee
        order_cost = float(coffee_data.MENU[user_input]['cost'])
        print(f'Your order of {user_input} will be a total of ${order_cost:.2f}')

        #   e) Create system for collecting coins
        #       e) PART 1: Print Coin Reference Display menu
        print("Coin Menu:")
        for index, coin_data in coffee_data.coin_value.items():
            # Extract coin name and its value from the inner dictionary
            coin_face_name, coin_value = list(coin_data.items())[0]
            # Print the index, coin name, and value with formatting
            print(f'{index}: {coin_face_name + ":":<10} ${coin_value:.2f}')

        #       e) PART 2: Ask user for coins
        coin_sum = 0
        while coin_sum < order_cost:
            coin_choice = input("Enter the number corresponding to the coin: ")
            # check if coin choice is valid
            if coin_choice in list(coffee_data.coin_value.keys()):
                selected_coin_data = list(coffee_data.coin_value[coin_choice].items())[0]
                selected_coin, selected_coin_value = selected_coin_data
                print(f'You selected {selected_coin}, which is worth ${selected_coin_value:.2f}')
                # e)    PART 2C: Make sum calculation
                coin_choice_amount = int(input("How many of this coin would you like to enter?"))
                total_value = coin_choice_amount * selected_coin_value
                coin_sum += total_value
                print(f"You have added a total of ${total_value:.2f}")
                print(f'Your sum of coins is {coin_sum:.2f}')

            else:
                print("Invalid selection. Please choose a valid number.")

            # If enough coins are inserted
        if coin_sum >= order_cost:
            change = coin_sum - order_cost
            print(f"Thank you! Preparing your {user_input}. Your change is ${change:.2f}.")

        # Update resources
        resource_update(user_input)
        coffee_data.resources['money'] += order_cost
        ordering_coffee = False
