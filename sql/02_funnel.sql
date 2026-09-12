-- Product activation funnel
-- Measures user drop-off from signup to first meaningful product action.

WITH funnel AS (
    SELECT
        u.user_id,

        MAX(
            CASE
                WHEN e.event_name = 'signup'
                THEN 1 ELSE 0
            END
        ) AS signed_up,

        MAX(
            CASE
                WHEN e.event_name = 'onboarding_started'
                THEN 1 ELSE 0
            END
        ) AS onboarding_started,

        MAX(
            CASE
                WHEN e.event_name = 'onboarding_completed'
                THEN 1 ELSE 0
            END
        ) AS onboarding_completed,

        MAX(
            CASE
                WHEN e.event_name = 'project_created'
                THEN 1 ELSE 0
            END
        ) AS project_created

    FROM users u
    LEFT JOIN events e
        ON u.user_id = e.user_id

    GROUP BY
        u.user_id
)

SELECT
    COUNT(*) AS total_signups,

    SUM(onboarding_started) AS onboarding_started_users,

    ROUND(
        100.0 * SUM(onboarding_started) / COUNT(*),
        2
    ) AS onboarding_started_pct,

    SUM(onboarding_completed) AS onboarding_completed_users,

    ROUND(
        100.0 * SUM(onboarding_completed) / SUM(onboarding_started),
        2
    ) AS onboarding_completion_step_pct,

    SUM(project_created) AS project_created_users,

    ROUND(
        100.0 * SUM(project_created) / SUM(onboarding_completed),
        2
    ) AS project_creation_step_pct,

    ROUND(
        100.0 * SUM(project_created) / COUNT(*),
        2
    ) AS overall_activation_pct

FROM funnel;
