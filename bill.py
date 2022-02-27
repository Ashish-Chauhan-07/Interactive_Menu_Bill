import csv
from random import randint, random

print("<<<<<<\t\tWelcome to SSD Restaurant..!\t\t>>>>>\n\nHere is our menu : \n")

data = []
item_num = []
half_price = []
full_price = []

with open("Menu.csv", 'r') as menu:
    csvreader = csv.reader(menu)
    col_names = next(csvreader)

    for row in csvreader:
        data.append(row)
        item_num.append(int(row[0]))
        half_price.append(int(row[1]))
        full_price.append(int(row[2]))

print('{:^10} {:^15} {:^15}'.format(col_names[0], col_names[1], col_names[2]))

for row in data:
    print('{:^10} {:^15} {:^15}'.format(row[0], row[1], row[2]))

print("\nWe are ready to take your orders..\n")

order_ids = []
order_quantity = []
order_type = []
order_price = []
order_cost = 0.00

while(True):
    order_check = input(
        "Enter 'A' to add orders OR Enter 'N' to move ahead : ")
    if order_check == "N":
        break

    id_item = int(
        input("Please enter the Item Number from Menu you wish to order : "))
    order_ids.append(id_item)

    plate_type = input(
        "Should it be Half Plate(Enter 'H') or Full Plate(Enter 'F') : ")
    order_type.append(plate_type)
    item_quantity = int(input("What's the quantity you'd like to order..? : "))
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
        print("\n **** \t\t **** \n|    |\t\t|    |\n|    |\t\t|    |\n|    |\t\t|    |\n **** \t\t **** \n")
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

print("\nHere is the breakdown of your bill :\n")

for item in range(len(order_ids)):
    id_item = str(order_ids[item])
    # print(id_item)
    if id_item == "-1":
        continue
    else:
        quantity_item = str(order_quantity[item])
        plate_type_item = order_type[item]
        type_of_plate = ""
        if plate_type_item == "H":
            type_of_plate = "HALF"
        else:
            type_of_plate = "FULL"
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
