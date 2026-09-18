import csv
import os


def load_transactions():
    # Project ke root folder ka path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # CSV file ka path
    csv_path = os.path.join(base_dir, "data", "transactions.csv")

    transactions = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["amount"] = float(row["amount"])
            transactions.append(row)

    return transactions


if __name__ == "__main__":
    data = load_transactions()

    print(f"Total transactions loaded: {len(data)}")
    print("\nFirst transaction:")
    print(data[0])