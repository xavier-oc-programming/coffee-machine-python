def resource_check(order):
    for ingredient in coffee_data.MENU[order]['ingredients']:
        print(f"Menu Ingredient: {ingredient} \n"
              f'Menu Amount needed: {coffee_data.MENU[order]["ingredients"][ingredient]}')
        print()
        print(f"Resources ingredient: {ingredient} \n"
              f"Resource amount available {coffee_data.resources[ingredient]}")
        print()
        print()
        if coffee_data.MENU[order]["ingredients"][ingredient] > coffee_data.resources[ingredient]:
            return False
    return True
s