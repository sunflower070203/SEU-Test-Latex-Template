# exampaper —— 通用中文试卷 LaTeX 模板

一个可直接套用的中文试卷（期末考试卷）LaTeX 模板，提供了中文试卷常见的全部版式要素：

- A4 / 12pt，正文**宋体**、栏目与表格标题**黑体**、填写内容**楷体**，数学公式为 Computer Modern（原卷风格）；
- 试卷标题大字号 + 自动字距（`东 南 大 学 试 卷 （A卷）` 那种效果）；
- 抬头信息栏：`课程名称 / 课程代码 / 考试学期 / 适用专业 / 考试形式 / 考试时长`，带下划线填空；
- 评分表：`题号 | 一 | 二 | … | 总分`，`得分 / 评阅人` 两行，「总分」列自动跨行合并；
- 大题自动编号（`一、` `二、` `三、` …），小题自动编号（`1.` `2.` …），每题后可留答题空间；
- 左侧竖排**密封线**（考场纪律提示 + 学号/姓名 + 点线「密 封 线」），逐页出现在背景层；
- 页脚：`试卷名   共 X 页   第 Y 页`。

版式参数来自一份真实的期末试卷（A4，正文宽 14.70cm，页顶留白 4cm），抽取时保留了页面几何、
字号、行距、表格线与密封线的实际坐标，因此外观与原卷基本一致。**题目内容不在模板范围内**，
请自行填写。

## 效果预览

`preview/layout.svg` 是按模板参数绘制的版式示意图（非编译结果，仅供确认版式）：

![版式示意图](preview/layout.svg)

## 环境要求

| 项目 | 要求 |
| --- | --- |
| 编译器 | **XeLaTeX**（推荐）或 LuaLaTeX；中文不建议用 pdfLaTeX |
| TeX 发行版 | TeX Live 2020+ / MiKTeX 21+ / MacTeX（MacTeX 亦可） |
| 宏包 | `ctex`、`geometry`、`amsmath`、`graphicx`、`array`、`tabularx`、`multirow`、`lastpage`、`eso-pic`、`fancyhdr`（前两者之外都是常见宏包，随发行版自带） |
| 中文字体 | Windows 自带即可；macOS / Linux 见下文「字体」 |

## 编译

```bash
# 推荐：连续编译两遍，页脚「共 X 页」才正确
xelatex main.tex
xelatex main.tex

# 或者
latexmk -xelatex main.tex
```

### 在 Overleaf 上使用（已实测通过）

1. New Project → Upload Project，上传本项目的 zip。
2. **必须改编译器**：左下角 Settings → Compiler → 选 `XeLaTeX`（默认是 pdfLaTeX，
   会出现 `CTeX fontset 'fandol' is unavailable` + `Package CJK Error: Invalid character code`）。
   项目自带的 `latexmkrc`（`$pdf_mode = 5`）**不能**覆盖 Overleaf 的项目级编译器设置，
   实测仍会走 pdfLaTeX，所以这一步必须手动做。
3. 若报找不到字体，把 `\documentclass[12pt,a4paper]{exampaper}` 换成
   `\documentclass[fontset=fandol]{exampaper}`（Overleaf 是 Linux 环境，默认字体集为 fandol）。

> 本模板在文档类里已加入引擎检测：用 pdfLaTeX 编译时会直接报
> 「本模板包含中文，必须使用 XeLaTeX 或 LuaLaTeX 编译」，而不是抛出一堆看不懂的错。

## 文件说明

```
exampaper.cls          模板本体（版式、字体、评分表、密封线、插图、页脚全部在这里）
main.tex               试卷入口：默认是空骨架（只有抬头 + 评分表 + 各栏占位，不含题目）
example-exam.tex       示例内容（虚构题目），由 main.tex 在 \showexampletrue 时引入
figures/               放图片的目录（示例图 sample-figure.png 在这里）
latexmkrc              让 latexmk / Overleaf 走 XeLaTeX
preview/layout.svg     版式示意图
tools/make_preview.py  生成上面这张示意图的脚本（可选，不参与编译）
LICENSE                MIT
```

**模板不带题目**：默认编译 `main.tex` 出来的是空骨架，所有「〈…〉」都是占位符。
想先看完整排版效果（虚构题目 + 插图 + 公式），把 `main.tex` 里的
`\showexamplefalse` 改成 `\showexampletrue` 再编译一次即可，改回来就是空模板。

## 快速开始

改 `main.tex` 即可，骨架长这样（把「〈…〉」换成自己的信息，题目写在各栏里）：

```latex
\documentclass[12pt,a4paper]{exampaper}
\examname{〈试卷名〉}                       % 页脚左侧

\begin{document}
\examtitle{〈学校名〉试卷（A 卷）}           % 大标题，自动加字距

\begin{center}                             % 抬头信息栏
  \examfield[3.4cm]{课程名称}{〈课程名称〉}\hspace{0.4em}%
  \examfield[2.2cm]{课程代码}{〈课程代码〉}\hspace{0.4em}%
  \examfield[1.8cm]{考试学期}{〈20xx-xx-x〉}\\[0.4em]
  \examfield[4.4cm]{适用专业}{〈适用专业〉}\hspace{0.4em}%
  \examfield[2.0cm]{考试形式}{闭\hspace{0.5em}卷}\hspace{0.4em}%
  \examfield[1.9cm]{考试时长}{〈150〉\hspace{0.4em}分钟}
\end{center}

\examscoretable[6]                         % 评分表，6 = 评阅栏数

\examsection{〈第一栏标题，如：填空题（本题共 ? 小题，每小题 ? 分，满分 ? 分）〉}
\begin{examquestions}
  \examquestion 〈题干〉
\end{examquestions}

\examsection{〈第二栏标题，如：计算题（本题共 ? 小题…）〉}
\begin{examquestions}[7cm]                 % 7cm = 每题后留出的答题空间
  \examquestion 〈题干〉
\end{examquestions}

\end{document}
```

想直接看效果，编译 `example-exam.tex`（虚构题目，含插图与公式的完整写法）。

## 插图

`graphicx` 已加载，图片放在 `figures/` 目录下：

```latex
\examfigure[0.6\textwidth]{图题}{figures/sample-figure.png}   % 一行插图 + 自动图号
```

第一个参数是宽度（默认 `0.6\textwidth`）。需要标准 `figure` 浮动体时直接用：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.5\textwidth]{figures/your-image.png}
  \caption{图题}\label{fig:your}
\end{figure}
```

png / jpg / pdf 都可直接插入；svg 请先在外部转成 pdf。表格用标准 `tabular`
（`array`、`tabularx`、`multirow` 已加载），放在题干里即可。

## 多页试卷

页数不用手写：**内容变多就自动加页**（默认的空骨架刚好 1 页，`\showexampletrue` 的示例是 3 页）。
下面这些东西已经做成「每页自动都有」，不需要额外设置：

- 页脚 `试卷名   共 X 页   第 Y 页`（`lastpage` + `fancyhdr`，连 `plain` 样式页也装了同一个页脚）；
- 左侧竖排密封线（画在 `eso-pic` 背景层，逐页输出）。

抬头（标题 + 信息栏）和评分表只出现在第 1 页 —— 它们本来就是一次性内容。

控制分页的常用手段：

| 需求 | 写法 |
| --- | --- |
| 让某道大题整体挪到下一页开头 | 在 `\examsection{...}` 前加 `\newpage`（示例文件里演示了一次） |
| 长题目自动断开 | 不用管，LaTeX 会在行间自动分页 |
| 加/减答题空间 | 调 `\begin{examquestions}[7cm]` 的间距，或改 `\examitemsep` |
| 整份试卷不要密封线 | 导言区写 `\examsidebarfalse` |

两个容易踩的点：

1. **必须编译两遍**（Overleaf 默认就会跑两遍）。只编一遍时页脚「共 X 页」会显示上一轮的页数，
   可能看到 `??` 或旧数字。
2. **单处答题留白别超过一页**。`[7cm]` 是纯垂直空白，如果当前页只剩 3cm 而你要 7cm，
   空白会被切到下一页，看起来像「这道题的答题位置不见了」。对策：把间距调小，
   或者在 `\examsection` 前用 `\newpage` 让这道大题从新页开始。

## 命令速查

| 命令 | 说明 |
| --- | --- |
| `\examtitle{...}` | 试卷大标题：居中、`\Large`、字符自动加字距 |
| `\examname{...}` | 页脚中显示的试卷名，如「高等数学分析期末试卷(A)」 |
| `\examfield[宽]{项目名}{内容}` | 抬头信息栏的一项。宽度即下划线长度；内容留空 `{}` 得到空白横线；内容为楷体 |
| `\examscoretable[大题数]` | 评分表。参数默认 6，即 6 个评阅格；表格宽度自动撑满版心 |
| `\examsection{栏目标题}` | 大题标题，自动加「一、」「二、」…；同时把小题编号重置为 1 |
| `\begin{examquestions}[题间距]` … `\end{examquestions}` | 带编号的小题区。默认题间距 `\examitemsep`（13pt，填空题用）；给如 `[9cm]` 即每题后留出答题空间 |
| `\examquestion` | 输出「1.」「2.」…（每道大题内重新计数） |
| `\begin{examproblem}` … `\end{examproblem}` | 不带编号的单个大题（「三、（本题满分8分）」这类） |
| `\examfigure[宽]{图题}{图片文件}` | 插入一张图并自动给图号；`graphicx` 已加载，也可用标准 `figure` 环境 |
| `\examsidebarfalse` | 放在导言区，关闭左侧密封线 |
| `\question` | `\examquestion` 的短别名（仅当 `\question` 未被占用时定义） |

## 版式参数

参数集中在 `exampaper.cls` 的注释块里，直接改即可：

| 参数 | 默认 | 含义 |
| --- | --- | --- |
| `geometry` | `top=4cm, bottom=2.5cm, left=3.7cm, right=2.6cm` | 页边距。左边距较大是为密封线留位置 |
| `\parindent` | `0.8em`（≈9.6pt） | 段落首行缩进，也用于大题标题位置 |
| `\examindent` | `0.8em` | 题目整体左缩进（题干换行后与首行左端对齐，与原卷一致） |
| `\examziju` | `0.46em` | 试卷标题的字距（相对标题字号） |
| `\examitemsep` | `13pt` | `examquestions` 的默认题间距 |
| `\examsectionpreskip` / `\examsectionpostskip` | `1.2em` / `0.4em` | 大题标题上/下间距 |
| `\exam@warn` `\exam@id` `\exam@seal` | — | 密封线三行竖排文字的内容 |
| `\exam@side` 中的 `\put(x,y)` | `(27.9,286) (53.1,283.5) (76,145.5)` | 密封线三行文字的坐标，单位 pt，原点在**页面左下角** |

> 密封线是画在背景层（`eso-pic`）上的，位置用绝对坐标控制。若换成非 A4 纸或大改页边距，
> 需要相应调整这三个 `\put` 坐标。

## 常见问题

**页脚显示「共 ?? 页」或页数不对** —— 编译两遍即可（`lastpage` 需要这一轮才知道总页数）。

**密封线不在左侧 / 跑到别处** —— 密封线依赖 `eso-pic` 的背景层坐标（原点为页面左下角），
请确认 `eso-pic` 版本 ≥ 1.3；如需微调直接改 `\exam@side` 里的数字。

**提示字体缺失（XXX font not found）** —— 说明当前系统的 ctex 字体集不匹配：

```latex
\documentclass[fontset=windows]{exampaper}  % Windows：宋体/黑体/楷体
\documentclass[fontset=mac]{exampaper}      % macOS：Songti SC 等
\documentclass[fontset=ubuntu]{exampaper}   % Linux（需装 fonts-noto-cjk 等）
\documentclass[fontset=fandol]{exampaper}   % 随 TeX Live 附带，任何平台都能编
```

**提示 `Overfull \hbox`（文本超出版心）** —— 抬头信息栏/题干写得太宽，减小 `\examfield`
的宽度参数或换行即可。

**想换成自己学校的名字** —— 直接改 `\examtitle{...}`；有校名要求的可以把标题拆成两行。

## 发布到 GitHub

本仓库已经初始化过本地 git 并完成首次提交，直接推送即可：

```bash
# 方式一：GitHub CLI
gh repo create latex-exam-paper-template --public --source=. --push

# 方式二：先在 GitHub 网页端建空仓库，再
git remote add origin git@github.com:<你的用户名>/latex-exam-paper-template.git
git push -u origin main
```

建议 push 前先本地编译一遍（`xelatex main.tex` 两遍），确认效果后把生成的 PDF 一并发布。

## 许可

MIT License，见 `LICENSE`。欢迎自由修改、分发；若对版式做了改进，欢迎提 PR。
