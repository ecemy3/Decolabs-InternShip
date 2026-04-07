-- ============================================
-- PROJECT 3: SQL QUERIES
-- ============================================
-- Execution Order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
-- ============================================

-- QUERY 1: Product revenue analysis
-- Using GROUP BY and SUM aggregation
SELECT 
    Product, 
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS order_count,
    AVG(TotalPrice) AS avg_order_value
FROM orders
GROUP BY Product
ORDER BY revenue DESC;

-- ============================================

-- QUERY 2: Order status distribution
-- Using GROUP BY and COUNT aggregation
SELECT 
    OrderStatus, 
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY OrderStatus
ORDER BY count DESC;

-- ============================================

-- QUERY 3: Payment method analysis
-- Using GROUP BY and multiple aggregations
SELECT 
    PaymentMethod, 
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS transaction_count,
    AVG(TotalPrice) AS avg_transaction
FROM orders
GROUP BY PaymentMethod
ORDER BY revenue DESC;

-- ============================================

-- QUERY 4: Monthly sales trend
-- Using date manipulation and GROUP BY
SELECT 
    strftime('%Y-%m', Date) AS month,
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS order_count,
    AVG(TotalPrice) AS avg_order
FROM orders
GROUP BY month
ORDER BY month;

-- ============================================

-- QUERY 5: Top customers by spending
-- Using GROUP BY, aggregation and LIMIT
SELECT 
    CustomerID, 
    SUM(TotalPrice) AS total_spent,
    COUNT(*) AS order_count,
    AVG(TotalPrice) AS avg_per_order
FROM orders
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 10;

-- ============================================

-- QUERY 6: Outlier detection using WHERE clause
-- Filtering with WHERE clause
SELECT 
    OrderID,
    CustomerID,
    Product,
    TotalPrice,
    OrderStatus
FROM orders
WHERE TotalPrice > 3000
ORDER BY TotalPrice DESC;

-- ============================================

-- QUERY 7: HAVING clause example
-- Filtering after GROUP BY (WHERE vs HAVING difference)
SELECT 
    Product,
    SUM(TotalPrice) AS revenue,
    COUNT(*) AS order_count
FROM orders
GROUP BY Product
HAVING SUM(TotalPrice) > 50000
ORDER BY revenue DESC;

-- ============================================

-- QUERY 8: Combined analysis - Popular products status breakdown
-- Using multiple GROUP BY and WHERE combination
SELECT 
    Product,
    OrderStatus,
    COUNT(*) AS count,
    SUM(TotalPrice) AS revenue
FROM orders
WHERE Product IN ('Laptop', 'Phone', 'Monitor')
GROUP BY Product, OrderStatus
ORDER BY Product, count DESC;

-- ============================================

-- QUERY 9: Referral source effectiveness analysis
-- Analyzing which marketing channels perform best
SELECT 
    ReferralSource,
    COUNT(*) AS order_count,
    SUM(TotalPrice) AS total_revenue,
    AVG(TotalPrice) AS avg_order_value
FROM orders
GROUP BY ReferralSource
ORDER BY total_revenue DESC;

-- ============================================

-- QUERY 10: Overall statistics
-- Multiple aggregations without GROUP BY
SELECT 
    COUNT(*) AS total_orders,
    SUM(TotalPrice) AS total_revenue,
    AVG(TotalPrice) AS avg_order_value,
    MIN(TotalPrice) AS min_order,
    MAX(TotalPrice) AS max_order,
    COUNT(DISTINCT CustomerID) AS unique_customers,
    COUNT(DISTINCT Product) AS product_count
FROM orders;

-- ============================================
