# Pages UI Design Specification v1.0

Mandatory design constraints for the `index.html` GitHub Pages frontend.
Any implementation MUST conform to these specifications exactly.

## Design System

### Color Tokens (CSS Custom Properties)

Light mode (`:root`):
| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#4f46e5` | Active states, focus rings, filter tags |
| `--primary-hover` | `#4338ca` | Button hover |
| `--bg-light` | `#f8fafc` | Page background, input background, stats background |
| `--card-bg` | `rgba(255, 255, 255, 0.8)` | Main container (glassmorphism) |
| `--text-main` | `#1e293b` | Primary text |
| `--text-muted` | `#64748b` | Secondary text, labels |
| `--border` | `#e2e8f0` | Borders, button default bg |
| `--folder` | `#e36209` | Folder icons |
| `--hf-badge-bg` | `#fef3c7` | HuggingFace badge background |
| `--hf-badge-text` | `#92400e` | HuggingFace badge text |
| `--highlight` | `rgba(249, 171, 0, 0.1)` | Search match highlight |

Dark mode (`[data-theme="dark"]`):
| Token | Value |
|-------|-------|
| `--primary` | `#818cf8` |
| `--primary-hover` | `#a5b4fc` |
| `--bg-light` | `#0f172a` |
| `--card-bg` | `rgba(30, 41, 59, 0.7)` |
| `--text-main` | `#f1f5f9` |
| `--text-muted` | `#94a3b8` |
| `--border` | `#334155` |
| `--folder` | `#fb923c` |
| `--hf-badge-bg` | `#451a03` |
| `--hf-badge-text` | `#fbbf24` |
| `--highlight` | `rgba(249, 171, 0, 0.2)` |

### Typography

- Primary: `"Inter"` (Google Fonts, weights: 400/500/600/700)
- Headings: `"Outfit"` (Google Fonts, weights: 400/500/600/700)
- Fallback: `-apple-system, sans-serif`
- H1 size: `2.5rem` (desktop), `1.8rem` (mobile <=640px)

### Badge Styles

Two badge types, both with `border: 1px solid rgba(0, 0, 0, 0.05)`:

| Badge | Background | Text | Label |
|-------|-----------|------|-------|
| HuggingFace | `var(--hf-badge-bg)` | `var(--hf-badge-text)` | `🤗 HF` |
| GitHub | `#e0e7ff` | `#3730a3` | `📦 Git` |

Both: `padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700`

## Layout Structure

```
┌─ .container (max-width: 1100px, glassmorphism, border-radius: 24px) ──────┐
│                                                                            │
│  ┌─ header (flex, space-between, align-center) ────────────────────────┐  │
│  │  <h1> ${REPO_NAME}          [GitHub] [HuggingFace 🤗] [Theme 🌓]  │  │
│  │  (gradient text)            (.header-actions, flex, gap: 8px)       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─ section.search-area ───────────────────────────────────────────────┐  │
│  │  ┌─ .search-wrapper (flex, gap: 12px) ──────────────────────────┐  │  │
│  │  │  [🔍 搜搜你想找的资料... (支持文件名和路径)]    [清空]        │  │  │
│  │  │  (#searchInput, border-radius: 16px)    (.btn-clear)         │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─ .filter-tags (flex, gap: 10px, flex-wrap) ──────────────────┐  │  │
│  │  │  [全部] [PDF 文档] [项目源码] [压缩包]                        │  │  │
│  │  │  (pill-shaped, border-radius: 100px)                          │  │  │
│  │  └──────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─ main#file-list.file-tree (min-height: 300px) ─────────────────────┐  │
│  │  📁 folder/ (collapsible, toggle-icon ▶ rotates 90deg)             │  │
│  │    📕 file.pdf  [🤗 HF]                               0.5 MB      │  │
│  │    📄 file.txt  [📦 Git]                               0.1 MB      │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  ┌─ footer#stats.stats (grid, auto-fit minmax(200px, 1fr)) ───────────┐  │
│  │  文件总数      GitHub 文件     HuggingFace 大文件    资料总体积     │  │
│  │  XXX 个        XXX 个          XXX 个                XXX.X MB       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### Header Buttons (`.icon-btn`)
- Size: `44px × 44px`, border-radius: `12px`
- Background: `var(--border)` → hover: `var(--primary)` + `color: white` + `scale(1.05)`
- Three buttons in order: GitHub SVG link, HuggingFace 🤗 link, Theme toggle
- GitHub SVG: 16×16 viewBox, Octicon mark, `fill: currentColor`
- Links: `target="_blank" rel="noopener"`

### Search Input (`#searchInput`)
- Padding: `14px 20px`
- Border: `2px solid var(--border)` → focus: `var(--primary)` + `box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1)`
- Border-radius: `16px`
- Placeholder: `🔍 搜搜你想找的资料... (支持文件名和路径)`

### Clear Button (`.btn-clear`)
- Always visible next to search input (NOT hidden/toggle)
- Text: `清空`
- Default: `background: var(--border); color: var(--text-muted)`
- Hover: `background: #ef4444; color: white`
- On click: clear input, reset search state, **focus back to search input**

### Filter Tags (`.tag`)
- Pill-shaped: `border-radius: 100px`
- Default: `background: var(--bg-light); border: 1px solid var(--border); color: var(--text-muted)`
- Active: `background: var(--primary); color: white; border-color: var(--primary)`
- Hover (inactive): `border-color: var(--primary); color: var(--primary)`
- Required tags (in order): `全部` | `PDF 文档` | `项目源码` | `压缩包`
- Data attributes: `data-filter="all"` | `"pdf"` | `"code"` | `"archive"`

### File Tree
- Folder header: `font-weight: 600`, toggle icon `▶` rotates 90deg when open
- Folder icon: `📁` with `color: var(--folder)`
- Folder display name must end with trailing `/` (e.g. `📁 folder-name/`)
- Folder children: `margin-left: 28px; border-left: 1.5px solid var(--border)`
- Default state: folders collapsed (unless searching)
- File item: hover `translateX(4px)` + background color change
- HF file links: must include `download` attribute

### File Icons (by extension)
```
pdf→📕  zip/rar/7z/tar/gz→📦  py→🐍  js→⚡  html/htm→🌐
md→📝  txt→📄  ipynb→📓  jpg/jpeg/png/gif/svg/webp→🖼️
mp4→🎬  pptx/xlsx/csv→📊  default→📄
```

### Stats Footer (`.stats`)
- Grid layout: `repeat(auto-fit, minmax(200px, 1fr))`
- 4 stat cards: 文件总数 | GitHub 文件 | HuggingFace 大文件 | 资料总体积
- Label: uppercase, `letter-spacing: 1px`, `font-size: 0.8rem`
- Value: `font-weight: 700`, `font-size: 1.1rem`
- Mobile (<=640px): single column

### Search Highlight
- Matching files/folders: `background: var(--highlight); border-left: 3px solid var(--primary)`
- Search active: all folders auto-expand
- Search text match: wrap matched substring with `<mark class="text-match">` on both folder names and file names
- `mark.text-match`: `background: rgba(251, 191, 36, 0.4); color: inherit; border-radius: 4px; padding: 0 2px`
- `highlightText()` must escape regex special characters to prevent XSS: `query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')`

## Behavioral Requirements

### Theme Toggle
- Persist to `localStorage` key `"theme"`
- On load: read from localStorage, default `"light"`
- Icon: light mode shows `🌙`, dark mode shows `☀️`
- Toggle updates: `data-theme` attribute on `<body>`, localStorage, icon text

### File Type Classification
```
config.codeExts = ["py", "java", "cpp", "c", "js", "go", "sh", "ipynb", "md"]
config.archiveExts = ["zip", "rar", "7z", "tar", "gz", "bz2"]
config.previewExts = ["pdf", "jpg", "jpeg", "png", "gif", "svg", "webp", "txt", "json", "html", "htm"]
```
- PDF filter matches `ext === "pdf"` only
- Code filter matches `config.codeExts`
- Archive filter matches `config.archiveExts`

### Hidden Root Folders
- `config.hiddenRootFolders = ["data", "scripts"]`
- These top-level directories are filtered from display (infrastructure folders)

### File URLs
- HuggingFace files (`isHF === true`): use manifest `url` field directly
- GitHub files with preview extension: relative path `./path`
- GitHub files without preview extension: `https://github.com/{user}/{repo}/blob/{branch}/{path}`

### Data Source
- Primary: fetch from `./data/file_manifest.json?t={timestamp}` (cache bust)
- Fallback: parallel fetch GitHub Trees API `https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1`; only use API result when manifest fails or returns empty
- Map `is_hf` → `isHF` boolean on each file entry
- Empty result: show `🔍 没找到匹配的文件，换个关键词试试？`
- Error: show red error text with `e.message`
- Loading: show skeleton shimmer animation (5 animated bars with varying widths: 40%, 100%, 80%, 60%, 100%), NOT plain text loader

### Skeleton Loading
- Container: `.skeleton-tree` with `border-top: 1px solid var(--border); padding-top: 20px`
- Items: `.skeleton-item` with `height: 40px; border-radius: 10px; margin-bottom: 10px`
- Animation: `@keyframes shimmer` — `linear-gradient(90deg, var(--border) 25%, var(--bg-light) 50%, var(--border) 75%)` with `background-size: 200% 100%` animated `1.5s infinite linear`
- 5 skeleton bars with widths: `40%`, `100%`, `80%`, `60%`, `100%`

### Animations
- Container: `fadeIn 0.4s ease-out` (opacity 0→1, translateY 10px→0)
- Transitions: `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)` on interactive elements

## Glassmorphism Effect

Container must have:
- `backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px)`
- `background: var(--card-bg)` (semi-transparent)
- `box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)`
- Body background: two radial gradients for subtle color wash

## Mobile Responsiveness (<=640px)

- Container: `padding: 20px; border-radius: 0` (full-width)
- H1: `font-size: 1.8rem`
- Stats grid: single column
- Header: `flex-wrap: wrap; gap: 20px`

## H1 Gradient

```css
background: linear-gradient(135deg, var(--primary), #ec4899);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

Pink endpoint `#ec4899` is constant across light/dark modes.
