show databases;
use liquorsales;
show tables;
SELECT * FROM finance_liquor_sales;

SELECT * FROM finance_liquor_sales
WHERE date BETWEEN '2016-01-01 00:00:00' AND '2019-12-31 23:59:59';