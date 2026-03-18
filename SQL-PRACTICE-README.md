# SQL Practice Database

I made you a simple retail-style practice database with enough relationships to learn real SQL.

## Files

- `sql-practice-schema.sql` — creates the tables
- `sql-practice-data.sql` — inserts sample data
- `sql-practice-queries.sql` — example practice queries

## Database structure

Tables included:
- `stores`
- `employees`
- `customers`
- `suppliers`
- `categories`
- `products`
- `orders`
- `order_items`

This gives you practice with:
- `SELECT`, `WHERE`, `ORDER BY`
- `JOIN`
- `GROUP BY`, `HAVING`
- aggregates like `SUM`, `AVG`, `COUNT`
- profit and sales calculations
- filtering completed vs pending/cancelled orders

## If you want to use SQLite locally

If `sqlite3` is installed, run:

```bash
sqlite3 practice.db < sql-practice-schema.sql
sqlite3 practice.db < sql-practice-data.sql
sqlite3 practice.db
```

Then inside SQLite:

```sql
.tables
SELECT * FROM customers;
.read sql-practice-queries.sql
```

## Good beginner exercises

1. Find the top 3 customers by total spending.
2. Show total revenue by state.
3. Find products that have never been sold.
4. Show each employee and how many orders they handled.
5. Calculate total discount given per product.
6. Find the month with the highest revenue.
7. Show average order value by store.
8. Find customers who only bought accessories.

## Next upgrades I can add

If you want, I can also make:
- a **harder version** with 15+ tables
- a **university-style assignment set**
- a **SQLite `.db` file** if the right tool is available
- a **data analyst project version** with messy data for cleaning practice
