import csv
import random
import pandas as pd # type: ignore
import numpy as np  # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.metrics import mean_squared_error, r2_score  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore
import pickle 

class Product:
    def __init__(self, id, name, price, quantity, category):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

def add_product(products, id, name, price, quantity, category):
    products.append(Product(id, name, price, quantity, category))

def remove_product(products, id):
    for product in products:
        if product.id == id:
            products.remove(product)
            return True
    return False

def find_product_by_id(products, id):
    for product in products:
        if product.id == id:
            return product
    return None

def update_product(products, id, new_name, new_price, new_quantity, new_category):
    product = find_product_by_id(products, id)
    if product:
        product.name = new_name
        product.price = new_price
        product.quantity = new_quantity
        product.category = new_category
        return True
    return False

def show_products(products):
    for product in products:
        print(f"ID: {product.id}\n"
              f"Name: {product.name}\n"
              f"Price: ${product.price}\n"
              f"Quantity: {product.quantity}\n"
              f"Category: {product.category}\n"
              f"-------------------------\n")

def add_to_cart(cart, product):
    cart.append(product)

def place_order(cart):
    total = 0.0
    for product in cart:
        total += product.price * product.quantity
        print(f"Product: {product.name}, Quantity: {product.quantity}, Price: ${product.price}")
    print(f"Total: ${total}")

def recommend_products(products, viewed_product, num_recommendations=5):
    # Find other items in the same category as the viewed item
    recommendations = [product for product in products if product.category == viewed_product.category and product.id != viewed_product.id]

    # Randomly select 5 items from the recommendations (if available/Otherwise show out of stock)
    if len(recommendations) >= num_recommendations:
        recommendations = random.sample(recommendations, num_recommendations)
    else:
        recommendations = recommendations[:num_recommendations]

    return recommendations

def main():
    products = []

    # Adding some initial items
    add_product(products, 1, "Sony TV", 999.99, 50, "Electronics")
    add_product(products, 2, "Apple Watch", 299.99, 100, "Electronics")
    add_product(products, 3, "Bottle", 9.99, 200, "Household")
    add_product(products, 4, "Laptop", 1299.99, 30, "Electronics")
    add_product(products, 5, "Headphones", 99.99, 150, "Electronics")
    add_product(products, 6, "Blender", 49.99, 75, "Household")
    add_product(products, 7, "Camera", 499.99, 40, "Electronics")
    add_product(products, 8, "Smartphone", 699.99, 80, "Electronics")
    add_product(products, 9, "Microwave", 89.99, 60, "Household")
    add_product(products, 10, "Desk Lamp", 19.99, 90, "Household")

    show_products(products)  # Show the initial items

    viewed_product = find_product_by_id(products, 1)  

    if viewed_product:
        print(f"Recommendations for {viewed_product.name}:")
        recommendations = recommend_products(products, viewed_product)
        for rec in recommendations:
            print(f"- {rec.name} (${rec.price})")

    with open("product.csv", "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Transactions", "Conflicts", "ConflictPercentage"])

        # Generating test data
        for transactions in range(200, 5001, 500):
            conflicts = 0
            for _ in range(transactions):
                operation = random.randint(0, 3)
                id = random.randint(0, 999)

                if operation == 0:  # Add item
                    name = "product " + str(id)
                    price = random.randint(1, 100) + 1.0
                    quantity = random.randint(1, 10)
                    category = random.choice(["Electronics", "Household", "Clothing"])
                    add_product(products, id, name, price, quantity, category)
                elif operation == 1:  # Remove item
                    if not remove_product(products, id):
                        conflicts += 1
                elif operation == 2:  # Update item
                    item = find_product_by_id(products, id)
                    if item:
                        name = "Updated product " + str(id)
                        price = random.randint(1, 100) + 1.0
                        quantity = random.randint(1, 10)
                        category = random.choice(["Electronics", "Household", "Clothing"])
                        update_product(products, id, name, price, quantity, category)
                    else:
                        conflicts += 1
                elif operation == 3:  # Add to cart
                    product = find_product_by_id(products, id)
                    if product:
                        cart = []
                        add_to_cart(cart, product)
                        place_order(cart)
                    else:
                        conflicts += 1

            conflict_percentage = (conflicts / transactions) * 100.0
            writer.writerow([transactions, conflicts, conflict_percentage])


if __name__ == "__main__":
    main()
