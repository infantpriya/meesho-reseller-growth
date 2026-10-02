import sqlite3
import csv
import sys

DB_PATH = "data/meesho_reseller.db"
SQL_PATH = "part1_sql/queries.sql"

OUTPUT_FILES = {
    "1": "part1_sql/output/monthly_category_revenue.csv",
    "2": "part1_sql/output/region_revenue.csv",
    "3": "part1_sql/output/top_resellers.csv",
     "4": "part1_sql/output/zero_order_resellers.csv",
     "5": "part1_sql/output/june_delivered_aov.csv",
}


def run_query(query_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SQL_PATH, "r", encoding="utf-8") as f:
        sql = f.read()

    # Split the SQL file into individual queries
    queries = [
        query.strip()
        for query in sql.split(";")
        if query.strip()
    ]

    sql_query = queries[query_number - 1]

    cursor.execute(sql_query)

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    output_path = OUTPUT_FILES[str(query_number)]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    conn.close()

    print(f"Saved {len(rows)} rows to {output_path}")


if len(sys.argv) != 2:
    print("Usage: python part1_sql\\run_query.py <query_number>")
    print("Example: python part1_sql\\run_query.py 1")
    sys.exit(1)

run_query(int(sys.argv[1]))