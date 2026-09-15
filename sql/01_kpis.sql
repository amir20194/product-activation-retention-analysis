-- Baseline product KPIs
-- Activation = user creates at least one project within 7 days of signup.
-- D30 retention = user has a dashboard_viewed event between day 30 and day 40.

WITH user_metrics AS (
    SELECT
        u.user_id,
        u.signup_date,

        MAX(
            CASE
                WHEN e.event_name = 'project_created'
                     AND e.event_timestamp >= u.signup_date
                     AND e.event_timestamp < DATE_ADD(u.signup_date, INTERVAL 7 DAY)
                THEN 1
                ELSE 0
            END
        ) AS activated,

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
        u.signup_date
)

SELECT
    COUNT(*) AS total_signups,

    ROUND(
        100.0 * SUM(activated) / COUNT(*),
        2
    ) AS activation_rate_pct,

    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    ) AS d30_retention_rate_pct

FROM user_metrics;