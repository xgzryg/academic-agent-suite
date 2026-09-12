# 故事板格式与原生生成

统一故事板用于可靠传递页面内容和演讲文字，模型负责依据真实材料填写。脚本负责导出，不会代替模型撰写内容。

```json
{
  "title": "汇报标题",
  "style": "academic",
  "aspect_ratio": "16:9",
  "font": "Aptos",
  "cjk_font": "Microsoft YaHei",
  "footer": "用户提供的页脚",
  "page_numbers": true,
  "slides": [
    {
      "id": "s01",
      "type": "cover",
      "title": "当前演示的标题",
      "subtitle": "副标题",
      "notes": "这里填写实际口语稿，不能只放主题词。",
      "cues": ["停顿后指向标题"],
      "sources": [],
      "duration_seconds": 35
    },
    {
      "id": "s02",
      "type": "content",
      "title": "本页要传达的核心消息",
      "items": ["屏幕要点一", {"t": "屏幕要点二", "s": ["必要的下一级解释"]}],
      "notes": "逐页展开解释，保持与真实材料一致。",
      "duration_seconds": 60
    }
  ]
}
```

`id` 应稳定且唯一；数组顺序是当前页序。没有提供 ID 时原生生成器按当前顺序产生 s01、s02 等，新建稿应尽早补齐 ID 以便后续编辑。`notes` 写入 PowerPoint 演讲者备注，`cues` 用于提示卡，`sources` 为简洁来源文字，完整证据可留任务中的来源表。重排或编辑已有稿先读取其实际状态。

`duration_seconds` 是该页的计划用时，不能当作实际说完时间；未提供时由讲稿工具按指定语速估计。语速、停顿和互动需要实际排练校正。

## 原生页型

| type | 附加字段 |
| --- | --- |
| cover / section | subtitle、kicker、author、date（均可选） |
| agenda | topics：字符串列表 |
| content | items：字符串或 t/s 层次对象列表；可选 conclusion |
| two_column | left、right：列表；可选 left_title、right_title |
| table | headers、rows；每行长度必须与列数一致；null 表示缺失并显示“—” |
| chart | chart_type、categories、series；series 每项为 name 与 values；可选 y_label |
| timeline | milestones：含 label/desc 的对象列表或字符串列表 |
| image | image_path、caption；fit 为 contain（默认等比完整展示）或 cover（明确允许裁切） |
| quote | quote、attribution（实际来源或用户身份，不编造） |
| summary | points、conclusion |
| contact | info（用户提供的结束语或联系方式） |

图表类型支持 bar（柱形）、horizontal_bar、stacked_bar、line、pie。数值必须真实且有限，null 为缺失，不自动补零。饼图要求一组非负数据且总和为正。不能仅凭图片填写精确值。

主题为 academic、business、teaching、dark、minimal；原生比例支持 16:9 与 4:3。字体为可修改起点，由当前系统和用户模板确定；脚本不会安装或内嵌字体。复杂自定义布局进入高级 SVG 分支。

图片路径相对故事板文件解析，也可以使用明确的绝对路径。输出路径由命令显式指定；默认拒绝覆盖同名文件，需要替换时应有相应授权并使用 `--overwrite`。

```text
python <包根>/scripts/native_deck.py <任务目录>/storyboard.json --output <任务目录>/presentation.pptx
```

未知页型、缺失图片和错误数据会报错，不跳页后宣称整套完成。`layout_warnings` 是密度提示，不是实际 PowerPoint 视觉验收。
