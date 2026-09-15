from math import ceil
from scipy.stats import norm

# Baseline D30 retention among project creators
# who did not invite a teammate.
baseline_rate = 0.2624

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
print(f"Expected treatment rate: {treatment_rate:.2%}")
print(f"Minimum detectable effect: {mde:.2%}")
print(f"Alpha: {alpha}")
print(f"Power: {power:.0%}")
print()
print(f"Required users per variant: {sample_size_per_variant}")
print(f"Total required users: {total_sample_size}")
