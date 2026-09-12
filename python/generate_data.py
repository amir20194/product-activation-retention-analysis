import numpy as np
import pandas as pd
from pathlib import Path


np.random.seed(42)

N_USERS = 5000

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

user_ids = np.arange(1, N_USERS + 1)

signup_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2026-01-01", "2026-06-30"),
        size=N_USERS
    )
)

countries = np.random.choice(
    ["India", "UAE", "UK", "USA", "Germany"],
    size=N_USERS,
    p=[0.35, 0.15, 0.15, 0.20, 0.15]
)

platforms = np.random.choice(
    ["Web", "iOS", "Android"],
    size=N_USERS,
    p=[0.55, 0.20, 0.25]
)

channels = np.random.choice(
    ["Organic", "Paid Search", "Referral", "LinkedIn", "Direct"],
    size=N_USERS,
    p=[0.30, 0.20, 0.15, 0.15, 0.20]
)

users = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": signup_dates,
    "country": countries,
    "platform": platforms,
    "acquisition_channel": channels
})

users.to_csv(OUTPUT_DIR / "users.csv", index=False)

print(users.head())
print()
print(f"Users generated: {len(users)}")


event_rows = []

for _, user in users.iterrows():
    user_id = user["user_id"]
    signup_date = pd.to_datetime(user["signup_date"])

    event_rows.append({
        "user_id": user_id,
        "event_timestamp": signup_date,
        "event_name": "signup"
    })

    if np.random.rand() < 0.85:
        onboarding_start = signup_date + pd.Timedelta(
            hours=np.random.randint(1, 24)
        )

        event_rows.append({
            "user_id": user_id,
            "event_timestamp": onboarding_start,
            "event_name": "onboarding_started"
        })

        if np.random.rand() < 0.75:
            onboarding_complete = onboarding_start + pd.Timedelta(
                hours=np.random.randint(1, 12)
            )

            event_rows.append({
                "user_id": user_id,
                "event_timestamp": onboarding_complete,
                "event_name": "onboarding_completed"
            })

            if np.random.rand() < 0.70:
                project_created = onboarding_complete + pd.Timedelta(
                    days=np.random.randint(0, 4)
                )

                event_rows.append({
                    "user_id": user_id,
                    "event_timestamp": project_created,
                    "event_name": "project_created"
                })

                invited_teammate = np.random.rand() < 0.45

                if invited_teammate:
                    invite_time = project_created + pd.Timedelta(
                        days=np.random.randint(0, 3)
                    )

                    event_rows.append({
                        "user_id": user_id,
                        "event_timestamp": invite_time,
                        "event_name": "teammate_invited"
                    })

                if np.random.rand() < 0.30:
                    integration_time = project_created + pd.Timedelta(
                        days=np.random.randint(0, 5)
                    )

                    event_rows.append({
                        "user_id": user_id,
                        "event_timestamp": integration_time,
                        "event_name": "integration_connected"
                    })

                if np.random.rand() < 0.50:
                    report_time = project_created + pd.Timedelta(
                        days=np.random.randint(1, 7)
                    )

                    event_rows.append({
                        "user_id": user_id,
                        "event_timestamp": report_time,
                        "event_name": "report_created"
                    })

                retention_probability = 0.55 if invited_teammate else 0.25

                if np.random.rand() < retention_probability:
                    retained_event = signup_date + pd.Timedelta(
                        days=np.random.randint(30, 41)
                    )

                    event_rows.append({
                        "user_id": user_id,
                        "event_timestamp": retained_event,
                        "event_name": "dashboard_viewed"
                    })

events = pd.DataFrame(event_rows)

events = events.sort_values(
    ["user_id", "event_timestamp"]
).reset_index(drop=True)

events.to_csv(
    OUTPUT_DIR / "events.csv",
    index=False
)

print()
print(events.head(15))
print()
print(f"Events generated: {len(events)}")
print()
print(events["event_name"].value_counts())