# Full Stack Resources

收集全栈各种学习资料。

## 文件存储策略

本项目采用 **GitHub + HuggingFace 双重存储** 方案管理大量文件：

| 文件类型      | 大小阈值 | 存储位置             | 标识  |
| ------------- | -------- | -------------------- | ----- |
| PDF、压缩包等 | > 50MB   | HuggingFace Datasets | 🤗 HF |
| 其他资料      | < 50MB   | GitHub Repository    | 📄    |

```
大文件 (>50MB)  ─→  HuggingFace Datasets
小文件 (<50MB)  ─→  GitHub Repository
GitHub Pages    ←─  动态索引（index.html）
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/hfhfn/full_stack_resources.git
cd full_stack_resources
```

### 2. 一键配置

**Windows：**

```bash
scripts\setup.bat
```

**Linux/macOS：**

```bash
bash scripts/setup.sh
```

### 3. 配置 GitHub

确保在 GitHub 仓库设置中开启 **Pages**：

- Settings → Pages → 来源选择 `main` 分支

## 📥 文件浏览

访问 **[GitHub Pages](https://hfhfn.github.io/full_stack_resources)** 进行在线浏览和下载。

- 支持搜索
- 自动识别大文件来源
