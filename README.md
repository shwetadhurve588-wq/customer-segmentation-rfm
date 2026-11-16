# Who Are the Customers Worth Keeping?
### RFM customer segmentation on 392,692 retail transactions

**Stack:** PostgreSQL · SQL · Python (pandas, SQLAlchemy) · Power BI

![Dashboard](dashboard/dashboard.png)

---

## The short version

A UK online retailer sends the same offers to everyone. I split its 4,338 identifiable customers into six segments based on how recently, how often and how much they buy.

> **22% of customers (Champions) bring in 64.5% of revenue.**
> Champions and Loyal customers together are 44.5% of the base and **79.8% of revenue**.

The best place to spend win-back budget is the **At Risk** group, not the Lost group.

---

## The business question

How should a retailer split its marketing budget when customers are very different in value?

Sending one offer to everyone wastes money on people who rarely buy, and under-rewards the people who keep the business running. RFM analysis gives each customer a score for:

| Letter | Measure | How I calculated it |
|---|---|---|
| **R** | Recency | Days since the customer's last order |
| **F** | Frequency | Number of distinct orders |
| **M** | Monetary | Total spend (£) |

---

## What I found

| Segment | Customers | Share of customers | Revenue (£) | Share of revenue | Avg spend (£) |
|---|---|---|---|---|---|
| Champions | 947 | 21.8% | 5,730,403 | **64.5%** | ~6,051 |
| Loyal Customers | 985 | 22.7% | 1,359,260 | 15.3% | ~1,380 |
| At Risk | 670 | 15.4% | 849,783 | 9.6% | ~1,268 |
| Lost | 1,066 | 24.6% | 495,535 | 5.6% | ~465 |
| New / Promising | 312 | 7.2% | 287,385 | 3.2% | ~921 |
| Potential Loyalists | 358 | 8.3% | 164,843 | 1.9% | ~460 |

**Five things worth noticing**
1. A Champion spends about **13x** more than a Lost customer and **4.4x** more than a Loyal one.
2. The Lost group is the largest (24.6%) but adds only 5.6% of revenue.
3. At Risk customers average £1,268, close to Loyal customers, and have already spent £849,783 in total.
4. Losing even a small share of Champions would hurt more than losing all the Lost customers.
5. New / Promising customers already spend about £921 each, which is a strong start.

---

## What I would do about it

| Segment | Action | Why |
|---|---|---|
| Champions | Early access, loyalty rewards, referral program | Protect the revenue core |
| Loyal Customers | Bundles and upsell offers | There is a 4.4x spend gap to Champions |
| At Risk | Personalized win-back email with a time-limited offer | Best return on marketing spend |
| New / Promising | Welcome series and second-purchase offer | Convert early momentum into habit |
| Potential Loyalists | Product recommendations | Low-cost way to raise frequency |
| Lost | One cheap reactivation email, then stop | Low value per customer |

---

## How I built it

```
CSV  →  Python loads into PostgreSQL  →  Python cleans  →  SQL builds RFM  →  Power BI dashboard
```

**1. Load.** `Data/Load_data.py` reads the CSV, fixes data types and writes 541,909 rows to the `online_retail` table.

**2. Clean.** `Data/Clean_data.py` produces the `retail_clean` table:

| Step | Rows left | Removed |
|---|---|---|
| Raw data | 541,909 | n/a |
| Missing Customer ID | 406,829 | 135,080 |
| Cancelled orders (invoice starts with "C") | 397,924 | 8,905 |
| Zero or negative quantity or price | 397,884 | 40 |
| Duplicate rows | 392,692 | 5,192 |

It also adds `total_price = quantity × unit_price`. Rows with no Customer ID can't be tracked across orders, so they can't be segmented.

**3. Score.** `sql/rfm_queries.sql` builds `rfm`, `rfm_scores` and `rfm_segments`. Each metric gets a 1–5 score with `NTILE(5)`, and segment rules are applied on the scores.

**4. Visualize.** The Power BI dashboard (`dashboard/customer_segmentation.pbix`) shows KPI cards, segment size, revenue share, average spend, and an insight table.

---

## Data

- **Online Retail dataset** (UCI Machine Learning Repository / Kaggle)
- UK online retailer, 1 Dec 2010 to 9 Dec 2011
- 541,909 rows, 8 columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
- The CSV is not included in this repository. Download it and save it as `Data/Online_Retail.csv`.

---

## Limits of this analysis

- About 25% of raw rows had no Customer ID, so the results describe identified customers only.
- The data spans roughly one year, so seasonality can affect Recency scores.
- The segment rules are my own choices. Different cutoffs would change segment sizes.
- The data is from 2010–2011 and may not match current buying behavior.

---

## Getting Started

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.10+ | Tested on 3.13 |
| PostgreSQL | 14+ | Includes pgAdmin |
| Power BI Desktop | Latest | Only needed to open the dashboard |

### 1. Clone the repository

```bash
git clone https://github.com/shwetadhurve588-wq/customer-segmentation-rfm.git
cd customer-segmentation-rfm
```

### 2. Install dependencies

```bash
pip install pandas sqlalchemy psycopg2-binary matplotlib python-dotenv
```

### 3. Get the data

Download the **Online Retail** dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/) or Kaggle. Save it as:

```
Data/Online_Retail.csv
```

The raw file is excluded from this repository through `.gitignore`.

### 4. Configure the database

Create an empty database in PostgreSQL:

```sql
CREATE DATABASE retail_db;
```

Copy the environment template and enter your own credentials:

```bash
cp .env.example .env        # Windows PowerShell: Copy-Item .env.example .env
```

| Variable | Description | Example |
|---|---|---|
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | Your password | `your_password` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` (check yours in pgAdmin) |
| `DB_NAME` | Database name | `retail_db` |

### 5. Run the pipeline

Run every command from the project root folder.

| Step | Command | What it does | Expected result |
|---|---|---|---|
| 1 | `python Data/Load_data.py` | Loads the raw CSV into `online_retail` | 541,909 rows loaded |
| 2 | `python Data/Clean_data.py` | Cleans the data into `retail_clean` | 392,692 rows saved |
| 3 | Run `sql/rfm_queries.sql` in pgAdmin | Builds `rfm`, `rfm_scores` and `rfm_segments` | 4,338 customers segmented |
| 4 | `python Data/rfm.py` | Prints the segment summary and saves `dashboard/segments.png` | Six segments listed |

### 6. View the dashboard

Open `dashboard/customer_segmentation.pbix` in Power BI Desktop. If the data source cannot connect, go to **Transform data, Data source settings** and update the server (for example `localhost:5432`) and the database name.

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `Connection refused` | Wrong port or PostgreSQL is stopped | Check the port in pgAdmin and update `DB_PORT` in `.env` |
| `password authentication failed` | Wrong credentials in `.env` | Correct `DB_PASSWORD` and save the file |
| `relation "rfm_segments" does not exist` | SQL step was skipped | Run `sql/rfm_queries.sql` before `rfm.py` |
| `FileNotFoundError` for the CSV | Wrong file name or location | Save the dataset as `Data/Online_Retail.csv` |
| `ModuleNotFoundError` | Package missing | Re-run the install command in step 2 |

---

## Repository layout

```
├── Data/
│   ├── Load_data.py
│   ├── Clean_data.py
│   └── rfm.py
├── sql/
│   └── rfm_queries.sql
├── dashboard/
│   ├── customer_segmentation.pbix
│   ├── dashboard.png
│   ├── segments.png
│   └── Figure_1.png
├── .env.example
├── .gitignore
└── README.md
```

---

**Shweta Dhurve** · [LinkedIn](www.linkedin.com/in/shweta-dhurve-94b894210) · [GitHub](https://github.com/shwetadhurve588-wq)
