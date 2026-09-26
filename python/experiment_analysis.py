from math import ceil
from pathlib import Path

import pandas as pd
from scipy.stats import norm

# Both variants include everyone who creates a first project.
root = Path(__file__).resolve().parents[1]
users = pd.read_csv(root / "data/users.csv", parse_dates=["signup_date"])
events = pd.read_csv(root / "data/events.csv", parse_dates=["event_timestamp"])

projects = events[events["event_name"] == "project_created"]
eligible = users[users["user_id"].isin(projects["user_id"])].copy()

views = events[events["event_name"] == "dashboard_viewed"].merge(
    eligible[["user_id", "signup_date"]], on="user_id"
)
days_since_signup = views["event_timestamp"] - views["signup_date"]
retained_ids = set(views.loc[
    (days_since_signup >= pd.Timedelta(days=30))
    & (days_since_signup < pd.Timedelta(days=41)), "user_id"
])
baseline_rate = eligible["user_id"].isin(retained_ids).mean()

# Target = 5 percentage point absolute improvement in D30 retention.
mde = 0.05

alpha = 0.05
power = 0.80

treatment_rate = baseline_rate + mde

z_alpha = norm.ppf(1 - alpha / 2)
z_power = norm.ppf(power)

pooled_rate = (baseline_rate + treatment_rate) / 2

sample_size = (
    (
        z_alpha * (2 * pooled_rate * (1 - pooled_rate)) ** 0.5
        + z_power
        * (
            baseline_rate * (1 - baseline_rate)
            + treatment_rate * (1 - treatment_rate)
        ) ** 0.5
    )
    ** 2
) / (treatment_rate - baseline_rate) ** 2

sample_size_per_variant = ceil(sample_size)
total_sample_size = sample_size_per_variant * 2

print("Experiment Design")
print("-----------------")
print(f"Baseline rate: {baseline_rate:.2%}")
print(f"Eligible project creators in dataset: {len(eligible)}")
print(f"Expected treatment rate: {treatment_rate:.2%}")
print(f"Minimum detectable effect: {mde:.2%}")
print(f"Alpha: {alpha}")
print(f"Power: {power:.0%}")
print()
print(f"Required users per variant: {sample_size_per_variant}")
print(f"Total required users: {total_sample_size}")
