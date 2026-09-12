-- D30 retention analysis by cohort and user segment
-- Retained = dashboard_viewed between day 30 and day 40 after signup.

WITH user_retention AS (
    SELECT
        u.user_id,
        u.signup_date,
        DATE_FORMAT(u.signup_date, '%Y-%m') AS signup_month,
        u.platform,
        u.acquisition_channel,

        MAX(
            CASE
                WHEN e.event_name = 'dashboard_viewed'
                     AND e.event_timestamp >= DATE_ADD(u.signup_date, INTERVAL 30 DAY)
                     AND e.event_timestamp < DATE_ADD(u.signup_date, INTERVAL 41 DAY)
                THEN 1
                ELSE 0
            END
        ) AS retained_d30

    FROM users u
    LEFT JOIN events e
        ON u.user_id = e.user_id

    GROUP BY
        u.user_id,
        u.signup_date,
        u.platform,
        u.acquisition_channel
)

-- Retention by signup month
SELECT
    'signup_month' AS segment_type,
    signup_month AS segment,
    COUNT(*) AS users,
    SUM(retained_d30) AS retained_users,
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    ) AS d30_retention_rate_pct
FROM user_retention
GROUP BY signup_month

UNION ALL

-- Retention by platform
SELECT
    'platform' AS segment_type,
    platform AS segment,
    COUNT(*) AS users,
    SUM(retained_d30) AS retained_users,
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    ) AS d30_retention_rate_pct
FROM user_retention
GROUP BY platform

UNION ALL

-- Retention by acquisition channel
SELECT
    'acquisition_channel' AS segment_type,
    acquisition_channel AS segment,
    COUNT(*) AS users,
    SUM(retained_d30) AS retained_users,
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    ) AS d30_retention_rate_pct
FROM user_retention
GROUP BY acquisition_channel

ORDER BY segment_type, d30_retention_rate_pct DESC;
