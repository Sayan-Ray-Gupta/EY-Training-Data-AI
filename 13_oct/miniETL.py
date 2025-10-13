import pandas as pd

#step 1 Extract the data -Read the csv

df = pd.read_csv("students.csv")


#step 2: Transform - Clean and calculate
df.dropna(inplace=True)  #remove missing values
df["Marks"] = df["Marks"].astype(int)
df["Result"] = df["Marks"].apply(lambda x: "pass" if x > 50 else "fail")


#step 3 Load - Saving the transformed data

df.to_csv("cleasned_students.csv", index=False)

print("Data pipeline is completed. Cleaned data saved as cleaned_students")