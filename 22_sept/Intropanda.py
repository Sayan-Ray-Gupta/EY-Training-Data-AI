import pandas as pd
import numpy as np
data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha","Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI","ML","Data Science","AI","ML"],
    "Marks": [85, 98, 78, 88, 95],
}

df = pd.DataFrame(data)
# print(df)
# print(df["Name"])
# print(df[["Name","Marks"]])
# print(df.iloc[0]) #first row
# print(df.loc[2,"Marks"]) # values at row 2 , column marks

# #filter data
# high_scorer = df[df["Marks"]>85]
# print(high_scorer)


#Adding & Updating Columns

#add Pass/ Fail columns
df["Result"] = np.where(df["Marks"]>= 80, "Pass", "Fail")

#Update Neha's Marks
df.loc[df["Name"] == "Neha", "Marks"] = 92

print(df)