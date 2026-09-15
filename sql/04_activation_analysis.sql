-- Early product behaviors and their relationship with D30 retention.
-- These results show association, not causation.

WITH user_behavior AS (
    SELECT
        u.user_id,

        MAX(
            CASE
                WHEN e.event_name = 'project_created'
                THEN 1 ELSE 0
            END
        ) AS created_project,

        MAX(
            CASE
                WHEN e.event_name = 'teammate_invited'
                THEN 1 ELSE 0
            END
        ) AS invited_teammate,

        MAX(
            CASE
                WHEN e.event_name = 'integration_connected'
                THEN 1 ELSE 0
            END
        ) AS connected_integration,

        MAX(
            CASE
                WHEN e.event_name = 'report_created'
                THEN 1 ELSE 0
            END
        ) AS created_report,

        MAX(
            CASE
                WHEN e.event_name = 'dashboard_viewed'
                     AND e.event_timestamp >= DATE_ADD(u.signup_date, INTERVAL 30 DAY)
                     AND e.event_timestamp < DATE_ADD(u.signup_date, INTERVAL 41 DAY)
                THEN 1 ELSE 0
            END
        ) AS retained_d30

    FROM users u
    LEFT JOIN events e
        ON u.user_id = e.user_id

    GROUP BY
        u.user_id
)

SELECT
    'created_project' AS behavior,
    created_project AS behavior_flag,
    COUNT(*) AS users,
    SUM(retained_d30) AS retained_users,
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    ) AS d30_retention_rate_pct
FROM user_behavior
GROUP BY created_project

UNION ALL

SELECT
    'invited_teammate',
    invited_teammate,
    COUNT(*),
    SUM(retained_d30),
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    )
FROM user_behavior
GROUP BY invited_teammate

UNION ALL

SELECT
    'connected_integration',
    connected_integration,
    COUNT(*),
    SUM(retained_d30),
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    )
FROM user_behavior
GROUP BY connected_integration

UNION ALL

SELECT
    'created_report',
    created_report,
    COUNT(*),
    SUM(retained_d30),
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    )
FROM user_behavior
GROUP BY created_report

ORDER BY behavior, behavior_flag DESC;

-- Compare teammate invitation among activated users only.
-- Restricting the comparison to project creators makes the groups
-- more comparable than using all signups.

WITH user_behavior AS (
    SELECT
        u.user_id,

        MAX(
            CASE
                WHEN e.event_name = 'project_created'
                THEN 1 ELSE 0
            END
        ) AS created_project,

        MAX(
            CASE
                WHEN e.event_name = 'teammate_invited'
                THEN 1 ELSE 0
            END
        ) AS invited_teammate,

        MAX(
            CASE
                WHEN e.event_name = 'dashboard_viewed'
                     AND e.event_timestamp >= DATE_ADD(u.signup_date, INTERVAL 30 DAY)
                     AND e.event_timestamp < DATE_ADD(u.signup_date, INTERVAL 41 DAY)
                THEN 1 ELSE 0
            END
        ) AS retained_d30

    FROM users u
    LEFT JOIN events e
        ON u.user_id = e.user_id

    GROUP BY
        u.user_id
)

SELECT
    invited_teammate,
    COUNT(*) AS users,
    SUM(retained_d30) AS retained_users,
    ROUND(
        100.0 * SUM(retained_d30) / COUNT(*),
        2
    ) AS d30_retention_rate_pct

FROM user_behavior

WHERE created_project = 1

GROUP BY
    invited_teammate

ORDER BY
    invited_teammate DESC;
