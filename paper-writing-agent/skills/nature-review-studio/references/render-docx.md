# 同步渲染的实际schema

命令：`python <本分支>/scripts/render_review_docx.py --payload <task>/payload.json --out <task>/review.docx [--language zh|en]`。输出同stem DOCX和Markdown；任一已存在即拒绝覆盖。脚本生成相同顺序和内容，不自动判断科学真实性，不自动运行多agent。Word需另做可用的页面视觉检查。

```json
{
  "entry": "review",
  "case_id": "example",
  "language": "zh",
  "scope": "本轮仅审阅用户提供的当前稿Methods和Results；未含代码。",
  "assessment": "模拟修订建议，不是实际编辑决定。",
  "reviewers": [{
    "label": "Reviewer 1",
    "overall": "与当前材料一致的总体评价。",
    "strengths": "有实际依据的优点。",
    "major": [{
      "id": "R1-M1",
      "claim": "当前稿中需要核查的实际论断。",
      "evidence": "Methods，Analysis段。",
      "body": "具体意见及影响。",
      "blocking": true,
      "resolution": "可以验证问题关闭的结果或修改。"
    }],
    "minor": []
  }],
  "synthesis": [{"text": "作者/编辑侧的综合判断。", "concern_ids": ["R1-M1"]}],
  "tasks": [["R1-M1", "Reviewer 1", "具体问题", "clarify_existing_content", "TODO_TEXT", "实际所需输入", "修订段落", "Yes"]]
}
```

每个reviewer必须有label、overall、major列表、minor列表；列表允许为空，不能造问题填满。每条意见必须有id/claim/evidence/body/blocking/resolution，id不重复，minor不可blocking。synthesis如出现须引用已有意见id；tasks每行8个字符串。单人循环审稿可1份，普通多视角数量由已定设置提供，不在脚本强凑数量。

respond模式在每条意见加入response、changes、location、author_action和status；均明确真实进度。DONE/VERIFIED_DONE还要：

```json
"verification": {"path": "revised.md", "excerpt": "实际出现在该修订产物中的文字"}
```

verification路径相对payload文件解析，支持文本、Word和PDF。该检查仅验证摘录存在，语义是否足以解决意见由审稿者判定。其他状态不得描述未完成工作为已完成。五字段作者面回复可由Veritas按模板另行整理。
