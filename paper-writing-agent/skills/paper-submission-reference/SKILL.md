---
name: paper-submission-reference
description: Build and maintain a bilingual first-submission information master workbook, then render a Word reference document for copying into journal submission systems. Use for 投稿信息总表、投稿系统填报资料、投稿参照文档、作者信息总表 or consolidated author/declaration intake; do not use it as a substitute for a journal-specific cover letter or for submitting the manuscript.
---

# 投稿信息总表

从当前手稿、标题页、补充材料和作者提供的信息中整理首次投稿所需资料。Excel 是唯一结构化主表；Word 是由当前 Excel 生成的中英双语参照文档。缺项可以进入草稿，但关键字段未确认时不得标为最终版。

## 开始

1. 读取包根的 `references/shared-rules.md`，并识别用户指定的当前稿、标题页、补充材料、既有作者表和输出目录。
2. 读取本分支的[字段目录](references/field-catalog.md)和[工作簿结构](references/workbook-schema.md)。不要把示例值当作作者事实。
3. 如需新建主表，运行 `scripts/submission_reference.py init`；如有已存在主表，直接读取并保留人工修改。不要另建并行 JSON 资料库。
4. 从材料中预填可直接抄录的信息。自动抽取的值默认标记为 `抽取待确认`；作者明确确认或既有主表已确认的值才标记为 `已确认`。
5. 运行 `validate` 更新“缺项与待确认”及总状态，再按缺项主题分批询问。每轮只问少量相互关联的问题；多作者、单位和 CRediT 直接让用户核对预填 Excel。
6. 运行 `render` 生成 Word。关键项未解决时只能生成“草稿版”；零阻塞项时脚本自动标记“最终版”。

## 状态和证据边界

- 只使用 `已确认`、`抽取待确认`、`缺失`、`不适用`。`不适用` 与不知道不同；不确定时用 `缺失` 或 `抽取待确认`。
- 没在稿件中找到基金、利益冲突、AI 使用、预印本或相关稿件，不等于“无”。不得从沉默生成否定声明。
- 姓名不能用于推断性别、称谓、国籍、族裔、学位、贡献或通讯作者；单位所在地不能当作作者国籍。
- 伦理批准号、注册号、ORCID、邮箱、仓库链接和审稿人关系只允许抄录或由作者提供，不自动补全。
- 来源冲突时保留双方内容和位置，将字段保持为 `抽取待确认`，在备注写明冲突；不得按文件日期自动覆盖。
- 对声明类字段，只有状态为 `已确认` 的英文文本才能进入 Word 的“可直接粘贴”区域。其余内容只作为待确认信息展示。

## 交互和完成条件

- 先抽取，后追问。不要让用户重新填写已经确认的信息。
- 优先询问能改变适用性的控制项，例如是否涉及人体研究、动物研究、试验注册、预印本或 AI 使用；再询问被激活的具体字段。
- 作者、单位、贡献矩阵或审稿人清单信息量较大时，交付预填 Excel 供集中核对，不逐格追问。
- `validate` 返回的 blocking count 大于 0 时可交付草稿和缺项清单，但不得称为投稿就绪或最终版。
- 可选字段未知不阻止最终版；保留空白并注明“当前期刊如要求则补充”。

## 隐私与范围

- 邮箱、电话、地址、性别/投稿系统选项等可收录并标为 `仅投稿系统`；在交付时提醒文档含个人信息。
- 不记录密码、验证码、登录令牌、银行卡、支付凭据或账户恢复信息。
- 本分支仅覆盖首次投稿的通用资料。期刊专属裁剪、返修、转投、接收后版权、付款、发票和校样不在本分支范围。
- 生成文件不代表已经投稿、发送邮件或联系编辑/审稿人。
- 投稿信使用包内 `write-journal-cover-letter`；期刊式标题页和声明页使用 `nature-writing`；普通 Word 编辑使用 `paper-documents`。这些分支可以读取本主表中已确认的事实，但不得反向覆盖主表。

## 命令

以本分支目录为工作定位，使用宿主可用的 Python：

```powershell
python scripts/submission_reference.py init --output "论文投稿信息总表.xlsx"
python scripts/submission_reference.py validate --workbook "论文投稿信息总表.xlsx"
python scripts/submission_reference.py render --workbook "论文投稿信息总表.xlsx" --output "论文投稿信息参照文档.docx"
```

需要从已抽取事实批量预填时，可向 `init` 传入临时 `--seed-json`；JSON 仅是导入载体，不作为交付物或第二资料源。具体格式见[工作簿结构](references/workbook-schema.md)。

## 交付核验

- Excel 含规定工作表、下拉值和当前缺项；Word 能打开且与当前 Excel 一致。
- 作者顺序、作者—单位映射、通讯作者、贡献和声明状态在两份文件中一致。
- Word 中未确认的声明没有被写成确定句；“缺失”和“不适用”没有混用。
- 报告实际为草稿版或最终版，并给出两个文件的绝对路径。具备 LibreOffice 时查看实际 Word 页面；不能渲染时明确说明版面未目视核验。
