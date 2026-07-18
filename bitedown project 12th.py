#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 22:29:49 2026

@author: ashumendiratta
"""

import os
import pickle
import datetime

# CONSTANTS 
TAX_RATE = 0.08
BIRTHDAY_DISCOUNT = 0.10

USERS_FILE = "users.dat"
MENU_FILE = "menu.txt"

# MENU CREATION 
def create_menu_file():
    menu_text = """STARTERS
1 Tomato Basil Soup - 120
2 Sweet Corn Soup - 130
3 Classic French Fries - 110
4 PeriPeri Fries - 140
5 Garlic Bread - 130
6 Cheese Garlic Bread - 160
7 Veg Spring Rolls - 150
8 Chicken Spring Rolls - 180
9 Crispy Chilli Baby Corn - 180
10 Chicken Popcorn - 200

SALADS
11 Garden Fresh Salad - 160
12 Caesar Salad Veg - 180
13 Caesar Salad Chicken - 220
14 Greek Salad - 200
15 Protein Bowl Veg - 210

MAIN COURSE – INDIAN
16 Paneer Butter Masala - 240
17 Kadai Paneer - 230
18 Dal Tadka - 170
19 Dal Makhani - 200
20 Butter Chicken - 290
21 Chicken Tikka Masala - 300
22 Jeera Rice - 140
23 Veg Biryani - 220
24 Chicken Biryani - 280
25 Tandoori Roti - 20
26 Butter Naan - 40

MAIN COURSE – CONTINENTAL
27 Veg Alfredo Pasta - 240
28 Chicken Alfredo Pasta - 280
29 Veg Arrabbiata Pasta - 230
30 Margherita Pizza - 260
31 Farmhouse Pizza - 320
32 BBQ Chicken Pizza - 360
33 Grilled Veg Sandwich - 150
34 Chicken Club Sandwich - 190
35 Veg Burger - 160
36 Chicken Burger - 190

SNACKS & SIDES
37 Nachos with Salsa - 150
38 Cheese Nachos - 180
39 Veg Momos - 130
40 Chicken Momos - 160

DESSERTS
41 Chocolate Brownie - 140
42 Choco Lava Cake - 150
43 Gulab Jamun - 90
44 Ice Cream Scoop - 70
45 Fruit Salad with Ice Cream - 120

DRINKS
46 Mineral Water - 20
47 Fresh Lime Soda - 80
48 Cold Coffee - 120
49 Iced Tea - 110
50 Classic Milkshake - 140
"""
    with open(MENU_FILE, "w") as f:
        f.write(menu_text)

#LOAD / SAVE USERS
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "wb") as f:
        pickle.dump(users, f)

# USER FUNCTIONS 
def register_user():
    name = input("Enter name: ")
    address = input("Enter address: ")
    birthday = input("Enter birthday (MM/DD/YYYY): ")
    return {
        "address": address,
        "birthday": birthday,
        "orders": []
    }

def login(users):
    name = input("Enter your name: ")
    if name not in users:
        print("New user registered.")
        users[name] = register_user()
        save_users(users)
    return name

# MENU HANDLING 
def load_menu_dict():
    menu = {}
    with open(MENU_FILE, "r") as f:
        for line in f:
            if line.strip() and line[0].isdigit():
                parts = line.split("-")
                left = parts[0].split()
                item_no = int(left[0])
                item_name = " ".join(left[1:])
                price = int(parts[1].strip())
                menu[item_no] = (item_name, price)
    return menu

def show_menu():
    with open(MENU_FILE, "r") as f:
        print(f.read())

# ORDER SYSTEM
def place_order(menu, user, users):
    order = {}

    while True:
        show_menu()
        choice = input("Enter item number (or 'done'): ")

        if choice == "done":
            break

        item_no = int(choice)
        if item_no in menu:
            qty = int(input("Quantity: "))
            order[item_no] = order.get(item_no, 0) + qty
        else:
            print("Invalid item number.")

    if not order:
        return

    subtotal = 0
    for item_no, qty in order.items():
        subtotal += menu[item_no][1] * qty

    discount = 0
    bday_month = int(users[user]["birthday"].split("/")[0])
    if bday_month == datetime.datetime.now().month:
        discount = subtotal * BIRTHDAY_DISCOUNT

    tax = (subtotal - discount) * TAX_RATE
    total = subtotal - discount + tax

    users[user]["orders"].append({
        "date": str(datetime.datetime.now()),
        "total": total
    })

    save_users(users)

    print("\n----- BILL -----")
    for item_no, qty in order.items():
        name, price = menu[item_no]
        print(f"{name} x{qty} = ₹{price * qty}")
    print(f"Subtotal: ₹{subtotal}")
    print(f"Discount: ₹{discount}")
    print(f"Tax: ₹{tax:.2f}")
    print(f"Total: ₹{total:.2f}")

# ------------------ MAIN PROGRAM ------------------
create_menu_file()
users = load_users()
menu = load_menu_dict()

user = login(users)

while True:
    print("\n1. Place Order")
    print("2. View Past Orders")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        place_order(menu, user, users)
    elif choice == "2":
        for o in users[user]["orders"]:
            print(o)
    elif choice == "3":
        break