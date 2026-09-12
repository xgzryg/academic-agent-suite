---
name: presentation-editing
description: Apply scoped edits, template-based reordering and speaker-note enhancement to an existing PPTX while preserving current user edits and unsupported native objects.
---

# 已有演示文稿修改

先读当前文件及用户修改要求；依据实际对象定位，不从旧故事板重新生成覆盖。使用 `../../references/engine-usage.md` 中的原生编辑路径。

- 局部文字/数字修正：读取当前页和shape/run，优先patch-runs，用expected_text确认仍是当前文字，保留混合run样式和未改对象。
- 需要整段替换/表格/原生图表数据修改或授权的选页重排：template-inspect→template-plan→template-fill，保留原始输入，说明可保留的格式层次。
- 只补演讲备注：notes-init→按当前页写notes→准备已授权的enhancement_plan→notes-apply；不改变可见页面。更新对应讲稿与页序。
- 排版美化：检查实际文字框、字体、对齐、图片比例、留白和对比度；按授权对需要变化的对象实现局部修改。现有主题颜色补丁不是完整自动美化。不得为“美化”擅自更改事实、图表含义、作者、机构或页序。
- 复杂对象：保留源SmartArt/OLE/媒体；需要改内部语义时先确认有可用编辑手段与数据，不把保留对象说成已经能自动编辑。
- 音频/计时/转场仅在用户要求时开启；验证实际播放/页计时与讲稿对应后才声称完成。未测试的媒体兼容性写清楚。

更新后读取实际PPTX、核对受影响文本/备注/数据/页序，再渲染检查受影响页；结构变化时检查全稿。仅关闭本任务打开的PowerPoint文件，不Quit或Kill用户的Office进程。保留原稿，工作稿更新遵守用户授权。
