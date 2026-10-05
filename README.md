# Product Activation & Retention Analysis

## Business Problem

A fictional B2B SaaS product wants to understand why many new users do not reach first value or return later.

Think of it as a shared reporting workspace: a user signs up to create a project, connect an integration, build a report, and work with colleagues. The dataset records an invitation sent, not whether a colleague accepted or collaborated.

The product team wants to understand:

- Where users drop during onboarding
- Which early product behaviors are associated with stronger retention
- Whether the current activation definition is meaningful
- What product intervention should be tested next

The goal of this analysis is to identify behaviors that distinguish retained users and translate those findings into an experiment recommendation.

---

## Executive Summary

The analysis covered 5,000 synthetic users and 18,431 product events.

Key findings:

- 45.28% of users created their first project within 7 days of signup.
- 17.82% of all users returned and viewed the dashboard between day 30 and day 40.
- The largest funnel loss occurred before onboarding completion.
- Among users who created a project, those who invited a teammate had 56.21% D30 retention compared with 26.24% for those who did not.
- This represents a 29.97 percentage-point difference and approximately 2.1x higher retention.

Teammate invitation therefore appears to be a strong behavioral signal associated with retention.

However, this analysis shows association, not causation. More engaged users may simply be more likely to invite teammates.

The largest immediate funnel investigation is onboarding completion (1,058 users lost). The specific retention hypothesis to test is a teammate invitation prompt after first project creation. The proposed D30 test needs a feasibility check because the current traffic would take about eight months to enroll.

---

## Metric Definitions

### Activation

A user is considered activated if they create their first project within 7 days of signup.

```text
Activation Rate =
Users creating a project within 7 days
/
Total signups
```

Observed activation rate: **45.28%**

### D30 Retention

A user is considered retained if they generate a `dashboard_viewed` event between day 30 and day 40 after signup.

This is a 30–40 day retention window rather than exact-day D30 retention.

Observed retention rate: **17.82%**

---

## KPI Framework

The current data supports a funnel and one return window. A product team would need a wider lifecycle view before deciding whether better activation creates lasting value.

| Stage | Metric and denominator | Status |
|---|---|---|
| Acquisition | Signups by channel | Measured; acquisition cost is unavailable |
| Activation | Project creators within 7 days / signups | Measured: 45.28% |
| Early collaboration | Project creators inviting a teammate / project creators | Measurable; invitation acceptance is not tracked |
| Engagement | Users creating or viewing a report in a week / eligible users | Requires repeated usage events and a defined observation period |
| Retention | Dashboard viewers on days 30–40 / signups | Measured: 17.82%; a narrow activity proxy |
| Longer-term value | Day 60/90 return, repeat report use, paid conversion, value per acquired user | Not measurable from this dataset; requires later events and billing data |

For a real team product, I would also track active teams, but this dataset has no `team_id`. I would not substitute invitation sends for accepted invitations or claim revenue impact from these files.

---

## Data

The project uses a synthetic product analytics dataset containing two main tables.

### users

| Column | Description |
|---|---|
| user_id | Unique user identifier |
| signup_date | Date the user signed up |
| country | User country |
| platform | Web, iOS or Android |
| acquisition_channel | User acquisition source |

### events

| Column | Description |
|---|---|
| user_id | User identifier |
| event_timestamp | Timestamp of the product event |
| event_name | Product event |

The event stream contains:

- signup
- onboarding_started
- onboarding_completed
- project_created
- teammate_invited
- integration_connected
- report_created
- dashboard_viewed

---

## 1. Activation Funnel

The first analysis examines how users progress from signup to the first meaningful product action.

| Funnel Stage | Users | Step Conversion |
|---|---:|---:|
| Signup | 5,000 | 100% |
| Onboarding Started | 4,259 | 85.18% |
| Onboarding Completed | 3,201 | 75.16% |
| Project Created | 2,264 | 70.73% |

Overall activation rate: **45.28%**

The largest absolute loss occurs before users complete onboarding.

Out of 5,000 signups, 3,201 users complete onboarding and 2,264 go on to create their first project.

This suggests two areas worth investigating:

1. Friction during onboarding
2. Difficulty reaching first product value after onboarding

![Product Activation Funnel](outputs/charts/activation_funnel.png)

---

## 2. Retention Analysis

Overall retention in the day 30–40 window is **17.82%**.

Retention was also analyzed across signup cohorts, platforms and acquisition channels.

Monthly retention ranged from:

- 19.82% in February
- 15.66% in May

The variation between signup cohorts is noticeable but relatively small compared with the behavioral differences identified later in the analysis.

![Retention by Signup Cohort](outputs/charts/retention_by_cohort.png)

---

## 3. Behavioral Drivers of Retention

The next question was whether particular early product behaviors were associated with stronger long-term retention.

Raw retention rates among users performing several key actions were:

| Behavior | D30 Retention |
|---|---:|
| Invited teammate | 56.21% |
| Connected integration | 42.11% |
| Created report | 39.91% |

![Retention by Product Behavior](outputs/charts/retention_by_behavior.png)

At first glance, teammate invitation appears to be the strongest retention signal.

However, comparing users who invited teammates with every user who did not invite a teammate creates an unfair comparison. A user must first create a project before they can invite a teammate.

The non-inviter group therefore contains many users who never activated.

To create a more meaningful comparison, the analysis was restricted to users who had already created a project.

### Retention Among Project Creators

| Behavior | Users | Retained Users | D30 Retention |
|---|---:|---:|---:|
| Invited teammate | 991 | 557 | 56.21% |
| Did not invite teammate | 1,273 | 334 | 26.24% |

The absolute difference is **+29.97 percentage points**.

In relative terms, users who invited a teammate had approximately **2.1x higher retention**.

This makes teammate invitation a strong candidate for an activation behavior worth testing.

---

## 4. Segmentation

Retention was also analyzed across acquisition channels and platforms.

### Acquisition Channel

| Channel | D30 Retention |
|---|---:|
| LinkedIn | 18.92% |
| Direct | 18.58% |
| Referral | 17.87% |
| Paid Search | 17.43% |
| Organic | 17.04% |

### Platform

| Platform | D30 Retention |
|---|---:|
| Android | 19.52% |
| iOS | 17.31% |
| Web | 17.26% |

The differences across acquisition channels and platforms are relatively modest.

For example, the highest and lowest acquisition-channel retention rates differ by less than 2 percentage points.

This suggests that early product behavior may be more useful for generating retention hypotheses than acquisition source alone in this dataset.

---

## Key Finding

The strongest behavioral signal identified in the analysis is teammate invitation.

Among users who had already created a project:

**56.21% D30 retention for users who invited a teammate**

compared with:

**26.24% D30 retention for users who did not invite a teammate**

This is a substantial difference, but it should not be interpreted as causal evidence.

Several explanations are possible:

- Collaborative usage may create more product value.
- Users with stronger intent may naturally be more likely to invite teammates.
- Teams may have more reasons to return to the product.
- Teammate invitation may simply be a signal of deeper engagement.

The analysis therefore generates a product hypothesis rather than proving that teammate invitations cause higher retention.

---

## Product Recommendation

Test whether encouraging collaboration immediately after users experience their first meaningful product value can improve retention.

The proposed product intervention is:

> After a user creates their first project, show a contextual prompt encouraging them to invite a teammate.

The prompt should appear after first project creation rather than at the beginning of onboarding so that users experience some product value before being asked to collaborate.

**Priority:** First inspect the onboarding-started → completed journey, where 1,058 users were lost, using step-level events and user feedback. In parallel, validate whether an invitation is accepted and leads to shared use. Only then prioritize building the prompt. This separates the larger funnel opportunity from the narrower retention hypothesis.

---

## Proposed Experiment

### Hypothesis

Encouraging users to invite a teammate after creating their first project will increase D30 retention.

### Eligibility

Users who successfully create their first project.

### Control

Current product experience after project creation.

### Treatment

A contextual teammate invitation prompt shown immediately after the user's first project is created.

### Primary Metric

D30 retention measured using the same day 30–40 retention window used in the analysis.

### Secondary Metric

Teammate invitation rate within 7 days.

This acts as a leading indicator showing whether the treatment actually changes the target behavior.

### Guardrail Metrics

- Report creation rate
- Integration connection rate
- Invite prompt dismissal rate (requires a new event)

### Experiment Parameters

Baseline D30 retention among **all eligible project creators**: **39.36%**

Minimum detectable effect: **+5 percentage points**

Expected treatment retention: **44.36%**

Statistical assumptions:

- Significance level (alpha): 0.05
- Statistical power: 80%
- Two-sided test

Required sample size: **1,527 users per variant**

Total experiment sample: **3,054 users**

The 26.24% retention rate for non-inviters is an observational segment, not the control baseline: randomization would include all project creators in both variants. The sample size is a normal approximation for two independent proportions. At the synthetic dataset's pace of 2,264 project creators in six months, enrollment would take roughly eight months; wait a further 40 days after the last signup for complete observation. Do not stop when the dashboard first shows a low p-value.

### Business case and test decision

The +5 percentage-point MDE is a planning assumption, not a value established by this dataset. At roughly 377 eligible project creators per month, that lift would mean about **19 additional retained users per month** (377 × 0.05). To decide whether this is worth building, estimate the contribution margin of an additional retained user and compare `19 × margin` with the monthly cost of the prompt and any support burden. Pricing, costs, and paid outcomes are absent here, so a monetary ROI would be invented. If the smallest worthwhile lift is lower than five points, recalculate sample size and duration before launch.

Randomize users 50/50 when they create their first project, keep the assignment fixed, and log the assignment and prompt exposure once per user. Predefine the same signup-based day 30–40 window for both arms. Check for missing exposure logs, duplicate users, and sample-ratio mismatch (pause to investigate if a 50/50 chi-square check has p < 0.001). Do not treat invitation sends as proof that teammates joined.

At the planned sample size and after the last user has a full 40-day window, compare user-level retention with a two-sided 95% confidence interval. Recommend rollout only if the interval excludes zero, the observed lift is at least the commercially justified threshold, and report creation and integration connection show no material harm. Agree guardrail limits before launch; a provisional trigger is a drop of more than two absolute percentage points in either rate, reviewed with its uncertainty. If invitation rate rises but retention does not, iterate or stop the prompt; if tracking or randomization fails, fix it before drawing a conclusion. With the current synthetic traffic, the eight-month enrollment is a warning: validate the commercial case and traffic first, or choose a shorter **validated** leading metric for a separate test rather than quietly changing this test's primary metric.

---

## Limitations

This project uses synthetic data and should not be interpreted as evidence from a real product.

Important limitations include:

- Retention probability was intentionally designed to be higher for users who invite teammates.
- Retention events were generated only for users who created a project.
- Project creation is therefore mechanically related to retention in the synthetic dataset.
- Behavioral relationships demonstrate the analytical workflow rather than real-world causal effects.
- The teammate invitation analysis is observational and cannot establish causality.
- The dataset does not include experiment exposure data or real customer outcomes.

In a production environment, the analysis would also require validation of event instrumentation, experiment eligibility, tracking quality and sufficient observation windows.

---

## Repository Structure

```text
product-activation-retention-analysis/
├── README.md
├── .github/workflows/verify-sql.yml
├── data/
│   ├── users.csv
│   └── events.csv
├── sql/
│   ├── 00_setup.sql
│   ├── 01_kpis.sql
│   ├── 02_funnel.sql
│   ├── 03_retention.sql
│   └── 04_activation_analysis.sql
├── python/
│   ├── generate_data.py
│   ├── experiment_analysis.py
│   └── visualizations.py
├── outputs/
│   └── charts/
│       ├── activation_funnel.png
│       ├── retention_by_behavior.png
│       └── retention_by_cohort.png
└── requirements.txt
```

---

## Reproduce the analysis

From the repository root, install the four packages in `requirements.txt` and run:

```bash
python -m pip install -r requirements.txt
python python/generate_data.py
python python/visualizations.py
python python/experiment_analysis.py
```

`generate_data.py` uses seed 42 and overwrites the two CSVs. The chart script reads the CSVs and overwrites the three chart images; its values are calculated from the data. The [Verify SQL workflow](.github/workflows/verify-sql.yml) loads both CSVs into a temporary MySQL 8 instance on GitHub Actions, runs all four analysis files, and checks key results against this README. It requires no local database. For a manual run, create a MySQL database, run `sql/00_setup.sql`, import users.csv before events.csv, then run `sql/01_kpis.sql` through `sql/04_activation_analysis.sql`. The CSVs and charts in this repository are the outputs from seed 42.

The [successful MySQL verification run](https://github.com/amir20194/product-activation-retention-analysis/actions/runs/36262742330) confirms that the SQL queries execute and the checked results match the documented figures.

---

## Analysis Workflow

The project follows a product analytics workflow:

**Business problem → Metric definition → Activation funnel → Retention analysis → Behavioral analysis → Product hypothesis → Experiment design**

The objective is not only to calculate metrics, but to connect analysis with a product decision.

---

## Tools Used

- SQL / MySQL
- Python
- Pandas
- NumPy
- Matplotlib
- SciPy
- Git / GitHub
