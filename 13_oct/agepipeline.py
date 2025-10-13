import pandas as pd
from datetime import datetime

def customers_pipeline():
    df = pd.read_csv("customers1.csv")
    df= df[df['Age']>=20]

    def tagged_age(age):
        if age>30:
            return "young"
        elif age < 50:
            return "adult"
        else :
            return "senior"

    df["AgeGroup"] = df['Age'].apply(tagged_age)


    df.to_csv("customer_report.csv", index=False)
    print(f"Pipeline completed at {datetime.now()}")


if __name__ == "__main__":
    customers_pipeline()