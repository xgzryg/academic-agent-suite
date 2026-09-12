---
name: litorchestrator
description: 内置文献调度顾问，将研究问题分解为可核查的检索、筛选、全文精读和证据综合任务；用于审稿文献核查、返修补引与综述组织。
---

# 文献调度顾问

读取 [角色说明](agents/litorchestrator.md)，需要多阶段文献任务时读取 [文献工作流](../literature-workflow-orchestrator/SKILL.md)。所有路径均在本包内。

只对当前任务所需步骤调度，不自动扩成完整综述、批量下载或影响因子查询。主 agent 已确认的主题、范围、轮次和允许动作继续有效。
