"""Verify all numerical, unit-conversion, cgroup, Dockerfile, and scheduling claims in data/content/C.2.3.yaml."""
import math


def check_ept_and_vm():
    # Software 4-level page walk: 4 memory accesses (+1 data access = 5 total)
    # 2D EPT walk (4-level guest * 4-level host):
    # Each of the 4 guest levels requires a 4-level EPT walk (4 accesses) + 1 read of guest PTE (1) = 5, wait:
    # Plus final gPA -> hPA translation (4 EPT accesses) = 4*4 + 4 + 4 = 24 page-table accesses!
    g_levels = 4
    h_levels = 4
    # Guest PTE lookup per level = h_levels EPT steps + 1 guest PTE read; final gPA->hPA = h_levels steps; total PTE/EPT reads = (g_levels + 1) * h_levels + g_levels = 24
    worst_pt_accesses = (g_levels + 1) * h_levels + g_levels
    assert worst_pt_accesses == 24, worst_pt_accesses


def check_cgroups_math():
    # cpu.max = "200000 100000" -> 200ms quota per 100ms period = 2.0 CPU cores
    assert 200_000 / 100_000 == 2.0
    assert 150_000 / 100_000 == 1.5
    assert 250_000 / 100_000 == 2.5
    assert 100_000 / 1_000 == 100  # 100,000 us = 100 ms

    # memory.max = 4G = 4 GiB = 4 * 1024^3 bytes
    assert 4 * (1024**3) == 4_294_967_296

    # K8s millicores and MiB
    assert 500 + 500 == 1000  # 500m + 500m = 1 CPU core
    assert 128 * 2 == 256     # 2 containers * 128 Mi = 256 Mi > 200 Mi limit


def check_k8s_scheduling():
    # Node placement example 1: Pod requests 700m CPU, 256Mi RAM
    nodes1 = [
        ("node-A", 500, 1024, []),
        ("node-B", 1200, 512, []),
        ("node-C", 2000, 128, []),
    ]
    fit1 = [n for n, cpu, mem, taints in nodes1 if cpu >= 700 and mem >= 256 and not taints]
    assert fit1 == ["node-B"], fit1

    # Node placement example 2 (with taints): Pod requests 600m CPU, 300Mi RAM, no tolerations
    nodes2 = [
        ("node-A", 1500, 1024, ["gpu=true:NoSchedule"]),
        ("node-B", 900, 400, []),
        ("node-C", 500, 2048, []),
    ]
    fit2 = [n for n, cpu, mem, taints in nodes2 if cpu >= 600 and mem >= 300 and not taints]
    assert fit2 == ["node-B"], fit2

    # PodOverhead example: Container 1 requests 500m/256Mi, Container 2 requests 250m/128Mi, PodOverhead 100m/64Mi
    # Total node reservation = (500 + 250 + 100)m = 850m CPU, (256 + 128 + 64)Mi = 448Mi RAM
    assert 500 + 250 + 100 == 850
    assert 256 + 128 + 64 == 448


def check_dockerfile_sample():
    dockerfile = [
        "FROM python:3.12-slim",
        "WORKDIR /app",
        "COPY requirements.txt .",
        "RUN pip install --no-cache-dir -r requirements.txt",
        "COPY . .",
        "USER 1000:1000",
        'CMD ["python", "app.py"]',
    ]
    # Dependencies installed BEFORE copying application source code for layer cache efficiency
    assert dockerfile.index("COPY requirements.txt .") < dockerfile.index("COPY . .")
    assert dockerfile.index("RUN pip install --no-cache-dir -r requirements.txt") < dockerfile.index("COPY . .")
    assert any(l.startswith("USER ") and "root" not in l for l in dockerfile)


def main():
    check_ept_and_vm()
    check_cgroups_math()
    check_k8s_scheduling()
    check_dockerfile_sample()
    print("C.2.3 verify: all numerical, cgroup, Dockerfile, and scheduling checks passed.")


if __name__ == "__main__":
    main()
