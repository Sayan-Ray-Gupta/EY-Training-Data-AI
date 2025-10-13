import pandas as pd
from datetime import datetime


def invertory_pipeline():
    df = pd.read_csv("inventory.csv")

    #added restock
    df['RestockNeeded'] = df.apply(lambda row: "Yes" if row["Quantity"] < row["ReorderLevel"] else "No", axis=1)

    #added 'TotalValue Column
    df["TotalValue"] = df["Quantity"] * df["PricePerUnit"]

    #load
    df.to_csv("inventory_report.csv", index=False)

    print(f"Invertory Pipeline completed at {datetime.now()}")


if __name__ == "__main__":
    invertory_pipeline()