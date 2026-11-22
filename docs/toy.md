# Toy 上传包

Toy 包保留本地存档、互动课、结业挑战、导师、技能树和技能章节。完整版的外部课程资料、课程证据、教材目录及技能树附带的自学练习和参考答案由完整版提供。Toy 包的界面按实际提供的内容显示。第三方依赖的许可声明继续随包发布。

在游戏项目目录执行：

```powershell
npm run data
node scripts/build-web.mjs --toy
$version = (Get-Content -Raw package.json | ConvertFrom-Json).version
tar.exe -a -c -f "output/toy/cs-math-skill-game-$version-toy.zip" -C output/toy/web .
```

ZIP 根目录包含 `index.html`。更新时在原 Toy 的管理页上传 ZIP，保留原地址（slug），提交后重新审核。

上传前按检查表核对：入口 `index.html` 解压后不超过 1 MB（现在只有约 0.6 KB），资源一律用相对路径，包里不能有 `.git`、`node_modules`、`__MACOSX`、`.DS_Store`。app.js 里出现的 `href="/login"` 之类是网站开发课正文里的示例代码，不是页面跳转。B 站机审会去掉标点和空格再匹配敏感词：2.3.0 的“正相反，共享”就这样被读成了“反共”。所以 `--toy` 构建只保留汉字再查一遍：这个词，加上几个常见的政治敏感词，命中就报出那一行并停止，改 `data/content` 里的原文即可（这一处 2.3.0 是人工审核放行的，目标是以后不再进人工审核）。这只是轻量检查，不是完整词表。正常句子也会命中（如“两台独立”里的“台独”、“无法轮询”里的“法轮”），照样改写原文，因为客服只确认了“反共”，没说其余的不会触发。以后机审再标出新词，加进 [scripts/build-web.mjs](../scripts/build-web.mjs) 的 `TOY_FLAGGED`。官方的 `toy_doctor.py` 也能做上面这些检查，但它是下载来的脚本，要先经作者同意才能在本机运行。详细流程见 [B 站 Toy 官方发布检查表](https://github.com/bilibili/toy/blob/main/skills/toy/references/content-checklist.md)。
