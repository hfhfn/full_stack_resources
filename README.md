# full_stack_resources - 资源中心

本项目采用 **GitHub + HuggingFace 双端存储** 方案：

- **大文件 (>50MB)**: 自动分流并托管至 HuggingFace Datasets (🤗 HF)。
- **小文件与代码**: 保存在 GitHub 仓库。
- **动态导航**: 通过 GitHub Pages 提供统一的搜索与下载界面。

---

## 🚀 快速开始

### 1. 环境准备 (必需)

确保本地已安装 Python 3.8+ 及 Git。然后安装核心依赖：

```bash
pip install "huggingface_hub>=0.17.0"
```

### 2. 克隆与初始化

```bash
git clone https://github.com/hfhfn/full_stack_resources.git
cd full_stack_resources
```

**一键配置：**

- **Windows**: 双击或运行 `setup.bat`
- **Linux/macOS**: 运行 `bash setup.sh`

> 该脚本将引导您完成 HuggingFace 认证、大文件首次分发及 Git 自动关联。

### 3. 配置 GitHub Actions (实现自动化)

为了使推送代码后系统能自动分发大文件，请在 GitHub 仓库设置中添加以下 Secrets：
路径：`Settings -> Secrets and variables -> Actions -> New repository secret`

| Secret 名称   | 描述                     | 获取方式                                                                                 |
| :------------ | :----------------------- | :--------------------------------------------------------------------------------------- |
| `HF_TOKEN`    | HuggingFace 写入权限令牌 | [HF Tokens Settings](https://huggingface.co/settings/tokens) (创建 "Write" 权限的 Token) |
| `HF_USERNAME` | 你的 HuggingFace 用户名  | -                                                                                        |

### 4. 开启浏览器访问

进入 `Settings -> Pages`，选择 `main` 分支及 `/ (root)` 目录，点击 `Save`。
部署完成后，您可以通过以下地址访问精美的资源导航页：
`https://hfhfn.github.io/full_stack_resources`

---

## 🔄 文件更新说明

### 添加大文件

1. **将文件放入仓库目录** (>50MB 文件将自动转移至 HuggingFace)
2. **运行同步脚本** (Windows):
   ```batch
   setup.bat
   ```
   或 (Linux/macOS):
   ```bash
   bash setup.sh
   ```
3. **确认推送**: 脚本会提示确认，自动上传至 HuggingFace 并推送到 GitHub
4. **结果**:
   - ✅ 大文件在 HuggingFace 存储
   - ✅ `.gitignore` 自动添加规则
   - ✅ `data/file_manifest.json` 自动更新
   - ✅ Pages 页面显示该文件

### 删除大文件

**重要**: 删除大文件需要主动推送才能在 Pages 页面同步显示，否则会出现"404 Not Found"。

**完整操作步骤**:

1. **本地删除文件**:
   ```bash
   rm your_large_file.bin
   ```

2. **编辑 .gitignore，移除该文件规则**:
   - 打开 `.gitignore`
   - 找到 `# [Auto] Large files managed by HuggingFace` 部分
   - 删除对应的文件行

   示例：如果要删除 `《内容算法：把内容变成价值的效率系统》_闫泽华.pdf`
   ```
   # [Auto] Large files managed by HuggingFace
   # 删除这一行：《内容算法：把内容变成价值的效率系统》_闫泽华.pdf
   ```

3. **运行同步脚本** (必须):
   ```batch
   setup.bat
   ```
   脚本会：
   - 检测 `.gitignore` 变化
   - 自动从 HuggingFace 删除该文件
   - 自动从 `manifest.json` 删除该文件条目
   - **自动提交和推送到 GitHub** ⭐️

4. **验证成功**:
   - GitHub Actions 运行完毕（查看 Actions 标签）
   - Pages 页面刷新后，该文件消失

**关键点**:
- ❌ 不要直接运行 `python scripts/distribute_files.py`（不会推送更新）
- ✅ 必须用 `setup.bat` 或 `setup.sh`（会自动提交和推送）
- ⏳ GitHub Actions 同步需要 1-2 分钟

---

## 🛠️ 项目结构

- `scripts/distribute_files.py`: 核心分发引擎 v3.1（支持重试机制、增强日志及全量清单生成）。
- `setup.bat` / `setup.sh`: 跨平台一键环境搭建脚本。
- `data/file_manifest.json`: 自动生成的文件元数据清单（前端加载数据源，免除 GitHub API 限速干扰）。
- `index.html`: 高端毛玻璃风格的资源导航前端（支持骨架屏展示）。
- `.github/workflows/`: 自动化分发流水线配置。

---

## 🛡️ 备用方案：Git LFS (Large File Storage)

如果不想使用 HuggingFace 分发方案，可以使用 Git LFS 直接在 GitHub 管理大文件。

### 1. 安装 Git LFS

- **Windows**: `choco install git-lfs` 或从 [官网](https://git-lfs.github.com/) 下载。
- **macOS**: `brew install git-lfs`
- **Linux**: `sudo apt-get install git-lfs`

### 2. 初始化与使用

```bash
# 初始化 LFS
git lfs install

# 克隆仓库
git clone https://github.com/hfhfn/full_stack_resources.git

# 查看管理的文件
git lfs ls-files
```

> [!IMPORTANT]
> GitHub 免费用户 LFS 配额为 1GB 存储 + 1GB/月带宽。如果文件总量超过限制，建议使用 HuggingFace 主方案。

## ❓ 常见问题 (Q&A)

**Q: 文件没有出现在 GitHub Pages 中？**

- 检查文件是否已推送到 GitHub / HuggingFace。
- 确认 GitHub Pages 已启用，且 `data/file_manifest.json` 已更新。

**Q: HuggingFace 上传失败？**

- 运行 `huggingface-cli whoami` 验证登录。
- 确保 `HF_TOKEN` 具有 "Write" 权限。

**Q: 大文件下载很慢？**

- 国内用户可使用镜像：`huggingface-cli download hfhfn/full_stack_resources --repo-type dataset --endpoint https://hf-mirror.com`

---

## 📜 许可证

本项目收集的资料仅供学习交流使用。
