# Project 3: SQL Data Analysis

## 📊 Overview
This project demonstrates comprehensive SQL query skills including SELECT, WHERE, GROUP BY, aggregations (COUNT, SUM, AVG), ORDER BY, and HAVING clauses. The analysis is performed on an e-commerce orders dataset containing 1,200 transaction records.

## 🎯 Project Objectives
- Demonstrate SQL fundamental concepts
- Perform data aggregation and grouping
- Apply filtering techniques (WHERE vs HAVING)
- Extract business insights from data
- Understand SQL execution order: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`

## 📁 Project Structure
```
Project3/
├── Data/
│   └── cleanedEDA.csv          # Source dataset (1,200 orders)
├── sql_queries.sql             # All SQL queries (10 queries)
├── run_queries.py              # Python script to execute queries
├── results.txt                 # Query execution results
├── summary.txt                 # Business insights and analysis
├── orders.db                   # SQLite database (generated)
└── README.md                   # Project documentation
```

## 🗄️ Database Schema

**Table:** `orders`

| Column | Type | Description |
|--------|------|-------------|
| OrderID | TEXT | Unique order identifier |
| Date | DATE | Order date |
| CustomerID | TEXT | Customer identifier |
| Product | TEXT | Product category |
| Quantity | INTEGER | Number of items |
| UnitPrice | REAL | Price per unit |
| ShippingAddress | TEXT | Delivery address |
| PaymentMethod | TEXT | Payment type |
| OrderStatus | TEXT | Order status |
| TrackingNumber | TEXT | Shipment tracking |
| ItemsInCart | INTEGER | Total items in cart |
| CouponCode | TEXT | Discount coupon used |
| ReferralSource | TEXT | Marketing channel |
| TotalPrice | REAL | Total order value |

## 🔍 SQL Queries Implemented

### 1. Product Revenue Analysis
```sql
SELECT Product, SUM(TotalPrice) AS revenue, COUNT(*) AS order_count
FROM orders
GROUP BY Product
ORDER BY revenue DESC;
```
**Skills:** GROUP BY, SUM, COUNT, ORDER BY

### 2. Order Status Distribution
```sql
SELECT OrderStatus, COUNT(*) AS count, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY OrderStatus;
```
**Skills:** Subquery, Percentage calculation

### 3. Payment Method Analysis
```sql
SELECT PaymentMethod, SUM(TotalPrice) AS revenue, AVG(TotalPrice) AS avg_transaction
FROM orders
GROUP BY PaymentMethod;
```
**Skills:** Multiple aggregations

### 4. Monthly Sales Trend
```sql
SELECT strftime('%Y-%m', Date) AS month, SUM(TotalPrice) AS revenue
FROM orders
GROUP BY month
ORDER BY month;
```
**Skills:** Date manipulation, Time series analysis

### 5. Top Customers
```sql
SELECT CustomerID, SUM(TotalPrice) AS total_spent
FROM orders
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 10;
```
**Skills:** LIMIT clause, Top N queries

### 6. Outlier Detection
```sql
SELECT * FROM orders
WHERE TotalPrice > 3000
ORDER BY TotalPrice DESC;
```
**Skills:** WHERE clause, Filtering

### 7. HAVING Clause Example
```sql
SELECT Product, SUM(TotalPrice) AS revenue
FROM orders
GROUP BY Product
HAVING SUM(TotalPrice) > 50000;
```
**Skills:** HAVING vs WHERE difference

### 8. Combined Analysis
```sql
SELECT Product, OrderStatus, COUNT(*) AS count
FROM orders
WHERE Product IN ('Laptop', 'Phone', 'Monitor')
GROUP BY Product, OrderStatus;
```
**Skills:** Multiple GROUP BY columns, IN operator

### 9. Referral Source Effectiveness
```sql
SELECT ReferralSource, COUNT(*) AS order_count, SUM(TotalPrice) AS revenue
FROM orders
GROUP BY ReferralSource
ORDER BY revenue DESC;
```
**Skills:** Marketing channel analysis

### 10. Overall Statistics
```sql
SELECT COUNT(*) AS total_orders, SUM(TotalPrice) AS total_revenue,
       AVG(TotalPrice) AS avg_order, MIN(TotalPrice), MAX(TotalPrice)
FROM orders;
```
**Skills:** Multiple aggregations without GROUP BY

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pandas
- sqlite3 (built-in with Python)

### Installation
```bash
# Clone the repository
git clone https://github.com/ecemy3/Decolabs-InternShip.git
cd Decolabs-InternShip/Project3

# Install required packages
pip install pandas
```

### Running the Analysis
```bash
# Execute all SQL queries
python run_queries.py
```

This will:
1. Load CSV data into SQLite database
2. Execute all 10 SQL queries
3. Generate `results.txt` with query outputs
4. Display results in terminal

## 📈 Key Findings

### Business Insights
- **Total Revenue:** $1,264,762 from 1,200 orders
- **Top Product:** Chair ($195,620 revenue)
- **Average Order Value:** $1,054
- **Analysis Period:** 30 months (Jan 2023 - Jun 2025)

### Critical Issues Identified
⚠️ **High Return/Cancellation Rate:** 41.41% of orders are cancelled or returned
- Cancelled: 20.83%
- Returned: 20.58%
- Only 19.25% successfully delivered

### Customer Behavior
- **Low Loyalty:** Top customer made only 2 purchases
- **Single Purchase Dominance:** 90% of top customers made 1 order
- **Recommendation:** Implement loyalty programs and remarketing

### Marketing Performance
- **Best Channel:** Instagram (259 orders)
- **Balanced Performance:** All channels show similar effectiveness

## 📊 SQL Skills Demonstrated

| Skill | Queries |
|-------|---------|
| SELECT | All queries |
| WHERE | 6, 8 |
| GROUP BY | 1-9 |
| COUNT() | 1-10 |
| SUM() | 1, 3-5, 7-10 |
| AVG() | 1, 3-5, 9, 10 |
| MIN/MAX | 10 |
| ORDER BY | All queries |
| LIMIT | 5 |
| HAVING | 7 |
| Subqueries | 2 |
| Date Functions | 4 |
| Multiple Grouping | 8 |

## 📝 Files Description

- **`sql_queries.sql`** - Contains all 10 SQL queries with detailed comments
- **`run_queries.py`** - Python script that automates query execution
- **`results.txt`** - Complete output of all queries in tabular format
- **`summary.txt`** - Comprehensive business analysis and insights
- **`Data/cleanedEDA.csv`** - Source dataset

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- ✅ SQL query construction
- ✅ Data aggregation and summarization
- ✅ Filtering and conditional logic
- ✅ Date/time manipulation
- ✅ Subquery usage
- ✅ Business intelligence extraction
- ✅ Understanding SQL execution order

## 📫 Author

**Ecem Y.**  
Decolabs Internship - Project 3  
GitHub: [@ecemy3](https://github.com/ecemy3)

## 📄 License

This project is part of Decolabs internship program.

---

**Project Completion Date:** April 2026  
**Status:** ✅ Completed
