import pandas as pd

# 1. Load data
df = pd.read_csv("data/raw/data.csv")

# 2. Missing values
df["CouponCode"] = df["CouponCode"].fillna("NoCoupon")

# 3. Remove duplicates (PDF requirement)
df = df.drop_duplicates(subset="OrderID")

# 4. Fix date format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 5. Fix numeric columns
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["TotalPrice"] = pd.to_numeric(df["TotalPrice"], errors="coerce")

# 6. Validate logic
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# 7. Final validation (VERY IMPORTANT)
print("Duplicate OrderID:", df.duplicated(subset="OrderID").sum())
print("Invalid Dates:", df["Date"].isnull().sum())

# 8. Save cleaned data
df.to_csv("data/cleaned/cleaned_data.csv", index=False)
