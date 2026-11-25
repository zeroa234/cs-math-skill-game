#!/usr/bin/env python3
"""Independent numerical & symbolic verification for H.1.3 (Signals & Systems)."""
import cmath
import math


def approx(a, b, tol=1e-9):
    assert abs(a - b) <= tol, f"Expected {b}, got {a} (diff={abs(a - b)})"


def sinc(u):
    return 1.0 if abs(u) < 1e-15 else math.sin(math.pi * u) / (math.pi * u)


def discrete_conv(x, h):
    y = [0] * (len(x) + len(h) - 1)
    for i, xv in enumerate(x):
        for j, hv in enumerate(h):
            y[i + j] += xv * hv
    return y


def dft(x):
    N = len(x)
    out = []
    for k in range(N):
        s = sum(x[n] * cmath.exp(-2j * math.pi * k * n / N) for n in range(N))
        out.append(s)
    return out


def alias_freq(f, fs):
    k = round(f / fs)
    return abs(f - k * fs)


def main():
    checks = 0

    # --- Ch 1: Continuous & Discrete Signals ---
    # ct-signals-transforms: x(t) on [0,4], y(t)=x(2t-4) -> [2,4]
    t_lo, t_hi = (0 + 4) / 2, (4 + 4) / 2
    approx(t_lo, 2)
    approx(t_hi, 4)
    # q-combo-interval: x(t) on [-2, 6], y(t)=x(2t+2) -> [-2, 2], duration = 4
    lo2, hi2 = (-2 - 2) / 2, (6 - 2) / 2
    approx(lo2, -2)
    approx(hi2, 2)
    approx(hi2 - lo2, 4)
    # q-reversal-shift: x(t) on [1,3], y(t)=x(4-t) -> 1 <= 4-t <= 3 -> 1 <= t <= 3
    approx(4 - 3, 1)
    approx(4 - 1, 3)
    checks += 3

    # ct-signal-types-singularity:
    # E = int_0^inf (2*exp(-2t))^2 dt = int_0^inf 4*exp(-4t) dt = 1
    E_num = sum((2 * math.exp(-2 * (i + 0.5) * 1e-4)) ** 2 * 1e-4 for i in range(100000))
    approx(E_num, 1.0, tol=1e-4)
    # Power of 4*cos(10*pi*t) over period T=0.2
    T = 0.2
    M = 10000
    P_num = sum((4 * math.cos(10 * math.pi * (i + 0.5) * T / M)) ** 2 for i in range(M)) / M
    approx(P_num, 8.0, tol=1e-6)
    # Sifting examples: (t^2+3) at t=2 -> 7; (3t+1) at t=3 -> 10
    assert (2**2 + 3) == 7
    assert (3 * 3 + 1) == 10
    checks += 4

    # dt-signals-sequences:
    # Energy of [1, -2, 2]
    assert sum(v**2 for v in [1, -2, 2]) == 9
    # Period of cos(3*pi/4 * n) -> 3/8 -> N=8; verify periodicity
    for n in range(16):
        approx(math.cos(3 * math.pi / 4 * (n + 8)), math.cos(3 * math.pi / 4 * n), tol=1e-12)
    # Period of cos(2*pi/5 * n) -> N=5
    for n in range(10):
        approx(math.cos(2 * math.pi / 5 * (n + 5)), math.cos(2 * math.pi / 5 * n), tol=1e-12)
    # Decimation: x[n]=2n+1, y[n]=x[2n], y[3]=x[6]=13
    assert 2 * (2 * 3) + 1 == 13
    checks += 4

    # systems-and-interconnections:
    # Moving average: y[1] = 0.5*6 + 0.5*2 = 4
    approx(0.5 * 6 + 0.5 * 2, 4.0)
    # Cascade square then +3 at x=2 -> 7
    assert (2**2) + 3 == 7
    # Accumulator y[n]=x[n]+y[n-1], x=[3,-1,4], y[-1]=0 -> y=[3,2,6]
    y = 0
    ys = []
    for xv in [3, -1, 4]:
        y = xv + y
        ys.append(y)
    assert ys == [3, 2, 6]
    checks += 3

    # --- Ch 2: LTI ---
    # system-properties-lti:
    # a) 2x+1: x=0 -> 1 != 0 (nonlinear), shift invariant
    assert 2 * 0 + 1 == 1
    # c) n*x[n]: linear, time-varying
    assert 5 * 10 != (5 - 2) * 10
    # differential-and-difference-eqs:
    # Guess: y[n]=0.5y[n-1]+0.5x[n], x=100, y[-1]=0 -> y[0]=50, y[1]=75
    y = 0.0
    for _ in range(2):
        y = 0.5 * y + 0.5 * 100
    approx(y, 75.0)
    # ODE dy/dt + 2y = x, x=0, y(0)=5 -> dy/dt|_0 = -10
    approx(-2 * 5, -10)
    # Example: y[n]=0.5y[n-1]+x[n], x=u[n] -> [1, 1.5, 1.75]
    y, seq = 0.0, []
    for _ in range(3):
        y = 0.5 * y + 1.0
        seq.append(y)
    assert seq == [1.0, 1.5, 1.75]
    # q-diff-eq-iter: y[n]=0.5y[n-1]+2x[n], x=[1,1,0] -> y=[2, 3, 1.5]
    y, seq = 0.0, []
    for xv in [1, 1, 0]:
        y = 0.5 * y + 2 * xv
        seq.append(y)
    assert seq == [2.0, 3.0, 1.5]
    checks += 6

    # eigenfunctions-complex-exp:
    # H(j5) = 3 - 4j, amp=2 -> 2*|3-4j| = 10
    approx(2 * abs(3 - 4j), 10.0)
    # H(e^jw) = (1 + e^-jw)/2 = cos(w/2)e^(-jw/2)
    for w in [0.0, 0.7, math.pi / 2, math.pi]:
        lhs = (1 + cmath.exp(-1j * w)) / 2
        rhs = math.cos(w / 2) * cmath.exp(-1j * w / 2)
        approx(lhs, rhs)
    # H(jw) = 6 / (jw + 3) at w=4 -> |H| = 6/5 = 1.2
    approx(abs(6 / (4j + 3)), 1.2)
    # First-difference H(e^jpi) = 1 - e^-jpi = 2
    approx(abs(1 - cmath.exp(-1j * math.pi)), 2.0)
    checks += 4

    # --- Ch 3: Sampling ---
    # Nyquist: f_max=4000 -> 8000 Hz
    assert 2 * 4000 == 8000
    # 300 Hz at 1000 Hz -> 300 Hz (no alias); at 500 Hz -> 200 Hz
    assert alias_freq(300, 1000) == 300
    assert alias_freq(300, 500) == 200
    for n in range(20):
        approx(math.cos(2 * math.pi * 300 / 500 * n), math.cos(2 * math.pi * 200 / 500 * n), tol=1e-12)
    # 700 Hz at 1000 Hz -> 300 Hz; 1200 Hz at 1000 Hz -> 200 Hz
    assert alias_freq(700, 1000) == 300
    assert alias_freq(1200, 1000) == 200
    # sinc(2)=0, example x_r(0.5) = sinc(0.5)+sinc(-0.5) = 4/pi
    approx(sinc(2), 0.0, tol=1e-12)
    approx(sinc(0.5) + sinc(-0.5), 4 / math.pi, tol=1e-12)
    # ADC: 8-bit 5.12V -> 20mV, max err 10mV; 10-bit 10.24V -> 10mV
    approx(5.12 / (2**8) * 1000, 20.0)
    approx(10.24 / (2**10) * 1000, 10.0)
    # DAC: binary 1010 -> 10 -> 10 V
    assert int("1010", 2) * 1 == 10
    checks += 10

    # --- Ch 4: Convolution ---
    # Length: 5 + 3 - 1 = 7
    assert 5 + 3 - 1 == 7
    # [1,2,1] * [1,-1] = [1, 1, -1, -1]
    assert discrete_conv([1, 2, 1], [1, -1]) == [1, 1, -1, -1]
    # [2,1,3] * [1,2] = [2, 5, 5, 6]
    assert discrete_conv([2, 1, 3], [1, 2]) == [2, 5, 5, 6]
    # CT convolution: rect[0,2] * rect[0,1] at t=1.5 -> overlap [0.5, 1.5] length 1
    dt = 1e-4
    t = 1.5
    conv_15 = sum(
        (1.0 if 0 <= tau <= 2 else 0.0) * (1.0 if 0 <= t - tau <= 1 else 0.0) * dt
        for tau in [k * dt for k in range(-10000, 40000)]
    )
    approx(conv_15, 1.0, tol=1e-3)
    # u(t) * e^(-2t)u(t) -> (1 - e^-2t)/2 -> 0.5 at t->inf
    approx((1 - math.exp(-2 * 20)) / 2, 0.5, tol=1e-12)
    # Absolute sum: sum_{n=0}^inf 0.8^n = 5; sum_{n=0}^inf |-0.6|^n = 2.5
    approx(1 / (1 - 0.8), 5.0)
    approx(1 / (1 - 0.6), 2.5)
    checks += 7

    # --- Ch 5: Frequency Domain ---
    # CTFT of 6*e^(-3t)u(t) at w=0 -> 2; 10*e^(-3t)u(t) at w=4 -> 2
    approx(abs(6 / (3 + 0j)), 2.0)
    approx(abs(10 / (3 + 4j)), 2.0)
    # Modulation: [-4, 4] kHz shifted by 100 kHz -> [96, 104] kHz
    assert 100 + 4 == 104
    # Parseval: |X(jw)|=3 on [-2pi, 2pi] -> E = (1/(2pi)) * 9 * 4pi = 18
    approx((1 / (2 * math.pi)) * (3**2) * (4 * math.pi), 18.0)
    # dB: 20*log10(10)=20; 20*log10(1/sqrt(2)) ≈ -3.0103; 20*log10(0.1) = -20
    approx(20 * math.log10(10), 20.0)
    approx(20 * math.log10(1 / math.sqrt(2)), -3.0102999566, tol=1e-6)
    approx(20 * math.log10(0.1), -20.0)
    # 1st-order LPF tau=0.001 -> wc = 1000 rad/s
    approx(1 / 0.001, 1000.0)
    # DTFT of 0.5^n u[n] at w=0 -> 2; (-0.5)^n u[n] at w=pi -> 2
    approx(abs(1 / (1 - 0.5 * cmath.exp(0j))), 2.0)
    approx(abs(1 / (1 + 0.5 * cmath.exp(-1j * math.pi))), 2.0)
    # 2-pt avg H(e^jw) at 0, pi/2, pi
    approx(abs(math.cos(0)), 1.0)
    approx(abs(math.cos(math.pi / 4)), 1 / math.sqrt(2))
    approx(abs(math.cos(math.pi / 2)), 0.0, tol=1e-12)
    # DFT: fs=8000, N=8 -> df=1000; boss fs=16000, N=32 -> df=500
    approx(8000 / 8, 1000.0)
    approx(16000 / 32, 500.0)
    # 4-pt DFT of [1,1,1,1] -> [4,0,0,0]; of [1,-1,1,-1] -> [0,0,4,0]
    X1 = dft([1, 1, 1, 1])
    for val, exp in zip(X1, [4, 0, 0, 0]):
        approx(val, exp, tol=1e-12)
    X2 = dft([1, -1, 1, -1])
    for val, exp in zip(X2, [0, 0, 4, 0]):
        approx(val, exp, tol=1e-12)
    # FFT complex multiplications: (N/2)*log2(N) for N=16 -> 32; N=1024 -> 5120
    assert (16 // 2) * int(math.log2(16)) == 32
    assert (1024 // 2) * int(math.log2(1024)) == 5120
    # Zero padding: 100 + 29 - 1 = 128
    assert 100 + 29 - 1 == 128
    checks += 18

    # --- Ch 6: Digital Filter Models ---
    # Partial fraction check: 2/(1-0.5z^-1) - 1/(1-0.25z^-1) == 1/((1-0.5z^-1)(1-0.25z^-1))
    for z in [2.0 + 0j, 1.0 + 1j, -3.0 + 2j]:
        zi = 1 / z
        lhs = 1 / ((1 - 0.5 * zi) * (1 - 0.25 * zi))
        rhs = 2 / (1 - 0.5 * zi) - 1 / (1 - 0.25 * zi)
        approx(lhs, rhs)
    # Initial value theorem: (3 - 2z^-1)/(1 - 0.5z^-1) as z->inf -> 3
    approx((3 - 0) / (1 - 0), 3.0)
    # 1st-order IIR: H(z) = 0.1 / (1 - 0.9z^-1)
    # Pole z=0.9, |H(1)|=1, |H(-1)|=0.1/1.9 ≈ 0.05263
    approx(0.1 / (1 - 0.9), 1.0)
    approx(0.1 / (1 + 0.9), 1 / 19)
    # Boss IIR: H(z) = 0.2 / (1 - 0.8z^-1) -> pole 0.8, |H(1)|=1, |H(-1)|=1/9 ≈ 0.111
    approx(0.2 / (1 - 0.8), 1.0)
    approx(0.2 / (1 + 0.8), 1 / 9)
    # Symmetric FIR: L=9 -> 5 mults; L=11 -> 6 mults
    assert (9 + 1) // 2 == 5
    assert (11 + 1) // 2 == 6
    # SQNR: 6.02*B + 1.76 -> +4 bits -> +24.08 dB ≈ 24 dB; 16-bit -> 98.08 dB
    approx(4 * 6.02, 24.08)
    approx(6.02 * 16 + 1.76, 98.08)
    # 16-bit signed wrap-around: 25000 + 20000 = 45000 -> 45000 - 65536 = -20536
    assert ((25000 + 20000 + 32768) % 65536) - 32768 == -20536
    # 8-bit signed saturation: 90 + 60 = 150 -> clamped to 127 (wrap would be -106)
    assert min(127, max(-128, 90 + 60)) == 127
    assert ((90 + 60 + 128) % 256) - 128 == -106
    # Limit cycle: y[n] = round_half_away(-0.5 * y[n-1]), y[-1] = 1 -> -1, +1, -1, +1
    def round_half_away(v):
        return int(math.copysign(math.floor(abs(v) + 0.5), v))

    y = 1
    cycle = []
    for _ in range(4):
        y = round_half_away(-0.5 * y)
        cycle.append(y)
    assert cycle == [-1, 1, -1, 1]
    # Boss signal transform: x(t) on [-1, 5], y(t)=x(3t-1) -> [0, 2], duration=2
    approx((5 + 1) / 3 - (-1 + 1) / 3, 2.0)
    checks += 14

    # 2026-11-23 review: new numbers so the practice and the final challenge do not repeat the worked example
    assert discrete_conv([3, 1, 2], [1, -1]) == [3, -2, 1, -2]  # q-dt-conv-y2: y[2] = 1
    assert discrete_conv([1, 3, 2], [2, -1]) == [2, 5, 1, -2]  # boss-dt-conv: y[1] = 5
    assert alias_freq(900, 400) == 100  # boss-aliasing-calc
    for n in range(20):
        approx(math.cos(2 * math.pi * 900 / 400 * n), math.cos(2 * math.pi * 100 / 400 * n), tol=1e-9)
    # boss-lti-classify: x^2 nonlinear/TI, 3x[n-2] LTI, x[2n] linear/time-varying
    xs = [1, -2, 3, 0, 5, -1, 2, 4]
    sq = lambda x: [v * v for v in x]
    assert sq([2 * v for v in xs]) != [2 * v for v in sq(xs)]
    shift = lambda x, k: [0] * k + x[: len(x) - k]
    down = lambda x: x[0::2]
    assert down(shift(xs, 1)) != shift(down(xs), 1)
    checks += 4

    print(f"H.1.3 verify.py: all {checks} verification groups passed.")


if __name__ == "__main__":
    main()
