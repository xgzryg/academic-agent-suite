# 可编辑 SVG 最小示例

这两页仅演示原生文字、几何、路径和备注，不包含真实研究数据。

从综合包根目录执行，work请替换为当前用户项目的任务目录：

```shell
python engines/easyslides/engine.py svg assets/examples/svg-demo --output work/svg-demo.pptx
```

SVG位于svg_output，备注位于notes并与SVG同名。封面与第二页的文字、形状和折线路径会转换为可编辑PowerPoint对象。备注写入PPTX备注页。默认不加动画、计时或音频。

复制此示例到项目后再按需要修改，不把用户工作稿写回技能安装目录。实际图片如以后插入仍然是图片；几何折线不带原生图表数据工作簿。
