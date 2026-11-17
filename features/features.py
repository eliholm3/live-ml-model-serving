import pandas as pd

def extract():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/refs/heads/master/titanic.csv"
    data = pd.read_csv(url)
    return data


def panda_clean(data):
    cleaned = data[["PassengerId", "Name", "Sex", "Age", "Survived", "Fare"]].dropna().copy()
    cleaned["Sex"] = cleaned["Sex"].map({"male": 0, "female": 1})
    cleaned = cleaned.rename(columns={"PassengerId": "passenger_id"})
    return cleaned


if __name__ == "__main__":
    data = extract()
    cleaned_data = panda_clean(data)
    print(cleaned_data.head(20))