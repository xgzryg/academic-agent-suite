---
name: delivery-qa
description: Verify the current presentation, notes and speech files; render and inspect actual PPTX pages where supported and report precise delivery limitations.
---

# 导出、核查与交付

核查实际准备交付的当前 PPTX；源 SVG、旧预览或已修改前的报告不能代替它。按任务验证事实、格式和覆盖范围，不凑审查问题。

## 内容与同步

- 页数、顺序和必讲内容符合当前需求；没有未处理的占位文案、遗留模板身份和不相关样本图。
- 数字、图表、引用、时间线和结论与事实源一致，正文、备注、讲稿和问答没有互相矛盾。
- 通过故事板 ID、当前页序和实际 notes 核对对应关系。缺失备注和阅读范围明确报告，不能拿旧讲稿凑齐。
- 图表中的数据/单位/缺失与含义正确；可编辑性的表述与实际对象匹配。

## 页面与导出

先发现当前环境。Windows 有 PowerPoint 时可用包内 `scripts/render_pptx.ps1` 对实际文件导出 PNG；参数见脚本帮助或[工程说明](../../references/engine-usage.md)。关闭本任务打开的文稿，不退出用户其他文稿。其他系统按实际可用的 LibreOffice 或宿主查看能力处理，不假称已渲染。

逐页查看生成图，核对遮挡、越界、字体、标题换行、图表密度、对比度、来源与页脚可读性。修复实质问题后重新生成受影响的最终文件和预览；不能以 XML/对象边界检查通过替代可用条件下的视觉检查。

需要 PDF、图片、Word 或 HTML 讲稿时按实际任务导出。PDF/PNG 是查看版本，不替代承诺的可编辑 PPTX。媒体、字体和动画未实测时精确说明其范围。

## 完成交付

交付用户要求的 PPTX、讲稿/备注、必要备答和预览，附简短来源与缺项说明。记录确有恢复需要的当前稿与阶段；不把完整构建日志写进用户演讲稿。提供完整绝对路径，实际完成后停止。
