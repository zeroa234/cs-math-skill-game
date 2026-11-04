# Checks every number data/content/D.3.1.yaml states. Code the lessons show is run for real with pandas, NumPy and
# scikit-learn (versions printed below); numbers quoted from the sources' own data files (restaurants, DAWN, the
# Pennsylvania poll, the vaccine trial, crabs) are copied from the source notes and only their arithmetic is checked.
# usage: .venv/Scripts/python.exe -I tests/content/D.3.1.verify.py   (prints "N/N claims hold", exit 1 on a mismatch)
# The .venv needs numpy pandas scikit-learn matplotlib seaborn (pip install with PIP_CACHE_DIR on the project drive).
import inspect, io, math, sys, warnings
from itertools import combinations
import numpy as np, pandas as pd, sklearn

checks = []
def add(got, want, tol=1e-9):
    line = inspect.stack()[1].lineno
    if isinstance(want, float) or isinstance(got, float):
        ok = abs(float(got) - float(want)) <= tol
    else:
        ok = got == want
    checks.append((ok, got, want, line))
print("pandas", pd.__version__, "numpy", np.__version__, "scikit-learn", sklearn.__version__)

# ---------------- lifecycle / data-scope / protocols
add(144_000 * 0.01, 1440.0)
add(100 <= 108, True)

# ---------------- python-values
price, count = 8, 3; add(price * count, 24); add(price * 3, 24)
a = 5; b = a + 2; a = 100; add(b, 7)
add("8" + "1", "81"); add(8 + 1, 9); add("3" + "4", "34")
add(6 / 2, 3.0); add(type(6 / 2).__name__, "float")
add(8 > 3, True); add(8 == 3, False); add(31 > 30, True)

# ---------------- python-containers
temps = [21, 25, 19]; add(temps[0], 21); add(temps[-1], 19); add(len(temps), 3)
add([120, 98, 143, 87][2], 143)
day = {"date": "2024-07-01", "temp": 31, "rentals": 143}; add(day["temp"], 31)
add({"name": "杭州", "pop": 1252}["name"], "杭州")
add(len([3, 8, 5]), 3); add(round(3.14159, 2), 3.14); add(round(3.14159, ndigits=2), 3.14)
add(round(2.71828, 3), 2.718)
add("abc".upper(), "ABC"); add("a,b,c".split(","), ["a", "b", "c"]); add(str("a,b,c".split(",")), "['a', 'b', 'c']")
total = 0
for r in [120, 98, 143]: total = total + r
add(total, 361)
total = 0
for s in ["Ann", "Bo", "Cy"]: total = total + len(s)
add(total, 7); add([len(n) for n in ["Ann", "Bo", "Cy"]], [3, 2, 2])

# ---------------- file-formats / encoding-size
add(len("数据".encode("utf-8")), 6); add(len("data".encode("utf-8")), 4)
add(52_428_800 / 1024**2, 50.0); add(1024**2, 1_048_576); add(2 * 5, 10)
try:
    b"\x31\x39\x2c\xd1\x41".decode("utf-8"); add("decoded", "UnicodeDecodeError")
except UnicodeDecodeError as e:
    add("can't decode byte 0xd1" in str(e), True)

# ---------------- dataframe
df = pd.DataFrame({"date": ["07-01", "07-02", "07-03", "07-04"], "temp": [31, 28, 33, 35], "rentals": [143, 120, 151, 97]})
add(df.shape, (4, 3)); add(int(df["rentals"].sum()), 511); add(float(df["temp"].mean()), 31.75); add(int(df["temp"].sum()), 127)
add(str(df["temp"].dtype), "int64"); add(str(df["date"].dtype), "str")
try:
    df[0]; add("no error", "KeyError")
except KeyError:
    add("KeyError", "KeyError")
add(str(pd.DataFrame({"r": ["143", "暂无"]})["r"].dtype), "str")
nd = pd.DataFrame([{"a": 1, "b": 2}, {"b": 3, "c": 4}])
add(nd.isna().to_numpy().tolist(), [[False, False, True], [True, False, False]]); add(str(nd["a"].dtype), "float64"); add(nd["a"].iloc[0], 1.0)
add(int(pd.DataFrame([{"x": 1}, {"y": 2}, {"x": 3, "y": 4}]).isna().sum().sum()), 2)
add(pd.DataFrame({"a": range(365), "b": 0, "c": 0, "d": 0}).shape, (365, 4))

# ---------------- granularity
insp = pd.DataFrame({"business_id": [19, 19, 24, 24, 64859, 64859], "date": [20160513, 20171211, 20171101, 20161005, 20150924, 20150924], "score": [94, 94, 98, 98, 96, 91]})
add(len(insp), 6); add(insp["business_id"].nunique(), 3); add(int(insp.groupby(["business_id", "date"]).size().max()), 2)
v = pd.DataFrame({"sex": ["F", "M", "F", "M"], "wt": [1, 3, 1, 1]})
add(float(np.average(v.sex == "F")), 0.5); add(round(float(np.average(v.sex == "F", weights=v.wt)), 2), 0.33)
add(round(22 / 45, 2), 0.49); add(round(78 / 55, 2), 1.42)
add(round(52.3 - 48.0, 1) > 4, True)

# ---------------- json-http
ex = {"lender_id": "matt", "loan_count": 23, "status": [2, 1, 3], "sponsored": False, "sponsor_name": None, "lender_dem": {"sex": "m", "age": 77}}
add(ex["lender_dem"]["age"], 77)
flat = pd.json_normalize(ex); add(flat.shape[1], 7); add("lender_dem.sex" in flat.columns and "lender_dem.age" in flat.columns, True)
add(flat["status"].iloc[0], [2, 1, 3])
rj = pd.read_json(io.StringIO('{"site":["0014","0014"],"aqi":[30,null]}')); add(int(rj["site"].iloc[0]), 14)
rc = pd.read_csv(io.StringIO("site\n0014\n0102\n")); add(rc["site"].tolist(), [14, 102])
add(pd.read_csv(io.StringIO("site\n0014\n"), dtype={"site": str})["site"].iloc[0], "0014")

# ---------------- select
s = pd.Series([0.25, 0.5, 0.75, 1.0], index=["a", "b", "c", "d"])
add(list(s.loc["a":"c"].index), ["a", "b", "c"]); add(list(s.iloc[0:2].index), ["a", "b"])
add(len(s.loc["b":"d"]), 3); add(len(s.iloc[1:3]), 2)
d = pd.Series(["a", "b", "c"], index=[1, 3, 5]); add(d.loc[1], "a"); add(d.iloc[1], "b"); add(d.loc[3], "b")
try:
    d.iloc[3]; add("no error", "IndexError")
except IndexError:
    add("IndexError", "IndexError")
add(len(df[df["temp"] > 30]), 3); add(len(df[(df["temp"] > 30) & (df["rentals"] > 100)]), 2)
add(len(df.query("temp > 30 and rentals > 100")), 2)
add(df.loc[df["temp"] > 30, ["date", "rentals"]].shape, (3, 2))

# ---------------- quality
add(len("941033148"), 9); add("941033148"[:5], "94103")

# ---------------- missing
x = pd.Series([1, None, 3]); add(x.isna().tolist(), [False, True, False]); add(float(x.sum()), 4.0); add(float(x.mean()), 2.0)
add(bool(np.isnan(np.array([1, np.nan, 3]).sum())), True)
add(float(pd.Series([4, None, 8, None]).mean()), 6.0)
y3 = pd.Series([10, np.nan, 14]); add(y3.interpolate().tolist(), [10.0, 12.0, 14.0]); add(y3.ffill().tolist(), [10.0, 10.0, 14.0])
c = pd.Series([400.1, -99.99, 401.3]); add(round(float(c.replace(-99.99, np.nan).mean()), 2), 400.7); add(round(float(c.mean()), 1), 233.8)

# ---------------- text-time
with warnings.catch_warnings():
    warnings.simplefilter("error")
    dts = pd.to_datetime(pd.Series([20160513, 20171211]).astype(str), format="%Y%m%d")
    add(dts.dt.year.tolist(), [2016, 2017]); add(dts.dt.day_of_week.tolist(), [4, 0])
add(pd.to_datetime("20160513", format="%Y%m%d").day_of_week, 4); add(pd.to_datetime("20160513", format="%Y%m%d").day_name(), "Friday")
add(pd.Timestamp("2024-07-06").day_of_week, 5); add(pd.Timestamp("2024-07-07").day_of_week, 6)
add(int(pd.Series(["High risk vermin", "Unclean floor", "vermin noted"]).str.contains("vermin").sum()), 2)
add(pd.Series(["High risk vermin", "Unclean floor", "vermin noted"]).str.contains("vermin").tolist(), [True, False, True])
r3 = pd.Series([3, 6, 9, 12]).rolling(3).mean(); add(float(r3.iloc[-1]), 9.0); add(int(r3.isna().sum()), 2)
bk = pd.DataFrame({"date": pd.to_datetime(["2024-06-29", "2024-06-30", "2024-07-01", "2024-07-02"]), "rentals": [100, 120, 150, 130]})
add(bk.groupby(bk["date"].dt.to_period("M"))["rentals"].mean().tolist(), [110.0, 140.0])
add(pd.Series([3, 6, 9]).shift(1).tolist()[1:], [3.0, 6.0])
def add_dates(t):
    dd = pd.to_datetime(t["date"].astype(str), format="%Y%m%d")
    return t.assign(timestamp=dd, year=dd.dt.year)
add(insp.pipe(add_dates)["year"].tolist(), [2016, 2017, 2017, 2016, 2015, 2015])
add(list(insp.columns), ["business_id", "date", "score"])   # assign left the original alone

# ---------------- combine
A = pd.Series([2, 4, 6], index=[0, 1, 2]); B = pd.Series([1, 3, 5], index=[1, 2, 3])
ab = A + B; add(ab.index.tolist(), [0, 1, 2, 3]); add([None if math.isnan(v) else v for v in ab.tolist()], [None, 5.0, 9.0, None])
add(A.add(B, fill_value=0).tolist(), [2.0, 5.0, 9.0, 5.0])
cc = pd.concat([pd.DataFrame({"x": [1, 2]}), pd.DataFrame({"x": [3, 4]})]); add(cc.index.tolist(), [0, 1, 0, 1]); add(len(cc.loc[0]), 2)
add(pd.concat([pd.DataFrame({"x": [1, 2]}), pd.DataFrame({"x": [3, 4]})], ignore_index=True).index.tolist(), [0, 1, 2, 3])
left = pd.DataFrame({"business_id": [19, 24, 31, 45]})
right = pd.DataFrame({"business_id": [19, 19, 24, 31, 99], "score": [94, 94, 98, 90, 80]})
add(len(pd.merge(left, right, on="business_id")), 4); add(len(pd.merge(left, right, on="business_id", how="left")), 5)
try:
    pd.merge(pd.DataFrame({"site": ["0014"]}), pd.DataFrame({"site": [14], "aqi": [30]}), on="site"); add("merged", "ValueError")
except ValueError as e:
    add("trying to merge on str and int64 columns for key 'site'" in str(e), True)

# ---------------- reshape
w = pd.DataFrame({"Yr": [1959, 1960], **{m: [315.0 + m, 316.0 + m] for m in range(1, 13)}})
lg = w.melt(id_vars=["Yr"], var_name="month", value_name="average"); add(lg.shape, (24, 3))
add(pd.pivot_table(lg, index="Yr", columns="month", values="average").shape, (2, 12))
g = pd.DataFrame({"city": ["A", "A", "B", "B"], "year": [2023, 2024, 2023, 2024], "rentals": [10, 12, 7, 9]}).groupby(["city", "year"])["rentals"].sum()
add(g.tolist(), [10, 12, 7, 9]); add(g.unstack().shape, (2, 2)); add(g.loc["A"].tolist(), [10, 12])
counties = pd.Series([100, 200, 300]); add(int(counties.sum() + counties.sum()), 2 * 600)

# ---------------- summary
x6 = pd.Series([2, 3, 3, 4, 5, 100]); add(float(x6.mean()), 19.5); add(int(x6.sum()), 117); add(float(x6.median()), 3.5)
add(float(pd.Series([2, 3, 3, 4, 5, 1000]).mean()), 169.5); add(float(pd.Series([2, 3, 3, 4, 5, 1000]).median()), 3.5)
add(float(x6.quantile(0.25)), 3.0); add(float(x6.quantile(0.75)), 4.75); add(0.25 * 5, 1.25); add(0.75 * 5, 3.75)
iqr = 4.75 - 3; add(iqr, 1.75); add(4.75 + 1.5 * iqr, 7.375); add(1.5 * iqr, 2.625); add(3 - 1.5 * iqr, 0.375)
x7 = pd.Series([1, 2, 4, 4, 5, 7, 30]); add(float(x7.median()), 4.0); add(int(x7.sum()), 53); add(round(float(x7.mean()), 2), 7.57)
add(float(x7.quantile(0.25)), 3.0); add(float(x7.quantile(0.75)), 6.0); add(0.75 * 6, 4.5); add(6 + 1.5 * 3, 10.5)
h = np.array([189, 170, 189, 163, 183, 171, 185, 168, 173, 183, 173, 173, 175, 178, 183, 193, 178, 173, 174, 183, 183, 168, 170, 178, 182, 180, 183, 178, 182, 188, 175, 179, 183, 193, 182, 183, 177, 185, 188, 188, 182, 185])
add(len(h), 42); add(round(h.mean(), 1), 179.7); add(int(h.min()), 163); add(int(h.max()), 193)
add(float(np.percentile(h, 25)), 174.25); add(float(np.median(h)), 182.0); add(float(np.percentile(h, 75)), 183.0)
add(round(float(h.std()), 2), 6.93); add(round(float(pd.Series(h).std()), 2), 7.02); add(round(float(h.std()), 1), 6.9)
add(float(np.var([2, 4, 6])), 8 / 3, 1e-9); add(round(float(np.std([2, 4, 6])), 2), 1.63)
add(float(pd.Series([1, 2, 3]).corr(pd.Series([2, 4, 6]))), 1.0, 1e-12); add(float(pd.Series([1, 2, 3, 4]).corr(pd.Series([4, 3, 2, 1]))), -1.0, 1e-12)
add(float(pd.Series([-2, -1, 0, 1, 2]).corr(pd.Series([4, 1, 0, 1, 4]))), 0.0, 1e-12)

# ---------------- groupby
wd = pd.DataFrame({"weather": ["晴", "雨", "晴", "阴", "雨", "晴"], "rentals": [150, 60, 130, 100, 80, 140]})
gm = wd.groupby("weather")["rentals"].mean(); add(gm.to_dict(), {"晴": 140.0, "阴": 100.0, "雨": 70.0}); add(list(gm.index), ["晴", "阴", "雨"])
add(int(wd.groupby("weather")["rentals"].sum()["雨"]), 140)
ag = wd.groupby("weather")["rentals"].agg(["mean", "max", "count"]); add(ag.loc["晴"].tolist(), [140.0, 150.0, 3.0]); add(ag.loc["阴"].tolist(), [100.0, 100.0, 1.0]); add(ag.loc["雨"].tolist(), [70.0, 80.0, 2.0])
tm = wd.groupby("weather")["rentals"].transform("mean"); add(tm.tolist(), [140.0, 70.0, 140.0, 100.0, 70.0, 140.0])
add((wd["rentals"] - tm).tolist(), [10.0, -10.0, -10.0, 0.0, 10.0, 0.0])
add(len(wd.groupby("weather").filter(lambda q: len(q) >= 2)), 5)
kk = pd.DataFrame({"weather": ["晴", "雨", "晴", "雨"], "rentals": [150, 60, 130, 80]}); add(float(kk.groupby("weather")["rentals"].mean()["晴"]), 140.0)

# ---------------- pivot (Titanic counts: survivors per cell are the source's aggfunc=sum table; class sizes from the same dataset)
surv = {("female", "First"): (91, 94), ("female", "Second"): (70, 76), ("female", "Third"): (72, 144), ("male", "First"): (45, 122), ("male", "Second"): (17, 108), ("male", "Third"): (47, 347)}
want = {("female", "First"): 0.968085, ("female", "Second"): 0.921053, ("female", "Third"): 0.5, ("male", "First"): 0.368852, ("male", "Second"): 0.157407, ("male", "Third"): 0.135447}
for k, (sv, nn) in surv.items(): add(round(sv / nn, 6), want[k])
add(round(91 / 94, 3), 0.968); add(round((91 + 70 + 72) / (94 + 76 + 144), 3), 0.742); add(sum(nn for _, nn in surv.values()), 891)
add(sum(sv for sv, _ in surv.values()), 342); add(round(342 / 891, 3), 0.384)
add(round(70 / 76, 3), 0.921); add(round(45 / 122, 3), 0.369); add(round(17 / 108, 3), 0.157); add(round(47 / 347, 3), 0.135)

# ---------------- histogram
cnts, edges = np.histogram([1, 2, 2, 3, 3, 3], bins=3); add(cnts.tolist(), [1, 2, 3]); add([round(e, 1) for e in edges.tolist()], [1.0, 1.7, 2.3, 3.0])
cnts, edges = np.histogram([1, 2, 2, 3, 3, 3, 10], bins=3); add(cnts.tolist(), [6, 0, 1]); add(edges.tolist(), [1.0, 4.0, 7.0, 10.0])

# ---------------- figure-parts
add((71 - 2.5, 71 + 2.5), (68.5, 73.5)); add((74 - 5, 74 + 5), (69, 79)); add(max(68.5, 69) < min(73.5, 79), True)
add(np.arange(6).reshape(2, 3)[1, 2], 5)   # axes[1, 2] is the second row, third column

# ---------------- numpy
arr = np.array([3.14, 4, 2, 3]); add(str(arr.dtype), "float64"); add(arr[1], 4.0)
gg = np.arange(12).reshape(3, 4); add((gg.shape, gg.ndim, gg.size), ((3, 4), 2, 12)); add(int(gg[1, 2]), 6); add(int(gg[2, 1]), 9)
xi = np.array([5, 0, 3]); xi[0] = 3.14159; add(xi.tolist(), [3, 0, 3])
xj = np.array([1, 2, 3]); xj[1] = 7.9; add(int(xj[1]), 7)
sv = gg[:2, :2]; sv[0, 0] = 99; add(int(gg[0, 0]), 99)
z = np.zeros(5); bz = z[1:3]; bz[0] = 8; add(float(z[1]), 8.0)

# ---------------- ufuncs
xa = np.array([1, 4, 2, 5, 3]); add((xa * 2).tolist(), [2, 8, 4, 10, 6]); add(round(float(np.sin(np.pi)), 18) != 0, True); add(f"{np.sin(np.pi):.2e}", "1.22e-16")
add((np.array([1, 2, 3]) ** 2 + 1).tolist(), [2, 5, 10])
M = np.array([[1, 2, 3], [4, 5, 6]]); add(int(M.sum()), 21); add(M.sum(axis=0).tolist(), [5, 7, 9]); add(M.max(axis=1).tolist(), [3, 6])
add(np.array([[1, 2], [3, 4], [5, 6]]).sum(axis=0).tolist(), [9, 12])
add((xa > 2).tolist(), [False, True, False, True, True]); add(int(np.sum(xa > 2)), 3); add(xa[(xa > 1) & (xa < 5)].tolist(), [4, 2, 3])
x9 = np.array([3, 8, 1, 9, 4, 7]); add(int(np.sum((x9 > 3) & (x9 < 9))), 3)
try:
    xa[(xa > 1) and (xa < 5)]; add("no error", "ValueError")
except ValueError:
    add("ValueError", "ValueError")
add(round(104 / 0.442), 235)
add(int(np.sum(np.array([5, 12, 7, 20, 3]) > 6)), 3)

# ---------------- sklearn
from sklearn.linear_model import LinearRegression
rng = np.random.RandomState(42); xs = 10 * rng.rand(50); ys = 2 * xs - 1 + rng.randn(50)
add(xs.shape, (50,)); add(xs.reshape(-1, 1).shape, (50, 1))
lr = LinearRegression(fit_intercept=True).fit(xs.reshape(-1, 1), ys)
add(round(float(lr.coef_[0]), 2), 1.98); add(round(float(lr.intercept_), 2), -0.90); add(round(float(lr.predict([[5]])[0]), 1), 9.0); add(round(1.98 * 5 - 0.90, 2), 9.0)
add(round(float(lr.predict([[5]])[0]), 3), 8.985)
add((1797, 64), (1797, 64))

# ---------------- urn
pairs = list(combinations("bbbww", 2)); add(len(pairs), 10); add(sum(p[0] == p[1] for p in pairs), 4); add(4 / 10, 0.4)
add(len(list(combinations("ABCDEFG", 3))), 35); add(sum("A" in c for c in combinations("ABCDEFG", 3)), 15); add(6 * 5 // 2, 15)
tanks = [1, 1, 0, 1, 0, 1, 0]; dist = {}
for c in combinations(range(7), 3):
    k = sum(tanks[i] for i in c); dist[k] = dist.get(k, 0) + 1
add(dist, {0: 1, 1: 12, 2: 18, 3: 4}); add(round(1 / 35, 2), 0.03); add(round(12 / 35, 2), 0.34); add(round(18 / 35, 2), 0.51); add(round(4 / 35, 2), 0.11)
add(round(22 / 35, 2), 0.63); add(round(4 / 7, 2), 0.57)
add(abs(0.4032 - 0.4) < 0.01, True)

# ---------------- poll-bias (simulation results copied from B 3.2; check the arithmetic)
add(round(0.4818 - 0.4746, 4), 0.0072); add(100 - 61, 39)
add(round(0.60613 * 100), 61); add(round(0.44967 * 100), 45); add(round(0.78968 * 100), 79); add(round(0.36935 * 100), 37); add(12_000 / 1_500, 8.0)

# ---------------- trial-air
add(43_738 - 468, 43_270); add(43_738 // 2, 21_869); add(117 + 351, 468); add(468 / 2, 234.0)
add(round((1 - 117 / 351) * 100, 1), 66.7)
add(round(0.687 / 6.6 * 100), 10); add(round(0.687 / 8.6 * 100), 8); add(round(0.687 / 5.4 * 100, 1), 12.7)
add(3 * 15, 45)

# ---------------- train-test
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score, LeaveOneOut, KFold
Xi, yi = load_iris(return_X_y=True); add(len(Xi), 150)
k1 = KNeighborsClassifier(n_neighbors=1).fit(Xi, yi); add(float(accuracy_score(yi, k1.predict(Xi))), 1.0)
X1, X2, y1, y2 = train_test_split(Xi, yi, random_state=0, train_size=0.5)
a2 = accuracy_score(y2, KNeighborsClassifier(n_neighbors=1).fit(X1, y1).predict(X2)); add(round(float(a2), 3), 0.907); add(int(round(a2 * 75)), 68); add(round(68 / 75, 3), 0.907)
add(99 - 22, 77); add(round(22 / 99 * 100), 22)
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
Xr, yr = make_regression(random_state=42, n_features=1, noise=1)
Xtr, Xte, ytr, yte = train_test_split(Xr, yr, test_size=0.4, random_state=42)
sc = StandardScaler(); mr = LinearRegression().fit(sc.fit_transform(Xtr), ytr)
e_bad = mean_squared_error(yte, mr.predict(Xte)); e_ok = mean_squared_error(yte, mr.predict(sc.transform(Xte)))
add(round(float(e_bad), 2), 62.81); add(round(float(e_ok), 2), 0.90); add(round(62.80 / 0.90), 70)

# ---------------- pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.pipeline import make_pipeline
rg = np.random.RandomState(42); Xb = rg.standard_normal((200, 10000)); yb = rg.choice(2, 200)
Xsel = SelectKBest(k=25).fit_transform(Xb, yb); a_, b_, c_, d_ = train_test_split(Xsel, yb, random_state=42)
add(float(accuracy_score(d_, HistGradientBoostingClassifier(random_state=1).fit(a_, c_).predict(b_))), 0.76)
Xtr, Xte, ytr, yte = train_test_split(Xb, yb, random_state=42)
pp = make_pipeline(SelectKBest(k=25), HistGradientBoostingClassifier(random_state=1)).fit(Xtr, ytr)
add(float(accuracy_score(yte, pp.predict(Xte))), 0.5)
scs = cross_val_score(make_pipeline(SelectKBest(k=25), HistGradientBoostingClassifier(random_state=1)), Xb, yb)
add(f"{scs.mean():.2f}+/-{scs.std():.2f}", "0.43+/-0.05")
add(round((0.76 - 0.5) * 100), 26)
from sklearn.impute import SimpleImputer
Xm = np.array([[np.nan, 0, 3], [3, 7, 9], [3, 5, 2], [4, np.nan, 6], [8, 8, 1]])
add(SimpleImputer(strategy="mean").fit_transform(Xm)[0, 0], 4.5); add(SimpleImputer(strategy="mean").fit_transform(Xm)[3, 1], 5.0)
from sklearn.preprocessing import OneHotEncoder
cities = np.array([["北京"], ["上海"], ["杭州"], ["南京"], ["成都"], ["北京"]])
oh = OneHotEncoder().fit_transform(cities).toarray(); add(oh.shape[1], 5); add(oh.sum(axis=1).tolist(), [1.0] * 6)
from sklearn.feature_extraction import DictVectorizer
dv = DictVectorizer(sparse=False, dtype=int).fit([{"neighborhood": "Queen Anne"}, {"neighborhood": "Fremont"}, {"neighborhood": "Wallingford"}])
add(dv.transform([{"neighborhood": "Queen Anne"}, {"neighborhood": "Fremont"}]).tolist(), [[0, 1, 0], [1, 0, 0]])

# ---------------- confusion
add(990 / 1000, 0.99)
add(0.9, 0.9)
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, r2_score, mean_absolute_error
yt = [0, 0, 0, 1, 1, 1, 1, 1]; yp = [0, 1, 0, 1, 0, 1, 0, 1]
add(confusion_matrix(yt, yp).ravel().tolist(), [2, 1, 2, 3]); add(float(accuracy_score(yt, yp)), 0.625)
add(float(accuracy_score([0, 1, 2, 3], [0, 2, 1, 3])), 0.5); add(float(accuracy_score([0, 1, 2, 3], [0, 2, 1, 3], normalize=False)), 2.0)
add(377 + 49 + 104 + 129, 659); add(round((377 + 129) / 659, 3), 0.768)
add(int(sum(p > 0.4 for p in [0.2, 0.45, 0.6, 0.9])), 3); add(int(sum(p > 0.5 for p in [0.2, 0.45, 0.6, 0.9])), 2)
add(round(0.65 + 0.35, 2), 1.0)

# ---------------- precision-recall
add(float(precision_score([0, 1, 0, 1], [0, 1, 0, 0])), 1.0); add(float(recall_score([0, 1, 0, 1], [0, 1, 0, 0])), 0.5)
add(round(float(f1_score([0, 1, 0, 1], [0, 1, 0, 0])), 3), 0.667)
TP, FP, FN, TN = 40, 60, 10, 890; P = TP / (TP + FP); R = TP / (TP + FN)
add(P, 0.4); add(R, 0.8); add(round(2 * P * R / (P + R), 3), 0.533); add((TP + TN) / 1000, 0.93); add((P + R) / 2, 0.6, 1e-12)
add(round(2 * 1.0 * 0.5 / 1.5, 3), 0.667); add((1.0 + 0.5) / 2, 0.75)
add(TP + FP + FN + TN, 1000)

# ---------------- roc
add(round(1 - 0.70, 2), 0.3)
yy = np.array([0, 0, 1, 1]); sco = np.array([0.1, 0.4, 0.35, 0.8])
add(float(roc_auc_score(yy, sco)), 0.75)
fpr, tpr, th = roc_curve(yy, sco); add(fpr.tolist(), [0.0, 0.0, 0.5, 0.5, 1.0]); add(tpr.tolist(), [0.0, 0.5, 0.5, 1.0, 1.0])
add(float(roc_auc_score(yy, 1 - sco)), 0.25)   # scoring the other column gives 1 - AUC

# ---------------- regression-metrics
yt4 = [3, -0.5, 2, 7]; yp4 = [2.5, 0.0, 2, 8]
add(float(mean_absolute_error(yt4, yp4)), 0.5); add(float(mean_squared_error(yt4, yp4)), 0.375); add(round(float(np.sqrt(0.375)), 3), 0.612)
add(round(float(r2_score(yt4, yp4)), 3), 0.949); add(float(r2_score(yt4, [np.mean(yt4)] * 4)), 0.0)
add(round(float(mean_absolute_error([10, 20, 30], [12, 18, 33])), 2), 2.33); add(round(float(mean_squared_error([10, 20, 30], [12, 18, 33])), 2), 5.67)
add(float(mean_absolute_error(yt4 + [10], yp4 + [0])), 2.4); add(round(float(mean_squared_error(yt4 + [10], yp4 + [0])), 1), 20.3)

# ---------------- overfitting / cross-validation
from sklearn.preprocessing import PolynomialFeatures
rs = np.random.RandomState(0); xo = np.sort(rs.uniform(10, 80, 40)); yo = 200 - 2.5 * xo + rs.normal(0, 10, 40)
tr = [mean_squared_error(yo, LinearRegression().fit(PolynomialFeatures(d, include_bias=False).fit_transform((xo[:, None] - 45) / 35), yo).predict(PolynomialFeatures(d, include_bias=False).fit_transform((xo[:, None] - 45) / 35))) for d in range(1, 13)]
add(all(tr[i + 1] <= tr[i] + 1e-6 for i in range(11)), True)   # training MSE never rises as the degree grows
add(75 // 3 * 2, 50)
cv5 = cross_val_score(KNeighborsClassifier(n_neighbors=1), Xi, yi, cv=5); add([round(float(v), 3) for v in cv5], [0.967, 0.967, 0.933, 0.933, 1.0]); add(round(float(cv5.mean()), 2), 0.96)
add(round(float(cross_val_score(KNeighborsClassifier(n_neighbors=1), Xi, yi, cv=LeaveOneOut()).mean()), 2), 0.96)
add(150 // 5, 30)
add(round(sum([0.80, 0.85, 0.90, 0.75, 0.85]) / 5, 3), 0.83); add(4 * 5, 20); add(120 // 4 * 3, 90)

# ---------------- randomness
from sklearn.datasets import make_classification
r0 = np.random.RandomState(0); Xc, yc = make_classification(random_state=r0); rf = RandomForestClassifier(random_state=r0)
a_, b_, c_, d_ = train_test_split(Xc, yc, random_state=r0); add(float(rf.fit(a_, c_).score(b_, d_)), 0.84)
add([round(float(v), 2) for v in cross_val_score(RandomForestClassifier(random_state=123), Xc, yc)], [0.85, 0.95, 0.95, 0.9, 0.9])
add([round(float(v), 2) for v in cross_val_score(RandomForestClassifier(random_state=np.random.RandomState(0)), Xc, yc)], [0.9, 0.95, 0.95, 0.9, 0.9])
add(round((0.85 + 0.95 + 0.95 + 0.9 + 0.9) / 5, 2), 0.91); add(round((0.9 + 0.95 + 0.95 + 0.9 + 0.9) / 5, 2), 0.92)
X10 = np.arange(10).reshape(-1, 1)
cvi = KFold(n_splits=2, shuffle=True, random_state=np.random.RandomState(0))
add([te.tolist() for _, te in cvi.split(X10)][0], [1, 2, 4, 8, 9]); add([te.tolist() for _, te in cvi.split(X10)][0], [1, 2, 3, 5, 9])
cv0 = KFold(n_splits=2, shuffle=True, random_state=0); add([te.tolist() for _, te in cv0.split(X10)], [te.tolist() for _, te in cv0.split(X10)])

# ---------------- three-distributions / bootstrap / hypothesis-test / prediction-interval
add(round(0.21 + 1.96 * 0.027, 3), 0.263); add(round(0.21 - 1.96 * 0.027, 3), 0.157)
add(math.sqrt(400) / math.sqrt(100), 2.0)
boot = np.random.RandomState(1).choice(np.arange(100), size=100, replace=False); add(sorted(boot.tolist()), list(range(100)))
add(float(np.mean(np.arange(1, 201))), 100.5); add((1 + 200) / 2, 100.5)
add(round(0.00052 * 100, 3), 0.052)
add(40 * 0.05, 2.0); add(20 * 0.05, 1.0)
add(round(11.07 / math.sqrt(452), 2), 0.52); add(round(math.sqrt(452), 2), 21.26); add(round(1.96 * 11.07 / math.sqrt(452), 2), 1.02)
add(round(11.07 * math.sqrt(1 + 1 / 452), 2), 11.08); add(round(math.sqrt(1 + 1 / 45_200), 5), 1.00001)
add(15.63 < 15.86 < 16.08 and 12.48 < 15.86 < 19.24, True); add(round(19.24 - 12.48, 2) > round(16.08 - 15.63, 2), True)

# ---------------- experiments / boss
add(0.989 > 0.988, True); add(round(0.989 - 0.988, 3), 0.001)
add(3 * 1024**3 / 1024**3 * 5, 15.0)
lt = pd.DataFrame({"site": ["A", "B", "C"]}); rt = pd.DataFrame({"site": ["A", "A", "B", "D"], "v": [1, 2, 3, 4]}); add(len(pd.merge(lt, rt, on="site", how="left")), 4)

# ---------------- line-scatter / histogram / figure-parts: the plotting calls the lessons name
import os
os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.path.dirname(__file__), "..", "..", "temp", "mpl"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, seaborn as sns
fig, ax = plt.subplots(); add(hasattr(ax, "xlabel"), False); add(hasattr(ax, "set_xlabel"), True)
add(all(hasattr(ax, n) for n in ("errorbar", "fill_between", "scatter", "hist")) and all(hasattr(plt, n) for n in ("hist2d", "contour")), True)
ax.plot([1, 2], [3, 4]); ax.plot([1, 2], [4, 3]); add(len(ax.get_lines()), 2); add(ax.get_lines()[0].get_color() != ax.get_lines()[1].get_color(), True)
with warnings.catch_warnings():
    warnings.simplefilter("ignore"); add(len(ax.legend().get_texts()), 0)   # no label= → empty legend
ax.plot([1, 2], [1, 1], "-g"); add((ax.get_lines()[-1].get_color(), ax.get_lines()[-1].get_linestyle()), ("g", "-"))
fig, axes = plt.subplots(2, 3, sharex="col"); add(axes.shape, (2, 3))
add(all(hasattr(sns, n) for n in ("histplot", "boxplot", "pairplot")), True)

bad = [(ln, g, w) for (ok, g, w, ln) in checks if not ok]
for i, g, w in bad:
    print(f"line {i}: got {g!r}, want {w!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
sys.exit(1 if bad else 0)
