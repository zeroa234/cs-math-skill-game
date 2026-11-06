# Toy 上传包

Toy 包保留本地存档、互动课、结业挑战、导师、技能树和技能章节。完整版的外部课程资料、课程证据、教材目录及技能树附带的自学练习和参考答案由完整版提供。Toy 包的界面按实际提供的内容显示。第三方依赖的许可声明继续随包发布。

在游戏项目目录执行：

```powershell
npm run data
node scripts/build-web.mjs --toy
$version = (Get-Content -Raw package.json | ConvertFrom-Json).version
tar.exe -a -c -f "output/toy/cs-math-skill-game-$version-toy-review2.zip" -C output/toy/web .
```

ZIP 根目录包含 `index.html`。在原 Toy 的管理页上传 ZIP 后重提审核。详细流程见 [B 站 Toy 官方发布检查表](https://github.com/bilibili/toy/blob/main/skills/toy/references/content-checklist.md)。
