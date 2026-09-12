---
name: reproducibility-checklist
description: Reproducibility Checklist — Open Science Best Practices
---

先读取 [便携整合规则](PORTABLE.md)。本包当前明确授权与便携规则优先于下列旧默认。


# Reproducibility Checklist — Open Science Best Practices

## Overview
Ensure research is reproducible, transparent, and meets open science standards.

## Pre-Registration
- [ ] Study registered on ClinicalTrials.gov, OSF, or AsPredicted before data collection
- [ ] Primary outcome and analysis plan pre-specified
- [ ] Deviations from pre-registration documented and justified

## Data Availability
- [ ] Raw data deposited in domain repository (GEO, PDB, PRIDE, Zenodo, Dryad, Figshare)
- [ ] Data dictionary/codebook provided
- [ ] Sensitive data: de-identification method documented, access controls described
- [ ] DOI assigned to dataset

## Code Availability
- [ ] Analysis code in public repository (GitHub, GitLab, Zenodo)
- [ ] Environment specification (requirements.txt, conda env, Docker, renv.lock)
- [ ] Random seeds fixed and documented
- [ ] README with reproduction instructions

## Materials
- [ ] Reagent catalog numbers, lot numbers, manufacturer
- [ ] Custom materials: synthesis protocol or request process
- [ ] Cell lines: STR authentication, mycoplasma testing
- [ ] Antibodies: RRID or Antibody Registry ID

## Statistical Reporting
- [ ] All statistical tests, parameters, and software versions reported
- [ ] Effect sizes and confidence intervals (not just p-values)
- [ ] Multiple comparison correction method stated
- [ ] Sample size justification (power analysis)

## Reporting Standards
- [ ] Applicable guideline followed (STROBE/CONSORT/PRISMA/ARRIVE/MIQE)
- [ ] Checklist completed and submitted with manuscript


<!--
[LobsterAI 迁移元数据]
original_frontmatter: {"name": "reproducibility-checklist", "description": "Reproducibility Checklist — Open Science Best Practices"}
-->


## 适用性

这些项目按研究设计、真实注册状态、伦理和数据使用许可核查；未预注册的探索性研究、受限访问数据、非随机算法、既定报告方案不自动判错。不新增事后注册事实，不把许可受限数据强制公开，不因检查表自动改变多重性或中介方法。未报告与未实施分开。
