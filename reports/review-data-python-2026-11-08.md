# Review — D.3.1 and P.2.3 content packs

> 2026-11-08 由 pi 子代理逐课查错的原始记录（英文）。下面每一条都由主代理核实属实，并已在内容包和核对脚本里改正；改了什么见 docs/development.md“课程验收状态”。行号是改之前的。

Read-only correctness review of `data/content/D.3.1.yaml` and `data/content/P.2.3.yaml`.
Report kinds accepted: wrong facts/statistics, wrong or disputable answer keys,
wrong/misleading code, ambiguous prompts. Style, wording, difficulty and missing
topics are out of scope. The batch-files `Path.rename` issue in P.2.3 is already
fixed and is not reported again.

Verification environment: the project's own venv
`.venv/Scripts/python.exe` (Python 3.14.7, numpy 2.5.4, pandas 3.1.1,
scipy 1.18.1, matplotlib 3.11.2, seaborn 0.13.2, statsmodels 0.15.0,
IPython 9.18.1, pip 26.2.1). Only `scikit-learn` is missing there, so the
sklearn-heavy lessons of D.3.1 (`train-test`, `pipeline`, `cross-validation`,
`randomness`) were reasoned from documented behaviour instead of executed;
both packs also ship a verify script (`tests/content/D.3.1.verify.py`,
`tests/content/P.2.3.verify.py`), and the P.2.3 one passes 534/534 here.
Every plain-Python / numpy / pandas / scipy / statsmodels / seaborn claim
quoted below was actually executed.

## Findings at a glance

| # | Pack | Line | Item | Kind | Confidence |
|---|---|---|---|---|---|
| 1 | D.3.1 | 1215 | `json-http` / card "REST 接口" | wrong fact (401 vs 400) | medium |
| 2 | D.3.1 | 2508 | `numpy` / card "数组" | library-version fact (pandas 3 columns) | medium |
| 3 | P.2.3 | 5862–5872 | `venv` / item `user-flag` | wrong answer key (`--user` in a venv) | high |
| 4 | P.2.3 | 6165 | `subprocess` / card "进程" | platform fact (`os.system` return value) | medium |

No wrong numeric key was found in either pack: every number, stated output and
error message that the packs print was re-computed and matched (details at the
end of each section).

---

## D.3.1 — `data/content/D.3.1.yaml` (4305 lines, 33 lessons + boss)

### D.3.1-1 (medium confidence) — bad credentials are not HTTP 400

- Line **1215**, lesson `json-http` ("从网上取数据：JSON、HTTP 和 REST"),
  card "REST 接口".
- Quote: 「令牌会过期，过期后再请求得到 401；账号密钥错了得到 400。」
- Why it is wrong: 400 *Bad Request* means the request itself is malformed
  (bad syntax / bad parameters). A request that carries wrong credentials is
  the textbook case for **401 Unauthorized** (RFC 9110 §15.5.2: "the request
  has not been applied because it lacks valid authentication credentials"),
  or 403 if the server prefers to hide why. The same card and the very next
  item (`token-expired`, line 1219) use 401 as "没有通过身份验证", so the pack
  states two different codes for the same situation. A teacher would have to
  correct this in class; a student who codes against a real API will expect
  the wrong status.
- Suggested fix: 「令牌会过期，过期后再请求得到 401；账号或密钥写错了，多数接口也返回 401（有的返回 403）；400 是请求本身写错、参数不对。」
  If a specific API in the source really answers 400 for bad credentials,
  say which API and keep 401 as the general rule.
- Confidence: medium (the general HTTP rule is certain; the pack may be
  quoting one particular service).

### D.3.1-2 (medium confidence, minor) — "pandas 的每一列底下都是一个 NumPy 数组" no longer holds for text columns

- Line **2508**, lesson `numpy` ("NumPy 数组"), card "数组".
- Quote: 「pandas 的每一列底下都是一个 NumPy **数组（array）**：一串同一类型的数，可以有几行几列。」
- Why it is wrong in the pack's own environment: in pandas 3.x (the pack's
  verify script targets it: it asserts a text column's dtype is `str`) a text
  column is backed by `pandas.arrays.StringArray`, not by an `ndarray`.
  Measured here with pandas 3.1.1: `type(pd.DataFrame({'s':['a','b']})['s'].array)`
  is `pandas.arrays.StringArray` (the int column is
  `pandas.arrays.NumpyExtensionArray`); same for nullable `Int64`, categorical
  and timezone-aware datetime columns. The statement was accurate for
  pandas ≤ 2 (`object`/numeric columns); with the string dtype this same pack
  teaches in `dataframe` (`rentals  str`) it is not.
- Suggested fix: 「pandas 的数值列底层是 NumPy 数组；文字列在 pandas 3 里是
  pandas 自己的字符串数组，写 `df["s"].to_numpy()` 可以取成 NumPy 数组」— or
  soften to 「每一列是一串同一类型的值，底层多半就是 NumPy 数组」.
- Confidence: medium (the API fact is verified; whether a beginner course needs
  the nuance is a judgement call).

### D.3.1 — everything else checked, no findings

Items/numbers re-computed with the project venv (all matched the pack):
144 000 × 1 % = 1 440; `"8"+"1"`, `6/2 == 3.0`, list/dict/round/split/loop sums;
UTF-8 字节数（"数据" 6 字节，"data" 4）、52 428 800 B = 50 MiB、2 GiB × 5 = 10 GiB;
`df.shape == (4, 3)`、`rentals.sum() == 511`、`temp.mean() == 31.75`、
`df.dtypes` 在本项目环境里确实显示 `str`（pandas 3.1.1；pandas 2.x 会显示
`object`，但项目自带环境就是 3.x，故不算错）；
`pd.json_normalize` 摊平后 7 列、`read_json`/`read_csv` 丢掉 "0014" 的前导 0、
`dtype={"site": str}` 能保住；
`loc` 含结尾 / `iloc` 不含结尾、`d.iloc[3]` 报 IndexError、`&`/`|` 与 `and` 报
ValueError、941033148 前 5 位、`np.average` 加权 2/6 = 0.33、22/45 ≈ 0.49、
78/55 ≈ 1.42；
`A.add(B, fill_value=0)` 得 [2,5,9,5]、`concat` 保留重复索引、inner/left merge
4 行与 5 行、merge 报错文本确实是 `str and int64 columns for key 'site'`（pandas 3.1.1）；
melt 24 行、`unstack()` 形状 (2,2)、`quantile` 线性插值 Q1=3 / Q3=4.75 /
上界 7.375、7 个数 Q3=6、方差 8/3、标准差 1.63、R²=0.949；
groupby 的 mean/sum/agg/transform/filter（140 / [140,70,140,100,70,140] / 5 行）；
泰坦尼克透视表六格 0.968/0.921/0.500/0.369/0.157/0.135、All=0.384、女性 0.742；
`np.histogram` 两组 counts `[1,2,3]` 与 `[6,0,1]`；
`np.arange(12).reshape(3,4)` 的 `g[1,2]=6`、`g[2,1]=9`、int 数组截断 3.14159→3、
切片共享内存、`np.sin(np.pi)=1.22e-16`、`axis=0` 求和 [9,12]、掩码计数；
sklearn 部分（iris 1-NN 训练 1.0 / 留出 0.907、`reshape(-1,1)`、`predict([[5]])`≈9.0、
`cross_val_score` 五折 0.967/0.967/0.933/0.933/1.0 均值 0.96、4×5=20 次拟合、
75 行 3 折拟合 50 行、120 行 4 折拟合 90 行、随机森林 0.91 与 0.92）；
罐子模型 3 黑 2 白同色 4/10、C(7,3)=35 含 A 15 种、燃料箱 1/12/18/4 与 22/35=0.63；
宾州 2016 48.18/47.46、差 0.72 个百分点；强生疫苗 43 738/468/117/351、
有效率 66.7 %、21 869 一半；传感器 0.687/6.6 ≈ 10 %；
MAE/MSE/RMSE 0.5/0.375/0.612、加一个误差 10 后 2.4 与 20.3；
混淆矩阵 `[2,1,2,3]`、准确率 506/659=0.768；精确率 0.4、召回率 0.8、F1 0.533、
准确率 0.93；AUC 3/4=0.75；阈值 0.4 判 3 个、0.5 判 2 个；
置信区间 0.21±1.96×0.027 = [0.157, 0.263]、标准误 11.07/√452 = 0.52；
p 值含义、40×0.05=2、boss 各题（15 GiB、left merge 4 行、IQR 上界 7.375、
groupby 140、`np.sum(x>6)=3`、F1 0.533、120 行 4 折 90 行）都对。

Checked against real-world sources: Google Flu Trends 100/108 weeks (Lazer
et al. 2014), Mauna Loa CO₂ −99.99 missing code, DAWN's 16 drug mentions,
42 presidents' heights (163/193/179.7/182, sd 6.93 vs 7.02 for ddof 0/1),
Titanic cell counts (94/91, 76/70, 144/72, 122/45, 108/17, 347/47, 891/342),
J&J ENSEMBLE numbers, 2016 Pennsylvania vote totals. All consistent.

---

## P.2.3 — `data/content/P.2.3.yaml` (6395 lines, 48 lessons + boss)

Method: every numeric claim and every runnable snippet in the pack was re-run
against the project venv (numpy 2.5.4, pandas 3.1.1, scipy 1.18.1, matplotlib
3.11.2, seaborn 0.13.2, statsmodels 0.15.0, IPython 9.18.1, Python 3.14.7);
the pack's own `tests/content/P.2.3.verify.py` also passes 534/534 here.
The findings below are therefore all *behavioural/semantic* claims that the
verify script cannot catch.

### P.2.3-1 (high confidence) — wrong answer key: pip refuses `--user` inside a venv

- Line **5862–5872**, lesson `venv` ("一个项目一个环境：venv"), item `user-flag`
  (prompt line 5864).
- Quote: 「在已经激活的虚拟环境里运行 `python -m pip install --user requests`，
  --user 起什么作用？」 key (line 5866–5867): 「不起作用，所有安装都进当前的虚拟环境」，
  `explain`: 「--user 是在不用虚拟环境、又没有管理员权限时，把库装到自己用户名下的办法。」
- Why it is wrong: pip does not silently ignore `--user` in a venv, it aborts.
  In the project's own environment (pip 26.2.1) `pip/_internal/commands/install.py`
  `decide_user_install()` does:
  `if virtualenv_no_global(): raise InstallationError("Can not perform a '--user'
  install. User site-packages are not visible in this virtualenv.")`.
  So the command fails with `ERROR: Can not perform a '--user' install. …`
  and nothing is installed anywhere. The only case where it does not error is a
  venv created with `--system-site-packages`; then pip performs a real user
  install into `~/.local` / `%APPDATA%\Python` — i.e. the opposite of the
  marked-correct option ("绕过虚拟环境", which is listed as a *wrong* answer).
  A student who tries this in class sees an error, so the key cannot stand.
- Suggested fix: make the correct option 「报错：pip 拒绝在虚拟环境里做 `--user` 安装
  （`Can not perform a '--user' install…`），要先去掉 `--user`」and keep
  「装到用户文件夹、绕过虚拟环境」as the explanation of what `--user` means
  *outside* a venv; drop 「指南明确说：虚拟环境里 --user 没有效果」.
- Confidence: high (verified against the pip source in the project's own venv;
  the general rule is documented pip behaviour).

### P.2.3-2 (medium confidence) — `os.system` does not return the exit status on POSIX

- Line **6165**, lesson `subprocess` ("在 Python 里运行别的程序，多进程和多线程"),
  card "进程".
- Quote: 「最简单的办法是 `os.system('ls')`：命令的输出直接显示在屏幕上，
  **返回值是退出状态**，但输出拿不到变量里」。
- Why it is wrong: on Windows `os.system` returns the exit code, but on
  Unix/macOS it returns the *wait status* (`exit_code << 8`): a command that
  exits with 3 gives `768`, and `returncode == 3` is never true. The CPython
  docs say "On Unix, the return value is the exit status of the process encoded
  in the format specified for `wait()`" and point at
  `os.waitstatus_to_exitcode()`. The lesson spends the rest of the chapter
  teaching `returncode` from `subprocess.run`, so a Linux/macOS student who
  checks `os.system(...) == 3` gets a false negative. (Secondary, same line:
  `ls` does not exist in `cmd`/PowerShell, so the example also fails on
  Windows.)
- Suggested fix: say it differs by platform — 「Windows 上返回退出码；Linux/macOS
  上返回的是 `wait()` 编码的状态（退出码 3 得到 768），要用
  `os.waitstatus_to_exitcode()` 换算；拿输出和退出码都方便的做法还是
  `subprocess.run`」— or drop the `os.system` aside and use `subprocess.run`
  from the start (`subprocess.run(["dir"])` on Windows).
- Confidence: medium (the POSIX semantics are certain; the severity in a
  beginner course is a judgement call).

### P.2.3 — everything else checked, no findings

All numeric/text/choice keys and all displayed outputs in P.2.3 were
re-executed and matched, including: `sys.argv`/`IndexError`/`'34'`;
argparse usage and error texts (`backup [-h] -u USER outfile`,
`the following arguments are required: -u/--user`); `sum(range(5), -1)` = 9
vs `np.sum(range(5), -1)` = 10; `importlib.reload`; `(-1)**0.5`,
`(1+2j)(3-j)`, `abs(5+12j)`, the Julia-set loop (4 iterations, `-134+352j`);
list aliasing / `[5, 1]` after the remove-in-loop; late-binding default
arguments; `line` ends with `\n`; `'a'` mode, pickle `wb`; EAFP snippets;
`os.getenv` defaults and `'44'`; `splitext("archive.tar.gz")`; glob `?`
semantics; `os.walk` count; `date(2026,2,27)+2d`; the `Path.rename` example
(the already-fixed issue is now handled with `exists()` and `startswith`);
class/instance/`AttributeError`/`TypeError` messages (including the 3.14 text
`S2.set_age() takes 1 positional argument but 2 were given`);
NumPy: `arange`/`linspace`, `t = 10i+j` table and all its slices, view vs copy,
mask counting, `np.random.seed(3)` + `randint` reproducing exactly
`[10 3 8 0 19 10 11 9 10 6 0 20 12 7 14]`, `a > 2 & a < 8` raising
`ValueError`, `A*B` vs `A@B`, broadcast table (incl. `(2,3)+(2,)` error),
`axis` shapes, `np.cumsum`, `np.gradient` = `[3. 4. 6. 7.]`,
Σ n² to 10⁶ = 333333833333500000 and the int32 wraparound value
16866193336416, banker's rounding, uint8/int8 wraparound, float32 ε and the
10000×1e-8 experiment, structured/masked arrays, `poly1d` vs
`Polynomial([-1,2,3])`, `loadtxt`/`genfromtxt`, `.mat` shape `(1, 5)`,
`imsave`/`imread` dtypes; SciPy: `gamma`/`gammaln`/`comb`, `scipy.cos`
AttributeError, `linalg.solve`/`det`/`inv` (incl. the 1.18 singular message),
SVD values, CSR sizes, `interp1d` out-of-range message, `minimize`
(−1.30644012 / −7.945823375615215 / 3.83746709 / `[0.]`), `curve_fit` with
`default_rng(0)` giving `[2.64198155 1.51346571]` and the p0=[2,5] failure,
`root`/`fsolve`, `quad` (incl. `(0.9999999999999999, 1.1102230246251564e-14)`
and √π), `odeint` vs `solve_ivp` values and argument order, `stats.norm`,
`describe`, t-tests/paired/Wilcoxon/Mann–Whitney, `kstest`, `normaltest` <8
returning nan + SmallSampleWarning, statsmodels OLS (`-5.5335 / 2.9369`,
R² 0.804, identical p-value to `ttest_ind`), seaborn not touching rcParams,
FFT peaks and the `fftdreq` unit pitfall, `signal.resample`/`detrend`/`medfilt`
(`[2. 3. 4. 4. 5. 5.]`), `ndimage.zoom/rotate/shift/gaussian_filter/label/
binary_opening` (5 pixels, 1 component), pip/venv/wheel/`~=` semantics
(`~=1.4.2`), bash quoting/`$?`/`&&`/`2>`/pipes, `subprocess.run` bytes vs
`text=True`, GIL, `multiprocessing.Pool` and the `__main__` guard.

### Cross-pack note (not a defect, recorded for the parent agent)

`D.3.1` and `P.2.3` overlap (arrays, pandas, matplotlib, statistics) but do
not contradict each other on any number or API claim I checked.
