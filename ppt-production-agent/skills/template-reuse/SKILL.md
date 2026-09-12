---
name: template-reuse
description: Inspect, extract and reuse a user-supplied PowerPoint template; distinguish one-off native fill from building a reusable content-free template.
---

# 模板提取与复用

读取 `../../references/engine-usage.md`，使用同包 `../../engines/easyslides/engine.py`。先判断一次套模板，还是建立可以继续复用的模板库；已有明确意图时不重复询问。

1. 读取当前源PPTX，渲染查看页型、原生对象、字体、母版、图表和装饰。运行template-inspect取得真实页序与槽位ID；template-assets提取图片、主题和布局元数据。源文件完整保留。
2. **一次套模板**：根据新故事选择源页型，允许的范围内选页/复用/重排；填写fill_plan的新文字、表格、图表数据，检查原研究内容、姓名机构、日期和占位残留。不得把模板中的示例数据当新研究结果。
3. **通用模板**：依据源视觉定义固定装饰、正文槽位、图表与图片区域、字号与容量，不机械复制每一源页变一个模板。生成中性示例并用第二份不同内容真实替换验证；保留原模板的身份标识仅在用户希望且有权使用时。
4. template-fill保留形状几何、段落属性和各段首run格式；全新段落的局部高亮对应关系由agent重设或走patch-runs。不能承诺所有混合格式、SmartArt或OLE都能语义编辑。
5. 备注与转场不由fill_plan自动执行；如请求额外处理，走presentation-editing并同步当前讲稿。
6. 最终渲染检查覆盖实际页数、文字残留、图表数据和模板身份。只有资源提取或JSON生成时写“已提取”，不称“通用模板制作完成”。

模板工作和导出写入用户项目，不修改综合包安装目录。包内不附带原开发机的私人模板、源文稿归档或全量品牌图标；当前任务自行按授权使用输入素材。
