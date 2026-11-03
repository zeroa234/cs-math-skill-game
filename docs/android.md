# 安卓 App（APK）

把构建好的网页 `output/web/` 装进一个安卓 App，发给别人装着玩。用的是现成方案 [Capacitor](https://capacitorjs.com/) 8.5.3（MIT，Ionic 官方维护）：它生成一个只有一个全屏 WebView 的安卓工程，把网页文件打进 APK，App 离线也能玩。

选它的理由：游戏本来就是纯静态网页，Capacitor 不需要改游戏的写法；离线可用；导出存档、返回键这些手机上的差别有官方插件。没选的：TWA / Bubblewrap / PWABuilder 要先把游戏放到 HTTPS 网站上，而且离线要另写 Service Worker；Cordova 是同类的老方案，Capacitor 能兼容它的插件，选了新的那个；Tauri 移动端要装 Rust 和 NDK，对一个网页来说太重。

## 打包

```bash
node scripts/android/build-apk.mjs     # npm run build → cap sync → Gradle 签名发布版
```

产物：`output/apk/点亮之路-<版本>.apk`（不含音乐时约 9.5 MB；背景音乐约 18 MB 也打包在里面）。脚本会检查签名密钥在不在，不在就停下，避免打出装不上的未签名包；还会检查要打进 APK 的网页文件里没有指向导师素材来源的词（词表在不公开的 `assets/cast/not-public.txt`，和发布公开仓库时的检查共用 `scripts/lib/not-public.mjs`），因为 APK 也公开放在发布页上。

需要的工具（这台机器都装在 D 盘，脚本默认用这些路径；换机器时用同名环境变量覆盖）：

| 工具 | 默认位置 | 说明 |
|---|---|---|
| JDK 21 | `D:/java/jdk-21.0.12.1+1`（`JAVA_HOME`） | Capacitor 8 的 Gradle 插件要求 JDK 21 |
| Android SDK | `D:/tools/android-sdk`（`ANDROID_HOME`） | 要 `platforms;android-36`（2026-11-03 用 sdkmanager 装的）和 `build-tools;35.0.0` |
| Gradle 8.14.3 | 第一次打包时由 `gradlew` 自动下载到 `D:/tools/gradle-home`（`GRADLE_USER_HOME`） | 依赖缓存也在这里 |
| 安卓用户目录 | `D:/tools/android-user-home`（`ANDROID_USER_HOME`） | 模拟器、调试密钥等默认会写到 `C:\Users\…\.android`，这里改到 D 盘 |

Gradle 和 Java 的临时文件放 `temp/android-tmp/`，可以删。

## 签名密钥（重要）

发布版用 `config/android/release.jks` 签名，密码在同目录的 `keystore.properties`。**这个目录在 `.gitignore` 里，不进 git，要自己备份。**

安卓只允许用同一个密钥签名的新版本覆盖安装。密钥丢了，以后发的新版就装不上去，同学只能先卸载旧版再装，卸载会清掉 App 里的进度。新密钥的生成命令（换密钥时才用）：

```bash
keytool -genkeypair -keystore config/android/release.jks -storetype PKCS12 -alias dianliang -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=cs-math-skill-game"
```

## 发新版本

1. 改 `package.json` 里的 `version`（只有这一处）。网页构建把它写进游戏（“我的 → 版本”和更新检查用它）；`app/build.gradle` 读它作 `versionName`，并算出 `versionCode` = 主 × 10000 + 次 × 100 + 修订（1.1.0 → 10100），安卓靠它判断新旧，所以版本号只能往上加。
2. 提交，`node scripts/android/build-apk.mjs`（发版前跑一遍全量测试，见 [development.md](development.md)“测试”）。
3. 写更新说明 `docs/releases/<版本>.md`（App 的“检查更新”会原样显示它，用纯文本就好），提交。
4. `node scripts/publish-github.mjs --push` 把源码快照推到 [zeroa234/cs-math-skill-game](https://github.com/zeroa234/cs-math-skill-game)。
5. `node scripts/release-github.mjs` 建 `v<版本>` 的发布，附上 APK 和电脑版 zip（`output/web` 打包成 `cs-math-skill-game-<版本>-web.zip`，只有游戏文件，解压后双击 `index.html`）：说明取自第 3 步的文件，APK 以 `cs-math-skill-game-<版本>.apk` 上传（GitHub 会改掉文件名里的中文），中文名“点亮之路 <版本>（安卓）”作为显示标签；中文以 UTF-8 JSON 交给 gh，再读回来比对，上传后的 sha256 要和本地一致。

App 每天最多自动检查一次 `https://api.github.com/repos/zeroa234/cs-math-skill-game/releases/latest`（`src/game/app/update.js`），发现新版本就在营地显示“有新版本 [下载] [以后再说]”；“我的”页最下面可以随时手动检查。下载的是发布页上的 APK，安装要本人确认（安卓不允许商店外的 App 静默更新）；同包名、同签名，覆盖安装进度还在。请求只有这一个 GET，不带任何玩家数据；GitHub 对未登录请求每个 IP 每小时限 60 次，一天一次远远够用。

## 文件在哪

| 路径 | 内容 |
|---|---|
| `capacitor.config.json` | App 名、包名 `local.csmathskillgame.app`、网页目录 `output/web`、安卓工程目录 `src/android`。Capacitor 只认项目根目录下的这个文件，所以放在根目录 |
| `src/android/` | `npx cap add android` 生成的安卓工程。修改包括 `app/build.gradle` 的签名和版本、`res/` 的图标和启动背景、`MainActivity.java` 的 WebView 设置（禁止页面缩放；背景音乐换曲不需要再点一下，`setMediaPlaybackRequiresUserGesture(false)`，游戏自己仍然等第一次点击才出声）。网页副本（`app/src/main/assets/public`）和构建产物不进 git，每次 `cap sync` 重新复制 |
| `scripts/android/build-apk.mjs` | 上面的打包脚本（自写，约 40 行胶水代码） |
| `scripts/android/make-icon-sources.mjs` | 画图标和启动图的源图到 `assets/app-icon/`：游戏里的像素灯泡（pixelarticons 的 lightbulb，MIT），深蓝底、金色、亮黄灯芯，按整像素放大，保持像素边缘清楚（自写，用 Playwright 截 SVG） |
| `assets/app-icon/` | 图标源图。切成安卓各尺寸用官方工具：`npx @capacitor/assets@4.0.0 generate --android --androidProject src/android --assetPath assets/app-icon` |
| `src/game/app/native.js` | App 里才生效的部分：`NATIVE`（是不是在 App 里）、返回键处理、viewport 禁止整页缩放 |

## App 和网页版的差别

网页版的代码一行没删，在浏览器里（包括双击打开的 `file://`）`NATIVE` 是 false，和以前完全一样。在 App 里：

| 功能 | 网页版 | App |
|---|---|---|
| 导出存档 | 浏览器下载文件 | 安卓的 WebView 不支持下载链接，所以先把文件写到 App 缓存，再弹出系统分享（`@capacitor/filesystem` 8.1.5 + `@capacitor/share` 8.0.3），可以发到微信、QQ 或存到文件 |
| 导入存档 | 选文件 | 系统文件选择器（WebView 自带） |
| 手机返回键 | — | 返回上一个界面；在第一个界面再按就退出 App（`@capacitor/app` 8.1.2）。不装这个插件时，按返回键会直接关掉 App |
| 教材和课程链接 | 新标签页 | 跳到手机浏览器，回来时 App 停在原处 |
| 进度 | 存在浏览器里 | 存在 App 里；覆盖安装新版不丢，卸载会丢 |
| 状态栏 | — | 网页不延伸到状态栏下面（Capacitor 8 默认的 `SystemBars` 处理），不用改样式 |
| 页面缩放 | 保留浏览器缩放 | WebView 和 viewport 都禁止整页缩放；技能地图仍可单独缩放和拖动 |
| 背景音乐 | 切到别的标签页时暂停 | 切到后台（主屏键、来电、别的 App）时暂停（`@capacitor/app` 的 `appStateChange`） |

## 怎么验证的（2026-11-03）

在 Android 15 模拟器上验证（Pixel 7 尺寸、系统自带 WebView 124，AVD `cs35` 在 `D:/tools/android-user-home/avd`，用 `-no-window` 无窗口启动）：

- 发布版：安装、启动、开场、跳过开场、选远征、返回键回到营地、在营地再按返回键退出；桌面图标。
- 调试版（`gradlew assembleDebug`，可以远程调试 WebView，网页内容和发布版相同）用 Playwright 的 `_android` 驱动：玩到 C.2.1“页面置换”课里的交互题并操作一步；返回键从课程回到路线页；导出弹出系统分享面板，缓存里有存档文件；导入打开系统文件选择器；外部链接打开 Chrome，回到 App 时还在原来的界面。整个过程只有一条控制台错误（WebView 自动请求 `/favicon.ico` 得到 404），已给网页加上图标解决。

没验证的：真手机（各家系统，比如 MIUI、ColorOS 的安装提示）；Android 7–14 和更旧的 WebView（`minSdk` 是 24，即 Android 7.0）。

手机布局另有 `node tests/phone-fit.mjs`（电脑上的 Edge 手机模拟，360px）：每个界面、每课每一步都不许比屏幕宽。1.0 发给同学后发现结算页、技能页和长代码排序题会撑宽页面、能被拖动，这个检查就是为此加的；改样式后先跑它，再打包。

1.0.1 在模拟器上验证过覆盖安装（同包名、同签名，安装前后 App 里的存档文件逐个哈希一致）和禁止整页缩放，详见 [更新验证记录](../reports/android-update-1.0.1.md)。想让调试版和发布版同时装在一台模拟器上，可以用临时 Gradle init script 给调试版包名加后缀（那次用的是 `.qa`），这样不用卸载发布版、也不会清掉存档。

## 给同学装的时候

- 安卓手机要允许“安装未知应用”（第一次装时系统会问）；国产系统可能还会提示“未经检测的应用”，选继续安装。
- 用纯血鸿蒙（HarmonyOS NEXT）的华为手机装不了 APK；苹果手机也装不了。
- 微信有时会拦截 .apk 文件或给它改名；装不上就换 QQ 发，或者先压缩成 zip 再发。
- 两位导师是二创形象：源码仓库不含这些素材，发布页的 APK 带着（作者 2026-11-03 决定这样发布）。上架应用商店或商用之前要换成原创角色。
