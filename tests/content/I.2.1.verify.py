"""Independent numerical verification for I.2.1 (Computing Ethics, Social Impact & Professional Responsibility)."""
from fractions import Fraction
import math

# 1. Privacy & Re-identification (Lesson 3: reidentification-and-mining)
# Quasi-identifier combinations: 365 birth dates * 2 sexes * 20 zip codes in a mid-sized city
# In a town of 10,000 people vs 14,600 combinations (5-digit ZIP + DOB + sex)
combos_single_zip = 365 * 2 * 80  # 80 birth years -> 58,400 distinct (DOB, sex) buckets per ZIP
assert combos_single_zip == 58400
# A small town of 20,000 people inside one ZIP code: average people per (DOB, sex) bucket < 1
avg_per_bucket = 20000 / combos_single_zip
assert round(avg_per_bucket, 2) == 0.34
# k-anonymity example: 4 records share the same generalized (ZIP prefix, age bracket, sex) -> k = 4
# Upper bound on re-identification probability within an equivalence class of size k
assert Fraction(1, 4) == Fraction(25, 100)
# If one class has 2 records and another has 8, overall k = min(2, 8) = 2 -> max prob 50%
assert min(2, 8) == 2
assert Fraction(1, 2) == Fraction(50, 100)

# 2. Classification & Group Fairness (Lessons 10 & 11)
# Concrete credit scoring example with two groups A and B (200 applicants each)
# Group A: 120 actually repay (Y=1, base rate 60%), 80 default (Y=0)
# Group B: 60 actually repay (Y=1, base rate 30%), 140 default (Y=0)
base_A = Fraction(120, 200)
base_B = Fraction(60, 200)
assert base_A == Fraction(3, 5)  # 60%
assert base_B == Fraction(3, 10) # 30%

# Classifier 1 (equal PPV = 75% across both groups, i.e., calibrated / satisfies Sufficiency)
# Group A: TP=90, FN=30, FP=30, TN=50 -> predicted positive = 120
tpA, fnA, fpA, tnA = 90, 30, 30, 50
assert tpA + fnA == 120 and fpA + tnA == 80
rate_pos_A = Fraction(tpA + fpA, 200)  # 120/200 = 60%
tpr_A = Fraction(tpA, tpA + fnA)       # 90/120 = 75%
fpr_A = Fraction(fpA, fpA + tnA)       # 30/80 = 37.5%
ppv_A = Fraction(tpA, tpA + fpA)       # 90/120 = 75%
assert rate_pos_A == Fraction(3, 5)
assert tpr_A == Fraction(3, 4)
assert fpr_A == Fraction(3, 8)
assert ppv_A == Fraction(3, 4)

# Group B: TP=45, FN=15, FP=15, TN=125 -> predicted positive = 60
tpB, fnB, fpB, tnB = 45, 15, 15, 125
assert tpB + fnB == 60 and fpB + tnB == 140
rate_pos_B = Fraction(tpB + fpB, 200)  # 60/200 = 30%
tpr_B = Fraction(tpB, tpB + fnB)       # 45/60 = 75%
fpr_B = Fraction(fpB, fpB + tnB)       # 15/140 = 3/28 (~10.7%)
ppv_B = Fraction(tpB, tpB + fpB)       # 45/60 = 75%
assert rate_pos_B == Fraction(3, 10)
assert tpr_B == Fraction(3, 4)
assert round(float(fpr_B) * 100, 1) == 10.7
assert ppv_B == Fraction(3, 4)

# Verify Chouldechova identity: FPR = (p / (1 - p)) * ((1 - PPV) / PPV) * TPR
def expected_fpr(p, ppv, tpr):
    return (p / (1 - p)) * ((1 - ppv) / ppv) * tpr

assert expected_fpr(base_A, ppv_A, tpr_A) == fpr_A
assert expected_fpr(base_B, ppv_B, tpr_B) == fpr_B
# Notice: PPV_A == PPV_B (75%) and TPR_A == TPR_B (75%), yet FPR_A (37.5%) != FPR_B (10.7%)!
# And positive selection rate: 60% vs 30% (Independence violated!)
assert ppv_A == ppv_B and tpr_A == tpr_B and fpr_A != fpr_B

# If we force Independence (selection rate = 45% for both = 90 approvals each)
# In Group B there are only 60 true repayers; even if ALL 60 repayers are approved,
# PPV_B can be at most 60/90 = 66.7%, whereas in Group A approvals could be 90/90 = 100%
assert Fraction(60, 90) == Fraction(2, 3)

# Simple confusion matrix exercise in Lesson 10 (100 applicants)
# TP=36, FP=14, FN=4, TN=46
tp10, fp10, fn10, tn10 = 36, 14, 4, 46
assert tp10 + fp10 + fn10 + tn10 == 100
assert Fraction(tp10, tp10 + fn10) == Fraction(9, 10)  # TPR = 90%
assert Fraction(fp10, fp10 + tn10) == Fraction(14, 60) # FPR = 23.33%
assert round(float(Fraction(fp10, fp10 + tn10)) * 100, 1) == 23.3
assert Fraction(tp10, tp10 + fp10) == Fraction(36, 50) # PPV = 72%
assert Fraction(tp10 + fp10, 100) == Fraction(1, 2)    # selection rate = 50%

# 3. Carbon Efficiency & CO2eq (Lesson 13: carbon-and-greenhouse)
# IPCC AR5 100-year GWP values: CO2 = 1, CH4 = 28, N2O = 265
gwp_co2, gwp_ch4, gwp_n2o = 1, 28, 265
# Example: 100 kg CO2 + 5 kg CH4 + 1 kg N2O
co2eq_ex = 100 * gwp_co2 + 5 * gwp_ch4 + 1 * gwp_n2o
assert co2eq_ex == 505  # 100 + 140 + 265 = 505 kg CO2eq
# Practice problem: 200 kg CO2 + 10 kg CH4 = 200 + 280 = 480 kg CO2eq
assert 200 * gwp_co2 + 10 * gwp_ch4 == 480
# Boss problem: 50 kg CO2 + 2 kg CH4 + 1 kg N2O = 50 + 56 + 265 = 371 kg CO2eq
assert 50 * gwp_co2 + 2 * gwp_ch4 + 1 * gwp_n2o == 371

# 4. Carbon Intensity & Demand Shifting (Lessons 14 & 15)
# Training/batch job consuming 50 kWh:
# Region A (coal-heavy): 600 gCO2eq/kWh -> 30,000 g = 30 kg CO2eq
# Region B (hydro/wind-heavy): 80 gCO2eq/kWh -> 4,000 g = 4 kg CO2eq
# Reduction: 26 kg CO2eq (86.7% drop)
em_A = 50 * 600 / 1000
em_B = 50 * 80 / 1000
assert em_A == 30.0 and em_B == 4.0 and em_A - em_B == 26.0

# Temporal shifting example: 20 kWh nightly backup
# Evening peak (19:00): 550 g/kWh -> 11 kg
# Noon solar peak (13:00): 150 g/kWh -> 3 kg
# Saved: 8 kg
assert 20 * 550 / 1000 == 11.0
assert 20 * 150 / 1000 == 3.0
assert 11.0 - 3.0 == 8.0

# Marginal vs average carbon intensity example:
# Grid currently running 800 MW solar (0 g/kWh) + 200 MW gas (400 g/kWh)
# Average intensity = (800*0 + 200*400) / 1000 = 80 g/kWh
avg_ci = (800 * 0 + 200 * 400) / 1000
assert avg_ci == 80.0
# If solar is already fully used, adding 1 kWh of load must be met by the dispatchable gas plant -> marginal = 400 g/kWh!
# If solar is being curtailed (e.g. 50 MW surplus wind/solar wasted), adding 1 kWh absorbs curtailed power -> marginal = 0 g/kWh!
# Practice problem: 40 kWh batch job shifted from 450 g/kWh to 100 g/kWh -> saves 14 kg CO2eq
assert 40 * (450 - 100) / 1000 == 14.0

# 5. Software Failures (Lesson 16: software-failures)
# Therac-25: 1-byte (8-bit unsigned) flag counter wraps around to 0 every 256 increments (2^8 = 256)
assert 2**8 == 256
# Mars Climate Orbiter (1999): 1 lbf = 4.44822 N -> impulse discrepancy factor ~4.45x
lbf_to_N = 4.4482216152605
assert round(lbf_to_N, 2) == 4.45
# Patriot missile (1991, Dhahran): 0.1 s in 24-bit fixed-point binary loses ~0.000000095 s per 0.1 s tick
# Exact error per 0.1 s: 1/10 - floor((1/10)*2^24)/2^24? Let's verify exact 24-bit truncation of 0.1!
# 0.1 in binary is 0.00011001100110011001100110011... (starts at 2^-4, so 24 bits after the leading 1 or after binary point)
# GAO report (IMTEC-92-26): 0.1 truncated to 24 bits after binary point:
approx_01 = Fraction(int(Fraction(1, 10) * (2**24)), 2**24)
err_per_tick = Fraction(1, 10) - approx_01
# Wait: check exact GAO value: 0.000000095 s per tick -> after 100 hours (100 * 3600 * 10 = 3,600,000 ticks)
ticks_100h = 100 * 3600 * 10
assert ticks_100h == 3600000
# Note: in GAO report, register held 24 bits total starting from 2^-1 (24 bits right of binary point -> 2^-24):
# err_per_tick = 1/10 - floor(2^24 / 10)/2^24 = (6/10)/2^24? Wait let's check both 2^23 and 2^24:
err_23 = Fraction(1, 10) - Fraction(int(Fraction(1, 10) * (2**23)), 2**23)
err_24 = Fraction(1, 10) - Fraction(int(Fraction(1, 10) * (2**24)), 2**24)
# In 24-bit register (1/2 + ... + 2^-24), wait 0.1 = (1.10011001100110011001100...) * 2^-4
# Truncated to 24 bits right of binary point: 0.00011001100110011001100_2 (23 fractional bits! Since sign/int or 24 bits including leading 0s -> err = 0.00000009536743 s)
drift_100h = float(err_23) * ticks_100h
assert abs(float(err_23) - 9.536743e-8) < 1e-12
assert round(drift_100h, 2) == 0.34
# Scud missile speed ~1676 m/s -> 0.343 s * 1676 m/s ≈ 575 m (GAO report: > 500 meters, ~600 meters)
miss_dist = drift_100h * 1676
assert 570 < miss_dist < 580

print("ALL I.2.1 VERIFICATIONS PASSED")
