-- Practice questions and example queries

-- 1. Show all customers from NSW
SELECT *
FROM customers
WHERE state = 'NSW';

-- 2. List products with category names
SELECT p.product_name, c.category_name, p.unit_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
ORDER BY p.unit_price DESC;

-- 3. Total sales by store
SELECT s.store_name,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS total_sales
FROM orders o
JOIN stores s ON o.store_id = s.store_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY s.store_name
ORDER BY total_sales DESC;

-- 4. Top 5 best-selling products by quantity
SELECT p.product_name,
       SUM(oi.quantity) AS total_qty
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.product_name
ORDER BY total_qty DESC, p.product_name
LIMIT 5;

-- 5. Customers who placed more than one order
SELECT c.first_name, c.last_name, COUNT(*) AS order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(*) > 1;

-- 6. Average order value by payment method
SELECT o.payment_method,
       ROUND(AVG(order_total), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           o.payment_method,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.order_id, o.payment_method
) o
GROUP BY o.payment_method;

-- 7. Profit by product
SELECT p.product_name,
       ROUND(SUM((oi.unit_price - p.cost_price) * oi.quantity * (1 - oi.discount_pct / 100.0)), 2) AS estimated_profit
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.product_name
ORDER BY estimated_profit DESC;

-- 8. Monthly sales trend
SELECT SUBSTR(o.order_date, 1, 7) AS sales_month,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0)), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY SUBSTR(o.order_date, 1, 7)
ORDER BY sales_month;
