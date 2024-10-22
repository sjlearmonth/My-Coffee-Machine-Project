from data import MENU, resources

def print_report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${money_in_coffee_machine:,.2f}")
    return

def calculate_money_inserted():
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickles = int(input("How many nickles?: "))
    pennies = int(input("How many pennies?: "))
    money_inserted = (quarters * 25 + dimes * 10 + nickles * 5 + pennies) / 100.0
    return round(money_inserted, 2)

def serve_user(selection):
    global money_in_coffee_machine
    money_inserted = calculate_money_inserted()
    cost_of_coffee = MENU[selection]['cost']
    money_in_coffee_machine += money_inserted
    change_back = money_inserted - cost_of_coffee
    return change_back

def check_and_update_stock_levels(selection):
    coffee_ingredients = MENU[selection]['ingredients']
    for ingredient in coffee_ingredients:
        if ingredient == 'water':
            if resources['water'] < coffee_ingredients[ingredient]:
                return 'not_enough_water_left'
            else:
                resources['water'] -= coffee_ingredients[ingredient]
        elif ingredient == 'milk':
            if resources['milk'] < coffee_ingredients[ingredient]:
                return 'not_enough_milk_left'
            else:
                resources['milk'] -= coffee_ingredients[ingredient]
        else:
            if resources['coffee'] < coffee_ingredients['coffee']:
                return 'not_enough_coffee_left'
            else:
                resources['coffee'] -= coffee_ingredients['coffee']
    return 'coffee_machine_operational'

money_in_coffee_machine = 0
coffee_machine_is_ON = True
ingredients_available = {'espresso' : True, 'latte' : True, 'cappuccino' : True}

def report_low_stock_level(status):

    global coffee_machine_is_ON
    global ingredients_available
    start_of_ingredient = 11
    end_of_ingredient = len(status) - 5

    ingredient = status[start_of_ingredient:end_of_ingredient]
    user_message = f"Coffee machine does not have enough {ingredient} left to serve you "
    if user_selection == 'espresso':
        user_message += "an "
    else:
        user_message += "a "
    user_message += user_selection
    print(user_message)

    print("Please try another selection.")

    ingredients_available[user_selection] = False

while coffee_machine_is_ON:

    user_selection = input("What would you like? espresso/latte/cappuccino: ").lower()

    if user_selection == "off":
        print("Coffee machine has been switched off. Goodbye.")
        coffee_machine_is_ON = False
    elif user_selection == 'report':
        print_report()
    elif user_selection == 'espresso' or user_selection == 'latte' or user_selection == 'cappuccino':

        machine_status = check_and_update_stock_levels(user_selection)

        if machine_status == 'coffee_machine_operational':

                change = round(serve_user(user_selection), 2)

                if change < 0.0:

                    while change < 0.0:

                        print(f"You haven't inserted enough coins.")
                        print(f'Please insert another ${-change:,.2f}.')
                        money_inserted = calculate_money_inserted()
                        money_in_coffee_machine += money_inserted
                        change += money_inserted
                        change = round(change, 2)

                    print(f"Thank you, you have now inserted enough coins for your {user_selection}.")
                    print(f"Here is your {user_selection}, enjoy!")

                    if change > 0.0:
                        print(f"Here is ${change:,.2f} in change.")
                        money_in_coffee_machine -= change

                else:
                    print(f"Thank you, you have now inserted enough coins for your {user_selection}.")
                    print(f"Here is your {user_selection}, enjoy!")
                    if change > 0.0:
                        print(f"Here is ${change:,.2f} in change.")
                        money_in_coffee_machine -= change

        else:

            report_low_stock_level(machine_status)

            if not (ingredients_available['espresso'] or
                    ingredients_available['latte'] or
                    ingredients_available['cappuccino']):
                print("Sorry, unable to serve any coffee at this time due to low stock levels.")
                print("Please come back again when the coffee machine has been re-stocked.")
                coffee_machine_is_ON = False
    else:
        print("Error. You have entered an invalid selection.")
        print("Please try again. Goodbye.")
