import csv
import json
import requests
from random import randint, random

local_url = "http://localhost:8000/"


def place_order(user_name, response):
    data = []
    item_num = []
    half_price = []
    full_price = []
    data_receieved = json.loads(response)
    for data in data_receieved:
        item_num.append(int(data["id"]))
        half_price.append(int(data["half"]))
        full_price.append(int(data["full"]))

    order_ids = []
    order_quantity = []
    order_type = []
    order_price = []
    order_cost = 0.00

    while(True):
        order_check = input(
            "\nEnter 'A' to add orders OR Enter 'N' to move ahead : ")
        if order_check == "N":
            break

        id_item = int(
            input("Please enter the Item Number from Menu you wish to order : "))
        order_ids.append(id_item)

        plate_type = input(
            "Should it be Half Plate(Enter 'H') or Full Plate(Enter 'F') : ")
        order_type.append(plate_type)
        item_quantity = int(
            input("What's the quantity you'd like to order..? : "))
        order_quantity.append(item_quantity)

        if plate_type == "H":
            item_price = float(half_price[id_item - 1] * item_quantity)
            order_price.append(item_price)
            order_cost += item_price

        elif plate_type == "F":
            item_price = float(full_price[id_item - 1] * item_quantity)
            order_price.append(item_price)
            order_cost += item_price

        print("Item Added to order -> Item_Number: " + str(id_item) + "\tPlate_type: " +
              str(plate_type) + "\tQuantity: " + str(item_quantity) + "\n")

    tip_choice = int(input(
        "\nKindly choose the tip% you'd be providing us with: \n1 -> 0%\n2 -> 10%\n3 -> 20%\n"))

    tip_percent = 0.00

    if tip_choice == 2:
        tip_percent = 0.10
    elif tip_choice == 3:
        tip_percent = 0.20

    total_amt = order_cost + (order_cost * tip_percent)

    print("\nTotal amount -> " + '%.2f' % total_amt + "\t (Tip inclusive)")

    party_size = int(
        input("\nEnter the number of people, among which bill is to be split: "))
    share = total_amt/party_size
    print("\nContribution of each person comes out to be : " + '%.2f' % share)

    print("\n<<<<\t\t TEST YOUR LUCK \t\t>>>>\n")
    print("This is a limited time event..💫 You could avail huge discounts..💸")

    choice = input(
        "\nEnter 'Y' to participate and 'N' to loose by not participating : ")
    discount_percent = 0.0
    dis_increase = 0.0

    if choice == "Y":
        possible_discounts = [-0.50, -0.25, -0.25, -0.10, -0.10, -0.10, 0.0, 0.0,
                              0.0, 0.0, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20]
        luck_factor = randint(0, 19)
        discount_percent = possible_discounts[luck_factor]

        if discount_percent == 0.0 or discount_percent == 0.20:
            print("\n **** \n*    *\n*    *\n*    *\n*    *\n **** ")
            print("\nOops.. Today is not your lucky day")
        else:
            print(
                "\n **** \t\t **** \n|    |\t\t|    |\n|    |\t\t|    |\n|    |\t\t|    |\n **** \t\t **** \n")
            print("\t  {}\n\t______")
            print("\nCongratulations on receiving the discount. Lucky You..!")

        dis_increase = total_amt * discount_percent
        total_amt += dis_increase
        print("\nBased on your luck, your discounted/increased value is -> " +
              '%.2f' % dis_increase)

    for i in range(0, len(order_ids), 1):
        for j in range(i+1, len(order_ids), 1):
            if order_ids[i] != -1 and order_ids[i] == order_ids[j] and order_type[i] == order_type[j]:
                order_ids[j] = - 1
                order_price[i] = order_price[i] + order_price[j]
                order_quantity[i] = order_quantity[i] + order_quantity[j]
                order_price[j] = 0
                order_quantity[j] = 0

    item_list = str("")

    for item in range(len(order_ids)):
        id_item = str(order_ids[item])
        # print(id_item)
        if id_item == "-1":
            continue
        else:
            item_list += id_item + " "
            quantity_item = str(order_quantity[item])
            plate_type_item = order_type[item]
            type_of_plate = ""
            if plate_type_item == "H":
                type_of_plate = "HALF"
                item_list += type_of_plate
            else:
                type_of_plate = "FULL"
                item_list += type_of_plate
            price_item = str('%.2f' % order_price[item])
            print("Item " + id_item + "[" + type_of_plate +
                  "]" + "[" + quantity_item + "]: " + price_item)

    print("\nTotal: " + '%.2f' % order_cost)
    print("Tip Percentage: " + str(int(tip_percent*100)) + "%")
    print("Discount/Increase: " + '%.2f' % dis_increase)
    print("Final Total: " + '%.2f' % total_amt)

    share = total_amt/party_size
    print("Updated share per head: " + '%.2f' % share)
    print("\nThank You..\n")

    temp = {}
    temp['username'] = str(user_name)
    temp['item_id'] = item_list
    temp['total'] = '%.2f' % order_cost
    temp['tip_percent'] = str(int(tip_percent*100))
    temp['dis_inc'] = '%.2f' % dis_increase
    temp['final_total'] = '%.2f' % total_amt
    temp['updated_share_per_head'] = '%.2f' % share

    data = json.dumps(temp)
    final_url = local_url + "/add/transaction"
    response = requests.post(final_url, json=data).content.decode("ascii")
    print(response)

# ---------------------------------------------------------------------------------------------------------------


print("\n<<<<<<\t\tWelcome to SSD Restaurant..!\t\t>>>>>>\n\n")

print("Enter 1 -> SIGN UP")
print("Enter 2 -> LOGIN")
print("Enter 9 -> EXIT\n")

choice = int(input("Option : "))
count = 0

while(choice != 9):

    if(count != 0):
        print("\nEnter 1 -> SIGN UP")
        print("Enter 2 -> LOGIN")
        print("Enter 9 -> EXIT\n")
        choice = int(input("Option : "))

    if(choice == 1):
        count += 1
        print("\nEnter 1 -> Sign Up as CUSTOMER")
        print("Enter 2 -> Sign Up as CHEF\n")

        option = int(input("Option: "))

        if(option == 1):
            print("\nCUSTOMER Sign Up")
            user_name = input("Enter User Name : ")
            password = input("Enter Password : ")
            to_send = {}
            to_send['user_name'] = user_name
            to_send['password'] = password
            data = json.dumps(to_send)
            final_url = local_url + "customer/signup"
            response = requests.post(
                final_url, json=data).content.decode("ascii")
            print(response)

        elif(option == 2):
            print("\nCHEF Sign Up")
            user_name = input("Enter User Name : ")
            password = input("Enter Password : ")
            to_send = {}
            to_send['user_name'] = user_name
            to_send['password'] = password
            data = json.dumps(to_send)
            final_url = local_url + "chef/signup"
            response = requests.post(
                final_url, json=data).content.decode("ascii")
            print(response)

    if(choice == 2):
        count += 1
        print("\nEnter 1 -> Login as CUSTOMER")
        print("Enter 2 -> Login as CHEF\n")

        option = int(input("Option: "))
        if(option == 1):
            print("\nCUSTOMER Login")
            user_name = input("Enter User Name : ")
            password = input("Enter Password : ")
            to_send = {}
            to_send['user_name'] = user_name
            to_send['password'] = password

            data = json.dumps(to_send)
            final_url = local_url + "customer/login"
            user_session = requests.Session()
            response = user_session.post(
                final_url, json=data).content.decode("ascii")
            print(response)

            response = str(response)
            if "LOGGED" in response:
                while (True):
                    print("\nEnter 1 -> View Menu")
                    print("Enter 2 -> Order Items")
                    print("Enter 3 -> View Transactions")
                    print("Enter 4 -> Logout\n")

                    entered_choice = int(input("Option : "))

                    if(entered_choice == 1):
                        final_url = local_url + "menu"
                        response = requests.get(final_url).json()
                        print("")
                        print('{:^10} {:^15} {:^15}'.format(
                            "Item_No", "Half_Plate", "Full_Plate"))
                        for row in response:
                            print('{:^10} {:^15} {:^15}'.format(
                                str(row["id"]), str(row["half"]), str(row["full"])))

                    elif(entered_choice == 2):
                        final_url = local_url + "menu"
                        response = requests.get(final_url).json()
                        print('{:^10} {:^15} {:^15}'.format(
                            "Item_No", "Half_Plate", "Full_Plate"))
                        for row in response:
                            # print((row))
                            print('{:^10} {:^15} {:^15}'.format(
                                str(row["id"]), str(row["half"]), str(row["full"])))
                        place_order(user_name, response)  # assignment 3A

                    elif(entered_choice == 3):
                        temp = {}
                        temp['user_name'] = user_name
                        data = json.dumps(temp)
                        final_url = local_url + "list/transactions"
                        response = requests.get(
                            final_url, json=data).json()
                        print('{:^10} {:^15}'.format(
                            "Txn_no", "Total_Paid"))
                        for row in response:
                            print('{:^10} {:^15}'.format(
                                str(row["txn_num"]), str(row["final_total"])))

                        choice = input(
                            "Enter 'Y' to know the details of any transactions, else 'N' : ")

                        if(choice == "Y"):
                            txn_num = int(
                                input("Enter the Transaction number to view bill-details : "))
                            temp = {}
                            temp['transactionNumber'] = txn_num
                            data = json.dumps(temp)
                            final_url = local_url + "bill"
                            response = requests.get(
                                final_url, json=data).json()
                            print('{:^10} {:^15} {:^15} {:^15} {:^15} {:^15} {:^15}'.format(
                                "Txn_no", "User_name", "Total", "Tip_Percent", "Final_Total", "Disc/Inc", "Share_per_head"))
                            for row in response:
                                print('{:^10} {:^15} {:^15} {:^15} {:^15} {:^15} {:^15}'.format(
                                    str(row["txn_num"]), str(row["username"]), str(row["total"]), str(
                                        row["tip"]), str(row["final_total"]), str(row["dis_inc"]), str(row["share"])))
                        else:
                            continue

                    elif(entered_choice == 4):
                        final_url = local_url + "customer/signout"
                        response = requests.get(
                            final_url).content.decode("ascii")
                        print(response)
                        break

        if(option == 2):
            print("\nCHEF Login")
            user_name = input("Enter User Name : ")
            password = input("Enter Password : ")
            to_send = {}
            to_send['user_name'] = user_name
            to_send['password'] = password
            to_send['is_chef'] = 1

            data = json.dumps(to_send)
            final_url = local_url + "chef/login"
            user_session = requests.Session()
            response = user_session.post(
                final_url, json=data).content.decode("ascii")
            print(response)

            response = str(response)
            if "LOGGED" in response:
                while(True):
                    print("\nEnter 1 -> View Menu")
                    print("Enter 2 -> Order Items")
                    print("Enter 3 -> View Transactions")
                    print("Enter 4 -> Add New Items to Menu")
                    print("Enter 5 -> Logout\n")

                    entered_choice = int(input("Option : "))

                    if(entered_choice == 1):
                        final_url = local_url + "menu"
                        response = requests.get(final_url).json()
                        print("")
                        print('{:^10} {:^15} {:^15}'.format(
                            "Item_No", "Half_Plate", "Full_Plate"))
                        for row in response:
                            print('{:^10} {:^15} {:^15}'.format(
                                str(row["id"]), str(row["half"]), str(row["full"])))

                    elif(entered_choice == 2):
                        final_url = local_url + "menu"
                        response_send = requests.get(final_url).content
                        response = requests.get(final_url).json()
                        print("")
                        print('{:^10} {:^15} {:^15}'.format(
                            "Item_No", "Half_Plate", "Full_Plate"))
                        for row in response:
                            print('{:^10} {:^15} {:^15}'.format(
                                str(row["id"]), str(row["half"]), str(row["full"])))
                        place_order(user_name, response_send)  # assignment 3A

                    elif(entered_choice == 3):
                        temp = {}
                        temp['user_name'] = user_name
                        data = json.dumps(temp)
                        final_url = local_url + "list/transactions"
                        response = requests.get(
                            final_url, json=data).json()
                        print('{:^10} {:^15}'.format(
                            "Txn_no", "Total_Paid"))
                        for row in response:
                            print('{:^10} {:^15}'.format(
                                str(row["txn_num"]), str(row["final_total"])))

                        choice = input(
                            "Enter 'Y' to know the details of any transactions, else 'N' : ")

                        if(choice == "Y"):
                            txn_num = int(
                                input("Enter the Transaction number to view bill-details : "))
                            temp = {}
                            temp['transactionNumber'] = txn_num
                            data = json.dumps(temp)
                            final_url = local_url + "bill"
                            response = requests.get(
                                final_url, json=data).json()
                            print('{:^10} {:^15} {:^15} {:^15} {:^15} {:^15} {:^15}'.format(
                                "Txn_no", "User_name", "Total", "Tip_Percent", "Final_Total", "Disc/Inc", "Share_per_head"))
                            for row in response:
                                print('{:^10} {:^15} {:^15} {:^15} {:^15} {:^15} {:^15}'.format(
                                    str(row["txn_num"]), str(row["username"]), str(row["total"]), str(
                                        row["tip"]), str(row["final_total"]), str(row["dis_inc"]), str(row["share"])))
                        else:
                            continue

                    elif(entered_choice == 4):
                        choice = input(
                            "Enter 'Y' to add new item, else 'N' to stop : ")

                        if(choice == "Y"):
                            item_no = int(input("Enter Item Number : "))
                            half_price = int(
                                input("Enter Price of Half Plate : "))
                            full_price = int(
                                input("Enter Price of Full Plate : "))
                            temp = {}
                            temp['item_id'] = item_no
                            temp['half'] = half_price
                            temp['full'] = full_price

                            data = json.dumps(temp)
                            final_url = local_url + "add/menu"
                            response = user_session.post(
                                final_url, json=data).content.decode("ascii")
                            print(response)

                    elif(entered_choice == 5):
                        final_url = local_url + "chef/signout"
                        response = requests.get(
                            final_url).content.decode("ascii")
                        print(response)
                        break

    if(choice == 9):
        count += 1
        break

print("<<-- Bye -->>")
