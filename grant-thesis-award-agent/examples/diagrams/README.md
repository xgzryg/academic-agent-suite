# 可编辑科研图形示例

本目录的所有项目内容和日期均为合成演示，不代表真实数据、成果或推荐研究方法。Python 工具仅需 Python 3.9 以上标准库，离线运行，无需安装绘图库。运行时将 `python` 换成宿主真实可用的解释器路径；从本包根目录执行，并把输出路径改为用户项目中的实际目录。

```powershell
python scripts/research_diagrams.py --input examples/diagrams/roadmap.json --output-base 'D:/my-project/figures/roadmap'
python scripts/research_diagrams.py --input examples/diagrams/gantt.json --output-base 'D:/my-project/figures/gantt'
python scripts/research_diagrams.py --input examples/diagrams/timeline.json --output-base 'D:/my-project/figures/timeline'
```

每次生成 `<output-base>.svg` 和 `<output-base>.drawio`。两者包含文字和形状对象；draw.io 文件包含原生节点/连线，不是嵌入整张图片。SVG 可在现代浏览器中查看、在支持 SVG 的矢量编辑器中修改；draw.io 文件可在已有的 diagrams.net / draw.io 中打开。字体实际编辑能力取决于接收软件和已安装字体。工具不会自动启动浏览器或联网。

已有任何一个同名输出时工具退出，请采用新的输出名称。全部输入检查和 XML 构造通过后才创建输出；无效节点、边、日期或依赖不会产生输出图。JSON 源文件仍由用户项目保存，方便重新生成。修改后的人工固定图不要从旧 JSON 重建覆盖。

## 路线与流程

`roadmap.json` 示范 `type: roadmap`，也接受 `type: flow`。`title` 必填；`nodes` 为非空对象数组，每个节点必填唯一 `id`、非空 `label`、非负整数 `row` 和 `col`。行列按大小排列，占位不可重复；相同层级使用相同 row。可选 role 为 `process`、`input`、`evaluation`、`neutral`，仅决定样式。

`edges` 为数组，每条边提供 `source` 和 `target` 节点 ID，可选短 `label` 与 `type`：

| type | 含义 | 呈现 |
|---|---|---|
| flow | 实际工作流程 | 实线箭头 |
| dependency | 工作依赖 | 虚线箭头 |
| association | 关联 | 无箭头实线 |
| hypothesis | 假设关系 | 虚线箭头 |
| activation | 已有证据支持的激活关系 | 实线箭头 |
| inhibition | 已有证据支持的抑制关系 | T 端线 |

若同图使用不同意义但同样式的边，标签必须补明其具体含义。脚本不验证科学真实性，也不自动解决所有跨层线路交叉；按实际图检查并调整 row/col，复杂迭代或密集网络可在原生 draw.io 中调整。长文字会近似换行，最终仍需检查中文字体、节点、连线、箭头和印刷大小。自环不支持，应明确区分被重复执行的步骤。

## 甘特

`type: gantt`，必填 `title` 和非空 `tasks`。每项提供唯一 `id`、非空 `label` 和 ISO `YYYY-MM-DD` 的 `start`/`end`；结束日计入持续时间，开始日不得晚于结束日。横轴按日成比例，标注自动选取的真实日期刻度。可选 `depends_on` 为前置任务 ID 数组，语义仅支持“前置任务结束后才能开始”，日期不得重叠；并行任务不应人为加此依赖。依赖以图底文字列出，任务条不自动连箭头。没有真实日期时先交付待定计划表，不调用工具填假日期。

## 时间线

`type: timeline`，必填 `title` 和非空 `events`。每项提供唯一 `id`、有效 `date`、非空 `label`，可选 `description`。工具按日期排序，事件块逐项排列，图中明确说明间隔不代表时间比例。对“已完成”“计划”“预期”的事实状态由输入文字明确表达。

## 思维导图与插画

`mindmap.md` 是可编辑的 Markdown 层级源，可按已有软件的 Markdown 导入功能处理；Python 脚本不读取思维导图 Markdown，也不生成 `.xmind`。复杂机制和图文摘要插画由宿主真实图像工具条件执行；无工具时可交付设计方案、标签和可编辑关系框架。生成式插画不是统计图或可编辑关系图的替代品。

工具成功输出只证明文件创建和输入/语法检查完成。成品交付前须实际渲染 SVG 并检查；无法渲染或尚未在 draw.io 打开时，应明确尚未完成该层验证。
