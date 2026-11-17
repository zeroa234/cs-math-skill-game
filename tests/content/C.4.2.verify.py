"""Verify every numerical example, formula, and claim in data/content/C.4.2.yaml."""
import math


def check_capacity():
    # Skill-tree exercise (2): 200 req/s max, 70% target utilization, 5000 req/s peak
    eff_cap = 200 * 0.70
    assert math.isclose(eff_cap, 140.0)
    needed = math.ceil(5000 / eff_cap)
    assert needed == 36, needed

    # HPA formula: desiredReplicas = ceil(currentReplicas * (currentMetric / desiredMetric))
    # Lesson example 1: 4 replicas at 90% CPU, target 60%
    hpa1 = math.ceil(4 * (90 / 60))
    assert hpa1 == 6, hpa1

    # Lesson example 2: 5 replicas at 36% CPU, target 60% -> scale down to 3
    hpa2 = math.ceil(5 * (36 / 60))
    assert hpa2 == 3, hpa2

    # Practice item q-hpa-up: 6 replicas at 80% CPU, target 50% -> scale up to 10
    hpa3 = math.ceil(6 * (80 / 50))
    assert hpa3 == 10, hpa3

    # Practice item: 120 req/s max, 75% target -> 90 req/s effective; peak 1000 req/s -> 12
    eff2 = 120 * 0.75
    assert math.isclose(eff2, 90.0)
    assert math.ceil(1000 / eff2) == 12

    # Boss capacity item: 250 req/s max, 80% target -> 200 req/s effective; peak 3500 -> 18
    eff3 = 250 * 0.80
    assert math.isclose(eff3, 200.0)
    assert math.ceil(3500 / eff3) == 18


def check_sharding():
    # Naive modulo N=4 -> N=5 remapping fraction for keys 0..999
    keys = range(1000)
    moved_mod = sum(1 for k in keys if (k % 4) != (k % 5))
    assert moved_mod == 800, moved_mod  # 80% keys move!

    # Consistent hashing ring: adding 1 node to 4 nodes ideally moves ~1/(N+1) = 1/5 = 20%
    ideal_frac = 1 / 5
    assert math.isclose(ideal_frac, 0.20)

    # Hot-key skew: 4 shards, 10,000 req/s total, 40% to 1 hot key + 60% even across 4 shards
    hot_shard = 4000 + 6000 / 4
    cold_shard = 6000 / 4
    assert hot_shard == 5500 and cold_shard == 1500
    assert math.isclose(hot_shard / 10000, 0.55)


def check_sla_and_availability():
    # 30-day month = 30 * 24 * 60 = 43200 minutes; 365-day year = 365 * 24 * 60 = 525600 minutes
    month_min = 30 * 24 * 60
    year_min = 365 * 24 * 60
    assert month_min == 43200
    assert year_min == 525600

    # 99.9% (three nines)
    assert math.isclose(month_min * (1 - 0.999), 43.2)
    assert math.isclose(year_min * (1 - 0.999), 525.6)

    # 99.99% (four nines)
    assert math.isclose(month_min * (1 - 0.9999), 4.32)
    assert math.isclose(year_min * (1 - 0.9999), 52.56)

    # Two independent AZs, each with annual failure probability p = 0.01 (99%)
    # Probability both fail simultaneously (independent): p^2 = 0.0001 -> 99.99%
    p = 0.01
    both_down = p * p
    avail_2az = 1 - both_down
    assert math.isclose(both_down, 0.0001)
    assert math.isclose(avail_2az, 0.9999)

    # Serial chain of 3 components each at 99.9% -> 0.999^3 = 0.997002999 (~99.7%)
    serial3 = 0.999 ** 3
    assert math.isclose(serial3, 0.997002999, rel_tol=1e-9)


def check_scheduler_and_workloads():
    # Node bin-packing example:
    # Node-1: 4000m CPU, 8192Mi RAM total; allocated 2500m, 4096Mi -> free 1500m, 4096Mi
    # Node-2: 4000m CPU, 8192Mi RAM total; allocated 1000m, 2048Mi -> free 3000m, 6144Mi
    # Node-3: 4000m CPU, 8192Mi RAM total; allocated 3500m, 7168Mi -> free 500m, 1024Mi
    # Pod requests: 1000m CPU, 2048Mi RAM
    nodes = [
        ("node-1", 4000 - 2500, 8192 - 4096),
        ("node-2", 4000 - 1000, 8192 - 2048),
        ("node-3", 4000 - 3500, 8192 - 7168),
    ]
    feasible = [n for n, cpu, mem in nodes if cpu >= 1000 and mem >= 2048]
    assert feasible == ["node-1", "node-2"], feasible

    # Deployment rolling update: replicas=4, maxSurge=1, maxUnavailable=1
    # Max total Pods = 4 + 1 = 5; Min available Pods = 4 - 1 = 3
    assert 4 + 1 == 5 and 4 - 1 == 3

    # Practice: replicas=6, maxSurge=2, maxUnavailable=1 -> max 8, min 5
    assert 6 + 2 == 8 and 6 - 1 == 5


def check_economics_and_faas():
    hours_30d = 30 * 24
    assert hours_30d == 720

    # Skill-tree exercise (3):
    # Baseline: 10 instances * 720h; Peak: +20 instances * 4h/day * 30 days = 2400 instance-hours
    # On-demand: $0.10/h; 1-yr Reserved: $0.06/h
    hybrid_reserved = 10 * 0.06 * 720
    hybrid_ondemand = 20 * 0.10 * 4 * 30
    hybrid_total = hybrid_reserved + hybrid_ondemand
    all_ondemand = 10 * 0.10 * 720 + hybrid_ondemand
    all_reserved = 30 * 0.06 * 720

    assert math.isclose(hybrid_reserved, 432.0)
    assert math.isclose(hybrid_ondemand, 240.0)
    assert math.isclose(hybrid_total, 672.0)
    assert math.isclose(all_ondemand, 960.0)
    assert math.isclose(all_ondemand - hybrid_total, 288.0)
    assert math.isclose((all_ondemand - hybrid_total) / all_ondemand, 0.30)
    assert math.isclose(all_reserved, 1296.0)

    # FaaS vs 24x7 VM example (learning-paths/C.4.2.json step 3):
    # 1,000,000 calls/day, 200 ms (0.2s) each, 512 MB (0.5 GB) memory
    # Daily GB-seconds = 1_000_000 * 0.2 * 0.5 = 100,000 GB-s/day
    gb_s_day = 1_000_000 * 0.2 * 0.5
    assert math.isclose(gb_s_day, 100_000.0)
    # 30-day GB-seconds = 3,000,000 GB-s; at $0.000016/GB-s + $0.20/1M calls (30M calls = $6.00)
    faas_compute_30d = 3_000_000 * 0.000016
    faas_req_30d = 30 * 0.20
    faas_total_30d = faas_compute_30d + faas_req_30d
    assert math.isclose(faas_compute_30d, 48.0)
    assert math.isclose(faas_req_30d, 6.0)
    assert math.isclose(faas_total_30d, 54.0)

    # Low-traffic webhook comparison: 10,000 calls/day, 100 ms (0.1s), 512 MB (0.5 GB)
    # 30 days = 300,000 calls -> 300,000 * 0.1 * 0.5 = 15,000 GB-s
    low_gb_s = 300_000 * 0.1 * 0.5
    low_cost = low_gb_s * 0.000016 + 0.3 * 0.20
    assert math.isclose(low_gb_s, 15_000.0)
    assert math.isclose(low_cost, 0.30)
    # Compare with smallest always-on VM at $0.02/h * 720h = $14.40
    assert math.isclose(0.02 * 720, 14.40)

    # Break-even instance: Reserved $0.06/h vs On-demand $0.10/h -> 0.06 * 720 / 0.10 = 432h (60%)
    breakeven_hours = (0.06 * 720) / 0.10
    assert math.isclose(breakeven_hours, 432.0)
    assert math.isclose(breakeven_hours / 720, 0.60)

    # Boss economics item: 4 baseline * $0.05/h (720h) + 6 peak * $0.09/h * 5h/day * 30d
    b_res = 4 * 0.05 * 720
    b_on = 6 * 0.09 * 5 * 30
    b_tot = b_res + b_on
    b_all_on = 4 * 0.09 * 720 + b_on
    assert math.isclose(b_res, 144.0)
    assert math.isclose(b_on, 81.0)
    assert math.isclose(b_tot, 225.0)
    assert math.isclose(b_all_on, 340.2)
    assert math.isclose(b_all_on - b_tot, 115.2)


def main():
    check_capacity()
    check_sharding()
    check_sla_and_availability()
    check_scheduler_and_workloads()
    check_economics_and_faas()
    print("C.4.2 verify: all numerical checks passed.")


if __name__ == "__main__":
    main()
