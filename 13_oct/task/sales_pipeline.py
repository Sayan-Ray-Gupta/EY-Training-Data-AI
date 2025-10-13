import pandas as pd
from datetime import datetime


def run_sales_pipeline():
    #Extracting data
    product = pd.read_csv("Products_3rdTask.csv")
    customers = pd.read_csv("customers_3rdTask.csv")
    orders = pd.read_csv("Orders_3rdTask.csv")

    # Transforming Data
    #Joining Dataset
    merged_df = pd.merge(orders, customers, how="left", left_on="CustomerID", right_on="CustomerID")
    merged_df = pd.merge(merged_df, product, how="left", left_on="ProductID", right_on="ProductID")

    #Merged_df is the completely merged dataset now

    #step 2 : add new calulated columns
    merged_df["TotalAmount"] = merged_df["Quantity"] * merged_df["Price"]
    merged_df["OrderDate"] = pd.to_datetime(merged_df["OrderDate"])
    merged_df["OrderMonth"] = merged_df["OrderDate"].dt.month

    #step 3: filter
    filtered_df = merged_df[(merged_df ["Quantity"] >=2) & (merged_df["Country"].isin(["India","UAE"]))]

    #step 4 : group & aggregate
    category_summary = (
        filtered_df.groupby("Category")["TotalAmount"].sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
    )

    segment_summary = (
        filtered_df.groupby("Segment")["TotalAmount"]
        .sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
    )

    #step 5 Sorting
    customer_revenue = (
        filtered_df.groupby(["CustomerID", "Name"])["TotalAmount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    #Load
    filtered_df.to_csv("processed_orders.csv", index=False)
    category_summary.to_csv("category_summary.csv", index=False)
    segment_summary.to_csv("segment_summary.csv", index=False)
    customer_revenue.to_csv("customer_ranking.csv", index=False)


    print("ETL pipeline completed Successfully")


if __name__ == "__main__":
    run_sales_pipeline()
