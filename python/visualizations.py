from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


root = Path(__file__).resolve().parents[1]
output_dir = root / "outputs/charts"
output_dir.mkdir(parents=True, exist_ok=True)

users = pd.read_csv(root / "data/users.csv", parse_dates=["signup_date"])
events = pd.read_csv(root / "data/events.csv", parse_dates=["event_timestamp"])

event_users = {
    name: set(group["user_id"])
    for name, group in events.groupby("event_name")
}

# Count unique users, in funnel order.
stages = ["signup", "onboarding_started", "onboarding_completed", "project_created"]
counts = [len(event_users.get(stage, set())) for stage in stages]
labels = ["Signups", "Onboarding Started", "Onboarding Completed", "Project Created"]

plt.figure(figsize=(9, 5))
plt.bar(labels, counts)
plt.title("Product Activation Funnel")
plt.ylabel("Users")
plt.xticks(rotation=15)
plt.ylim(0, max(counts) * 1.12)
for i, count in enumerate(counts):
    plt.text(i, count + 60, str(count), ha="center")
plt.tight_layout()
plt.savefig(output_dir / "activation_funnel.png", dpi=150)
plt.close()

# A dashboard view only counts in the 30-40 day retention window.
views = events[events["event_name"] == "dashboard_viewed"].merge(
    users[["user_id", "signup_date"]], on="user_id"
)
age = views["event_timestamp"] - views["signup_date"]
retained_ids = set(views.loc[
    (age >= pd.Timedelta(days=30)) & (age < pd.Timedelta(days=41)), "user_id"
])
users["retained"] = users["user_id"].isin(retained_ids)

behaviors = [
    ("Invited Teammate", "teammate_invited"),
    ("Connected Integration", "integration_connected"),
    ("Created Report", "report_created"),
]
rates = [
    100 * users.loc[users["user_id"].isin(event_users.get(event, set())), "retained"].mean()
    for _, event in behaviors
]

plt.figure(figsize=(8, 5))
plt.bar([label for label, _ in behaviors], rates)
plt.title("D30 Retention by Early Product Behavior")
plt.ylabel("Day 30-40 Retention Rate (%)")
plt.ylim(0, max(rates) * 1.18)
for i, rate in enumerate(rates):
    plt.text(i, rate + 1, f"{rate:.1f}%", ha="center")
plt.tight_layout()
plt.savefig(output_dir / "retention_by_behavior.png", dpi=150)
plt.close()

cohorts = users.groupby(users["signup_date"].dt.to_period("M"))["retained"].mean() * 100
plt.figure(figsize=(8, 5))
plt.plot(cohorts.index.astype(str), cohorts.values, marker="o")
plt.title("Day 30-40 Retention by Signup Month")
plt.xlabel("Signup Month")
plt.ylabel("Retention Rate (%)")
plt.ylim(0, max(25, cohorts.max() * 1.2))
plt.tight_layout()
plt.savefig(output_dir / "retention_by_cohort.png", dpi=150)
plt.close()

print("Charts created from data/users.csv and data/events.csv")
