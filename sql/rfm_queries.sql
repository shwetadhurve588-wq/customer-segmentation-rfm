 SELECT COUNT(*) FROM retail_clean;


 
CREATE TABLE rfm AS
SELECT
    customer_id,
    ((SELECT MAX(invoice_date)::date FROM retail_clean) + 1)
        - MAX(invoice_date)::date            AS recency,
    COUNT(DISTINCT invoice_no)               AS frequency,
    ROUND(SUM(total_price)::numeric, 2)      AS monetary
FROM retail_clean
GROUP BY customer_id;

SELECT * FROM rfm ORDER BY monetary DESC LIMIT 10;
SELECT COUNT(*) FROM rfm;   -- about 4,300 customers




CREATE TABLE rfm_scores AS
SELECT
    customer_id, recency, frequency, monetary,
    NTILE(5) OVER (ORDER BY recency DESC)   AS r_score,
    NTILE(5) OVER (ORDER BY frequency ASC)  AS f_score,
    NTILE(5) OVER (ORDER BY monetary ASC)   AS m_score
FROM rfm;

SELECT * FROM rfm_scores LIMIT 10;




CREATE TABLE rfm_segments AS
SELECT *,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3                  THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2                  THEN 'New / Promising'
        WHEN r_score <= 2 AND f_score >= 3                  THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2                  THEN 'Lost'
        ELSE 'Potential Loyalists'
    END AS segment
FROM rfm_scores;

SELECT
    segment,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)    AS pct_customers,
    ROUND(SUM(monetary), 0)                               AS revenue,
    ROUND(100.0 * SUM(monetary) / SUM(SUM(monetary)) OVER (), 1) AS pct_revenue,
    ROUND(AVG(recency), 0)                                AS avg_recency_days,
    ROUND(AVG(frequency), 1)                              AS avg_orders,
    ROUND(AVG(monetary), 0)                               AS avg_spend
FROM rfm_segments
GROUP BY segment
ORDER BY revenue DESC;