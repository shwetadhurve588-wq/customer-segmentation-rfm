import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

result = pd.read_sql(
    "SELECT segment, COUNT(*) AS customers, ROUND(SUM(monetary)::numeric,0) AS revenue "
    "FROM rfm_segments GROUP BY segment ORDER BY revenue DESC", engine)
print(result)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].bar(result["segment"], result["customers"], color="#4C78A8")
ax[0].set_title("Customers per segment")
ax[0].tick_params(axis="x", rotation=30)

ax[1].pie(result["revenue"], labels=result["segment"], autopct="%1.0f%%")
ax[1].set_title("Revenue share by segment")

plt.tight_layout()
plt.savefig("dashboard/segments.png", dpi=150)
plt.show()