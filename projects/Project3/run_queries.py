import sqlite3
from pathlib import Path

import pandas as pd

# Paths
data_path = Path("Data/cleanedEDA.csv")
db_path = Path("orders.db")
sql_path = Path("sql_queries.sql")
results_path = Path("results.txt")

# Create database and load data
print("Loading data into SQLite database...")
conn = sqlite3.connect(db_path)

# Read CSV and create table
df = pd.read_csv(data_path)
df.to_sql('orders', conn, if_exists='replace', index=False)

print(f"✓ Loaded {len(df)} records into database\n")

# Read SQL queries
with open(sql_path, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Split queries (each query separated by -- ====)
queries = []
current_query = []
for line in sql_content.split('\n'):
    if line.strip().startswith('-- ====') and current_query:
        queries.append('\n'.join(current_query))
        current_query = []
    elif line.strip() and not line.strip().startswith('--'):
        current_query.append(line)

if current_query:
    queries.append('\n'.join(current_query))

# Execute queries and collect results
results = []
query_titles = [
    "QUERY 1: Product revenue analysis",
    "QUERY 2: Order status distribution",
    "QUERY 3: Payment method analysis",
    "QUERY 4: Monthly sales trend",
    "QUERY 5: Top customers by spending",
    "QUERY 6: Outlier detection using WHERE clause",
    "QUERY 7: HAVING clause example - Filtering after GROUP BY",
    "QUERY 8: Combined analysis - Popular products status breakdown",
    "QUERY 9: Referral source effectiveness analysis",
    "QUERY 10: Overall statistics"
]

print("Executing SQL queries...")
print("=" * 80)

for i, query in enumerate(queries):
    if query.strip():
        try:
            result_df = pd.read_sql_query(query, conn)
            title = query_titles[i] if i < len(query_titles) else f"QUERY {i+1}"
            
            results.append(f"\n{'='*80}")
            results.append(f"{title}")
            results.append(f"{'='*80}\n")
            results.append(result_df.to_string(index=False))
            results.append("\n")
            
            print(f"✓ {title}")
            print(result_df.to_string(index=False))
            print("\n" + "="*80 + "\n")
            
        except Exception as e:
            results.append(f"\nERROR in Query {i+1}: {str(e)}\n")
            print(f"✗ Error in Query {i+1}: {str(e)}\n")

# Write results to file
with open(results_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print(f"\n✓ Results saved to {results_path}")

# Close connection
conn.close()

print("\n✓ All queries executed successfully!")
