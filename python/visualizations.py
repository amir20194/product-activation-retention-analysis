import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


OUTPUT_DIR = Path("outputs/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Activation funnel
funnel = pd.DataFrame({
    "stage": [
        "Signups",
        "Onboarding Started",
        "Onboarding Completed",
        "Project Created"
    ],
    "users": [5000, 4259, 3201, 2264]
})

plt.figure(figsize=(9, 5))
plt.bar(funnel["stage"], funnel["users"])
plt.title("Product Activation Funnel")
plt.ylabel("Users")
plt.xticks(rotation=15)

for i, value in enumerate(funnel["users"]):
    plt.text(i, value + 70, str(value), ha="center")

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "activation_funnel.png",
    dpi=150
)
plt.close()


# Retention by early product behavior
behavior = pd.DataFrame({
    "behavior": [
        "Invited Teammate",
        "Connected Integration",
        "Created Report"
    ],
    "retention_rate": [
        56.21,
        42.11,
        39.91
    ]
})

plt.figure(figsize=(8, 5))
plt.bar(
    behavior["behavior"],
    behavior["retention_rate"]
)

plt.title("D30 Retention by Early Product Behavior")
plt.ylabel("D30 Retention Rate (%)")
plt.ylim(0, 65)

for i, value in enumerate(behavior["retention_rate"]):
    plt.text(
        i,
        value + 1,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "retention_by_behavior.png",
    dpi=150
)
plt.close()


# Retention by signup cohort
cohort = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "retention_rate": [
        18.77,
        19.82,
        17.54,
        18.14,
        15.66,
        17.27
    ]
})

plt.figure(figsize=(8, 5))
plt.plot(
    cohort["month"],
    cohort["retention_rate"],
    marker="o"
)

plt.title("D30 Retention by Signup Month")
plt.xlabel("Signup Month")
plt.ylabel("D30 Retention Rate (%)")
plt.ylim(10, 25)

plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "retention_by_cohort.png",
    dpi=150
)
plt.close()


print("Charts created successfully.")
