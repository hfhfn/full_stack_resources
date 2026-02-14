---
name: github-hf-dual-storage
description: 将任何 GitHub 仓库转换为双端存储系统 (大文件上传至 HuggingFace，代码/网页保留在 GitHub)。v4.1 支持完整自动化部署、智能文件删除、详细设置指南及同步删除。
metadata:
  version: "4.1"
  author: "Antigravity"
---

# GitHub + HuggingFace Dual-Storage Skill

## 1. 概述与架构

本技能指导您将标准的 GitHub 仓库转换为针对大数据集或二进制文件优化的双端存储系统。

- **大文件 (>50MB)**: 自动上传至 HuggingFace Datasets，并通过 `.gitignore` 排除。
- **自动化分发 (v4.1)**: 集成 GitHub Actions，实现 push 代码后自动分流，且不会覆盖用户本地更新。
- **智能删除 (v4.1)**: 删除本地文件后自动移除 .gitignore 规则和 HF 文件，无需手动编辑。
- **新手友好文档 (v4.1)**: 生成包含完整环境配置、Secret 设置、一键脚本说明及 **Git LFS 备用方案** 的 `README.md`。
- **Premium 统一界面**: 基于 GitHub Pages 的玻璃拟态 UI，支持暗色模式与文件夹匹配搜索。

> 📖 **参考**: 阅读 `references/architecture.md` 以了解详细系统设计。

## 2. 执行阶段 (Phases)

### Phase 1: 环境分析与仓库识别

1. **GitHub 上下文**: 运行 `git remote -v` 获取当前仓库的用户名和名称。
2. **HuggingFace 上下文**: 询问用户 `HF_USERNAME` (默认同 GitHub) 和 `HF_REPO_NAME` (默认匹配仓库名)。

### Phase 2: 脚手架搭建 (Scaffolding)

按需读取 `assets/` 目录下的模板并注入配置：

1. **分发脚本 (`scripts/distribute_files.py`)**: 写入逻辑同 v3.1，确保 `HF_REPO_ID` 正确。新增特性：
   - 智能时间戳保留：仅当文件内容或数量变化时更新
   - 自动删除规则：检测本地已删除文件，自动移除 .gitignore 规则
   - 404 容错：文件已删除状态视为成功
2. **初始化脚本 (`setup.bat` & `setup.sh`)**: 确保脚本包含对 `huggingface_hub` 的自动安装。完整工作流支持。
3. **Web 界面 (`index.html`)**: 注入 GitHub 项目信息，支持自动过滤隐藏 `setup` 脚本。
4. **自动化流水线 (`.github/workflows/distribute-files.yml`)**: v4.1 仅处理 HF 同步，不提交推送，避免覆盖用户更新。
5. **标准文档 (`README.md`)**: 包含完整的 GitHub Actions 设置指南、手动运行说明及**自动化删除说明**。

### Phase 3: 初始化执行与验证

- **一键配置**: 指导用户运行根目录的 `setup.bat` 完成初次本地分发与 Git 同步。
- **云端授权**:
  - 必须在 GitHub 仓库设置 `HF_TOKEN` (必须有 Write 权限)。
  - **关键**: 确保 Workflow 具备 `contents: write` 权限 (v4.1 已在模板中默认修复)。
  - **v4.1 改进**: Workflow 设置为读取模式，仅同步 HF，不提交文件。
- **线上发布**: 引导开启 GitHub Pages，并验证资源树是否正确渲染。

## 3. 最佳实践

- **鉴权**: 优先使用 `HF_TOKEN` 环境变量。
- **删除文件**: 删除本地文件后直接运行 `setup.bat`，脚本自动处理所有清理（无需手动编辑）。
- **更新**: 定期运行同步删除逻辑以节省 HuggingFace 存储空间。
- **文档**: 始终提供清晰的 `README.md` 以便协同开发者理解分发逻辑。

## 4. v4.1 核心改进

### 4.1 智能 .gitignore 删除
- **旧方式 (v3.2)**: 用户需手动编辑 .gitignore，删除已删除文件的规则
- **新方式 (v4.1)**: 脚本检测本地文件是否存在，自动移除不存在文件的规则

### 4.2 GitHub Actions 控制权分离
- **旧方式 (v3.2)**: GitHub Actions 自动提交/推送 manifest，导致覆盖用户更新
- **新方式 (v4.1)**: GitHub Actions 仅运行同步逻辑，不提交任何更改，用户本地完全掌控

### 4.3 时间戳智能保留
- **旧方式 (v3.2)**: 每次运行都更新时间戳，导致无必要的更新
- **新方式 (v4.1)**: 仅当文件内容或数量变化时更新时间戳
