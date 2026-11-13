import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

df = pd.read_csv("Data/Online_Retail.csv", encoding="latin1")
print(len(df))
print(df.head())

# rename columns
df.columns = ["invoice_no", "stock_code", "description", "quantity",
              "invoice_date", "unit_price", "customer_id", "country"]

# fix data types
df["invoice_no"] = df["invoice_no"].astype(str)
df["stock_code"] = df["stock_code"].astype(str)
df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%m/%d/%y %H:%M")
df["customer_id"] = df["customer_id"].astype("Int64")

print("Loading into PostgreSQL, please wait...")

df.to_sql("online_retail", engine, if_exists="replace",
          index=False, chunksize=10000, method="multi")
print("Data loaded")

with engine.connect() as conn:
    print(conn.execute(text("SELECT COUNT(*) FROM online_retail")).scalar())