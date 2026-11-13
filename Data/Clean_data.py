import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

df = pd.read_sql("SELECT * FROM online_retail", engine)
print("Raw rows:", len(df))

df = df.dropna(subset=["customer_id"])
print("After removing missing customer IDs:", len(df))

df = df[~df["invoice_no"].str.startswith("C")]
print("After removing cancelled orders:", len(df))

df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
print("After removing zero/negative quantity or price:", len(df))

df = df.drop_duplicates()
print("After removing duplicates:", len(df))

df["customer_id"] = df["customer_id"].astype(int)
df["total_price"] = df["quantity"] * df["unit_price"]

df.to_sql("retail_clean", engine, if_exists="replace",
          index=False, chunksize=10000, method="multi")
print("Clean table saved:", len(df), "rows")