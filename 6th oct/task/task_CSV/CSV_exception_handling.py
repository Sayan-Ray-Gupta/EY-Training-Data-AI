import csv
import logging
import pandas as pd

logging.basicConfig(filename="sales.log",
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
    # read the data
    df = pd.read_csv('products.csv')
    print(df.head())

    # total sales of each item
    for index, row in df.iterrows():
        product = row['product']
        price = row['price']
        quantity = row['quantity']

        total_sales = price * quantity
        print(f" {product} = {total_sales}")
        logging.info(f" {product} = {total_sales}")

except FileNotFoundError as e:
    logging.error("File not found")
    print("File not found")

except TypeError as e:
    logging.error("Invalid Numerical value")
    print("Invalid Numerical value")