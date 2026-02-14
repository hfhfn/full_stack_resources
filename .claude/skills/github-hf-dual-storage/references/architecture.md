# System Architecture v4.1

The GitHub + HuggingFace Dual-Storage system solves GitHub's file size limitations by using HuggingFace Datasets as secondary storage for large binary files (>50MB), while keeping code and web interfaces on GitHub.

## 1. Storage Strategy

- **GitHub**: Stores code, small documentations, web interface (`index.html`), and metadata (`data/file_manifest.json`).
- **HuggingFace**: Stores large files (>50MB), excluded from Git tracking via `.gitignore`.

## 2. Key Components

### 2.1 Backend: `distribute_files.py` (v3.1 + v4.1 enhancements)

Core distribution engine with the following capabilities:

- **Scanning**: Identifies files exceeding the 50MB threshold.
- **Uploading**: Pushes large files to the specified HuggingFace dataset repository with retry logic (3 attempts, exponential backoff).
- **Sync Deletion**: Compares local files with HuggingFace repository:
  - **v4.1**: Checks if files in `.gitignore` rules exist locally
  - **v4.1**: Automatically removes rules for missing files
  - **v4.1**: Automatically deletes missing files from HuggingFace
  - **v4.1**: Treats 404 errors as expected (file already gone = success)
- **Manifest Generation**: Creates `data/file_manifest.json` with:
  - **v4.1**: Intelligent timestamp preservation (only updates if content changes)
  - **v4.1**: Automatic detection of file count changes (deletion indicator)
  - File metadata: name, path, size, URL, last_modified
- **Git Management**: Automatically updates `.gitignore` and removes large files from Git cache.

### 2.2 Frontend: `index.html`

A modern, glassmorphism-styled web interface that:

- Fetches code files directly from the GitHub API.
- Fetches large file metadata from `file_manifest.json`.
- Provides a unified tree view of both storage sources.
- Supports dark mode, searching, and type filtering.

### 2.3 Orchestration: `setup.bat` / `setup.sh` (v4.1)

Complete workflow orchestration:

1. **Environment Check**: Verify Python and dependencies
2. **Dependency Installation**: Auto-install huggingface_hub if missing
3. **Git Sync**: `git pull --rebase --autostash` for conflict-free synchronization
4. **Distribution**: Run `distribute_files.py` to process files
5. **Local Commit**: Stage and commit changes locally
6. **Push to GitHub**: Push to remote repository

### 2.4 CI/CD: `.github/workflows/distribute-files.yml` (v4.1)

GitHub Actions workflow with read-only model:

- **Triggers**: On push to main branch (excluding README.md and index.html)
- **Purpose**: Sync HuggingFace deletions (files deleted locally should be removed from HF)
- **v4.1 Model**: Read-only - script runs but does NOT commit or push
- **Reasoning**: Prevents GitHub Actions from overwriting user's local updates with stale versions
- **Responsibility Model**: User (local) controls all commits, GitHub Actions only validates

## 3. Workflow Architecture

### 3.1 Upload New File (>50MB)

```
User: Copy file > 50MB to repo
    ↓
setup.bat runs:
  1. git pull --rebase --autostash
  2. python distribute_files.py
     - scan_files() → detects new file
     - upload_to_hf() → uploads to HF
     - update_gitignore_and_git() → adds .gitignore rule
     - generate_manifest() → updates file_manifest.json
  3. git add . && git commit
  4. git push
    ↓
GitHub Actions triggered:
  - distribute_files.py runs (no-op, already uploaded)
  - Does NOT commit/push (read-only)
    ↓
Result: File in HF ✓, .gitignore on GitHub ✓, Pages updated ✓
```

### 3.2 Delete Large File

```
User: rm large_file.bin (delete locally)
    ↓
setup.bat runs:
  1. git pull
  2. python distribute_files.py
     - scan_files() → file not found
     - update_gitignore_and_git()
       a) Read .gitignore auto-section rules
       b) FOR EACH rule:
          - Check if file exists locally
          - IF NOT: Remove rule, delete from HF, handle 404 as success
       c) Remove stale rules from .gitignore
     - generate_manifest()
       - Detect file count decreased → force update timestamp
       - Remove entry for deleted file
  3. git add . && git commit
  4. git push
    ↓
GitHub Actions triggered:
  - distribute_files.py runs
  - File already deleted from HF (expected 404)
  - Does NOT commit (read-only)
    ↓
Result: File deleted from HF ✓, .gitignore updated ✓, manifest updated ✓, Pages current ✓
```

### 3.3 Multiple Changes (Add + Delete)

```
User operations:
  - Add big_file_A.bin (new)
  - Delete big_file_B.bin (existing)
    ↓
setup.bat processes:
  - big_file_A: Uploaded to HF, rule added to .gitignore
  - big_file_B: Deleted from HF, rule removed from .gitignore
  - Single manifest.json update with both changes
    ↓
Result: Atomic operation, consistent state
```

## 4. Error Handling & Resilience

| Scenario | Handling | Status |
|----------|----------|--------|
| HF upload fails | Retry 3x with exponential backoff (2s → 4s → 8s) | ✅ |
| File already on HF | Overwrite (idempotent) | ✅ |
| File missing from HF (404) | Treat as success (already gone) | ✅ |
| Network timeout | Retry decorator handles | ✅ |
| Missing huggingface_hub | Auto-installed by setup.bat | ✅ |
| Git conflict | setup.bat exits with instruction | ✅ |
| Manifest corruption | Regenerated automatically | ✅ |
| Timestamp mismatch | Smart preservation (only update on change) | ✅ |

## 5. Data Consistency Model

### Guarantee 1: Local Control
- User's local edits always take precedence
- GitHub Actions never overwrites local commits

### Guarantee 2: Idempotency
- Running script multiple times without changes = no extra commits
- Timestamp preserved if content identical
- Safe to run multiple times

### Guarantee 3: Sync Integrity
- File deleted locally → automatically removed from HF
- File missing from HF → automatically removed from .gitignore
- Manifest always reflects current state

## 6. Version Evolution

| Version | Key Features | Date |
|---------|-------------|------|
| v3.2 | Basic dual-storage, GitHub Actions auto-commit | 2026-02 |
| v4.0 | Fixed GitHub Actions conflicts, read-only model | 2026-02-14 |
| v4.1 | Auto-delete rules, smart timestamps, 404 handling | 2026-02-15 |

## 7. Performance Characteristics

- **Scan**: O(n) where n = total files in repo
- **Upload**: O(m) where m = files >50MB (with retry = O(m×3) worst case)
- **Sync Deletion**: O(hf_files) where hf_files = files on HuggingFace
- **Manifest Generation**: O(n) with sorting overhead
- **Total Run Time**: Typically 30-60s for typical repos (varies by file size and network)
