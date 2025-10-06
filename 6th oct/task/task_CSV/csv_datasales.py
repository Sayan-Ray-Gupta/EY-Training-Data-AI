import pandas as pd

# Create the data
data = {
    "product": ["Laptop", "Mouse", "Keyboard"],
    "price": [70000, 500, 1200],
    "quantity": [2, 5, 3]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("products.csv", index=False)

print("CSV file 'products.csv' has been created.")