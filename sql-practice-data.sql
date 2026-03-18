-- Sample data for SQL practice database

INSERT INTO stores VALUES
(1, 'North Sydney Central', 'Sydney', 'NSW', '2021-03-15'),
(2, 'Melbourne CBD', 'Melbourne', 'VIC', '2020-09-01'),
(3, 'Brisbane Riverside', 'Brisbane', 'QLD', '2022-01-20');

INSERT INTO employees VALUES
(1, 'Emma', 'Li', 'Store Manager', 1, '2021-03-01', 92000),
(2, 'Noah', 'Chen', 'Sales Analyst', 1, '2022-06-10', 76000),
(3, 'Olivia', 'Wang', 'Store Manager', 2, '2020-08-15', 91000),
(4, 'Lucas', 'Tran', 'Sales Assistant', 2, '2023-02-01', 58000),
(5, 'Mia', 'Patel', 'Store Manager', 3, '2022-01-05', 90000),
(6, 'Ethan', 'Nguyen', 'Sales Assistant', 3, '2022-04-18', 57000);

INSERT INTO customers VALUES
(1, 'Ava', 'Brown', 'F', 'Sydney', 'NSW', '2023-01-10', 'ava.brown@email.com'),
(2, 'Liam', 'Johnson', 'M', 'Sydney', 'NSW', '2023-02-14', 'liam.j@email.com'),
(3, 'Sophia', 'Lee', 'F', 'Melbourne', 'VIC', '2023-03-08', 'sophia.lee@email.com'),
(4, 'Mason', 'Taylor', 'M', 'Melbourne', 'VIC', '2023-04-19', 'mason.t@email.com'),
(5, 'Isabella', 'Martin', 'F', 'Brisbane', 'QLD', '2023-05-11', 'bella.m@email.com'),
(6, 'James', 'Wilson', 'M', 'Brisbane', 'QLD', '2023-06-22', 'j.wilson@email.com'),
(7, 'Charlotte', 'Hall', 'F', 'Sydney', 'NSW', '2023-07-04', 'charlotte.h@email.com'),
(8, 'Benjamin', 'Young', 'M', 'Adelaide', 'SA', '2023-08-17', 'ben.young@email.com');

INSERT INTO suppliers VALUES
(1, 'TechSource AU', 'Australia', 'sales@techsource.au'),
(2, 'Pacific Digital', 'Singapore', 'contact@pacificdigital.sg'),
(3, 'Smart Living Co', 'China', 'hello@smartliving.cn');

INSERT INTO categories VALUES
(1, 'Laptops'),
(2, 'Accessories'),
(3, 'Phones'),
(4, 'Tablets');

INSERT INTO products VALUES
(1, 'Aster Laptop 13', 1, 1, 1299.00, 930.00, 25, '2023-01-15'),
(2, 'Aster Laptop 15', 1, 1, 1599.00, 1180.00, 18, '2023-03-01'),
(3, 'Nimbus Phone X', 3, 2, 999.00, 710.00, 40, '2023-02-10'),
(4, 'Nimbus Phone Lite', 3, 2, 699.00, 510.00, 55, '2023-04-05'),
(5, 'Orbit Tablet 11', 4, 3, 749.00, 540.00, 22, '2023-05-12'),
(6, 'Wireless Mouse Pro', 2, 1, 59.00, 24.00, 120, '2022-11-20'),
(7, 'USB-C Dock', 2, 1, 149.00, 78.00, 75, '2023-01-08'),
(8, 'Noise-Cancel Headphones', 2, 3, 229.00, 120.00, 35, '2023-06-15');

INSERT INTO orders VALUES
(1001, 1, 2, 1, '2024-01-05', 'Completed', 'Credit Card'),
(1002, 2, 1, 1, '2024-01-07', 'Completed', 'PayPal'),
(1003, 3, 4, 2, '2024-01-09', 'Completed', 'Credit Card'),
(1004, 4, 3, 2, '2024-01-12', 'Returned', 'Credit Card'),
(1005, 5, 6, 3, '2024-01-14', 'Completed', 'Debit Card'),
(1006, 6, 5, 3, '2024-01-18', 'Completed', 'Credit Card'),
(1007, 7, 2, 1, '2024-01-19', 'Pending', 'PayPal'),
(1008, 8, 4, 2, '2024-01-21', 'Completed', 'Credit Card'),
(1009, 1, 2, 1, '2024-02-02', 'Completed', 'Credit Card'),
(1010, 3, 3, 2, '2024-02-03', 'Completed', 'Debit Card'),
(1011, 5, 6, 3, '2024-02-05', 'Completed', 'Credit Card'),
(1012, 2, 1, 1, '2024-02-09', 'Cancelled', 'PayPal');

INSERT INTO order_items VALUES
(1, 1001, 1, 1, 1299.00, 5.00),
(2, 1001, 6, 1, 59.00, 0.00),
(3, 1002, 3, 1, 999.00, 0.00),
(4, 1002, 8, 1, 229.00, 10.00),
(5, 1003, 4, 2, 699.00, 7.50),
(6, 1004, 7, 1, 149.00, 0.00),
(7, 1004, 6, 2, 59.00, 0.00),
(8, 1005, 5, 1, 749.00, 5.00),
(9, 1005, 8, 1, 229.00, 0.00),
(10, 1006, 2, 1, 1599.00, 8.00),
(11, 1007, 6, 3, 59.00, 0.00),
(12, 1008, 3, 1, 999.00, 12.00),
(13, 1008, 7, 1, 149.00, 0.00),
(14, 1009, 8, 2, 229.00, 5.00),
(15, 1010, 1, 1, 1299.00, 0.00),
(16, 1010, 7, 1, 149.00, 0.00),
(17, 1011, 4, 1, 699.00, 0.00),
(18, 1011, 6, 2, 59.00, 0.00),
(19, 1012, 2, 1, 1599.00, 3.00);
