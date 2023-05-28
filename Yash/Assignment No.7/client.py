import requests

url = 'http://127.0.0.1:5000/'

def add_num(num1, num2):
    endpoint = url + 'add'
    data = {"num1": num1, "num2": num2}
    response = requests.post(endpoint, json=data)
    result = response.json()['result']
    return result

def multiply_num(num1, num2):
    endpoint = url + 'multiply'
    data = {"num1": num1, "num2": num2}
    response = requests.post(endpoint, json=data)
    result = response.json()["result"]
    return result

state = True

while state:
    try:
        print("Enter the first number:")
        num1 = int(input())
        print("Enter the second number:")
        num2 = int(input())

        print("Do you want to:\n1. Add\n2. Multiply\n3. Exit")
        choice = int(input(""))

        if choice == 1:
            print(add_num(num1, num2))
            print("Do you wish to continue? (Yes, No)")
            if input().lower() == "no":
                state = False

        elif choice == 2:
            print(multiply_num(num1, num2))
            print("Do you wish to continue? (Yes, No)")
            if input().lower() == "no":
                state = False

        elif choice == 3:
            print("Thank you for using the service")
            state = False

        else:
            print("Invalid Input")

        if state:
            print("New Calculation")
            print("_" * 10, end="\n")

    except Exception as e:
        print("Encountered Error:", str(e))
        print("Restarting interface", end="\n")
