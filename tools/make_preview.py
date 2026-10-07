#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 exampaper.cls 的版式参数绘制试卷首页示意图（SVG）。

用途：无需 TeX 环境即可确认版式与原卷是否一致。
    python make_preview.py            # 输出 preview/layout.svg
    python make_preview.py --widget   # 额外输出可直接嵌入网页的版本

坐标说明：页面尺寸 A4 = 595.28pt x 841.89pt；下文的 y 采用「自上而下」，
与 PDF 中的量取值一致，因此可以直接和原卷比对。
"""

import argparse
import os

W, H = 595.28, 841.89          # A4
ML, MR = 105.3, 73.98          # 左右边距（geometry: left=3.7cm right=2.6cm）
MT, MB = 113.4, 71.1           # 上下边距（top=4cm bottom=2.5cm）
XR = W - MR                    # 版心右边界 521.3
XC = (ML + XR) / 2             # 版心中心 313.3

TITLE = "东南大学试卷（A卷）"
TITLE_SIZE = 17.28
TITLE_JU = 7.95                # 字距 0.46em

SONG = "SimSun, Songti SC, Noto Serif CJK SC, serif"
HEI = "SimHei, Heiti SC, Noto Sans CJK SC, sans-serif"
KAI = "KaiTi, Kaiti SC, Noto Serif CJK SC, serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, family=SONG, anchor="start", ls=0, weight="normal"):
    return (
        '<text x="%.2f" y="%.2f" font-size="%.2f" font-family="%s" '
        'text-anchor="%s" font-weight="%s"%s>%s</text>'
        % (
            x,
            y,
            size,
            family,
            anchor,
            weight,
            ' letter-spacing="%.2f"' % ls if ls else "",
            esc(s),
        )
    )


def vtext(x_base, y_start, s, size=12, family=SONG):
    """竖排文字：以 (x_base, y_start) 为起点，自下而上书写。"""
    return (
        '<text x="%.2f" y="%.2f" font-size="%.2f" font-family="%s" '
        'transform="rotate(-90 %.2f %.2f)">%s</text>'
        % (x_base, y_start, size, family, x_base, y_start, esc(s))
    )


def line(x1, y1, x2, y2, w=0.478, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return (
        '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#000" '
        'stroke-width="%.3f"%s/>' % (x1, y1, x2, y2, w, d)
    )


def rect(x, y, w, h):
    return (
        '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" '
        'stroke="#000" stroke-width="0.478"/>' % (x, y, w, h)
    )


def field(x_left, y, label, value, blank_w):
    """抬头信息栏一项：黑体项目名 + 楷体内容（居中）+ 下划线。返回 (svg 片段, 右端 x)。"""
    out = [text(x_left, y, label, 12, HEI)]
    ub_x = x_left + len(label) * 12 + 1.8
    out.append(text(ub_x + blank_w / 2, y, value, 12, KAI, anchor="middle"))
    out.append(line(ub_x, y, ub_x + blank_w, y))
    return out, ub_x + blank_w


def info_row(y, fields):
    """一行抬头信息栏：整体在版心内居中，各字段之间留 0.4em。"""
    gap = 0.4 * 12
    widths = [len(lab) * 12 + 1.8 + bw for lab, _, bw in fields]
    x = XC - (sum(widths) + gap * (len(fields) - 1)) / 2
    out = []
    for lab, val, bw in fields:
        frag, x = field(x, y, lab, val, bw)
        out += frag
        x += gap
    return out


def header_block():
    """标题 + 两行信息栏 + 评分表，返回 SVG 片段列表。"""
    out = []

    # --- 标题：居中、字距 ---
    n = len(TITLE)
    x_start = XC - ((n - 1) * TITLE_JU + n * TITLE_SIZE) / 2
    y_title = MT + 20.7 - 4.4          # ≈129.7
    for i, ch in enumerate(TITLE):
        out.append(
            text(
                x_start + i * (TITLE_SIZE + TITLE_JU),
                y_title,
                ch,
                TITLE_SIZE,
                SONG,
            )
        )

    # --- 信息栏第 1 行 ---
    y1 = y_title + 24.5
    fields1 = [
        ("课程名称", "高等数学分析", 3.4 * 28.4527),
        ("课程代码", "B07M1041", 2.2 * 28.4527),
        ("考试学期", "23-24-3", 1.8 * 28.4527),
    ]
    out += info_row(y1, fields1)

    # --- 信息栏第 2 行 ---
    y2 = y_title + 49.5
    fields2 = [
        ("适用专业", "选学高等数分各专业", 4.4 * 28.4527),
        ("考试形式", "闭  卷", 2.0 * 28.4527),
        ("考试时长", "150 分钟", 1.9 * 28.4527),
    ]
    out += info_row(y2, fields2)

    # --- 评分表 ---
    t_top, r_h, c_h, b_h = 202.6, 17.2, 25.8, 25.8
    y_table = [t_top, t_top + r_h, t_top + r_h + c_h, t_top + r_h + c_h + b_h]
    xs = [ML + i * (XR - ML) / 8 for i in range(9)]   # 9 条竖线 = 8 列
    out.append(line(ML, y_table[0], XR, y_table[0]))
    out.append(line(ML, y_table[1], XR, y_table[1]))
    out.append(line(ML, y_table[2], xs[7], y_table[2]))   # 横线不断开「总分」列
    out.append(line(ML, y_table[3], XR, y_table[3]))
    for i, x in enumerate(xs):
        y0 = y_table[0]
        out.append(line(x, y0, x, y_table[3]))
    heads = ["题号"] + ["一", "二", "三", "四", "五", "六"] + ["总分"]
    for i, lab in enumerate(heads):
        cx = (xs[i] + xs[i + 1]) / 2
        if i == 0 or i == 7:
            out.append(text(cx, y_table[0] + 12.3, lab, 12, HEI, anchor="middle"))
        else:
            out.append(text(cx, y_table[0] + 12.3, lab, 12, HEI, anchor="middle"))
    out.append(text((xs[0] + xs[1]) / 2, y_table[1] + 17.0, "得分", 12, HEI, anchor="middle"))
    out.append(text((xs[0] + xs[1]) / 2, y_table[2] + 17.0, "评阅人", 12, HEI, anchor="middle"))
    out.append(
        text((xs[7] + xs[8]) / 2, (y_table[0] + y_table[3]) / 2 + 4.3, "总分", 12, HEI, anchor="middle")
    )

    # --- 大题标题与小题目（示例）---
    y = y_table[3] + 14.4 + 14.5
    out.append(text(ML + 9.6, y, "一、填空题（本题共2小题，每小题4分，满分8分）", 12, HEI))
    y += 13 + 9.6
    q1 = "1. 设 f(x) = x²，则 f′(1) = ________。"
    out.append(text(ML + 9.6, y, q1, 12, SONG))
    y += 27.5
    out.append(
        text(ML + 9.6, y, "2. 设 D = [0,1] × [0,1]，则  ∬ x dσ = ________。", 12, SONG)
    )
    return out


def sidebar():
    out = []
    # 考场纪律提示：自下而上，三段之间留 17.5pt
    y = H - 286.0
    for seg in ["自觉遵守考场纪律", "如考试作弊", "此答卷无效"]:
        out.append(vtext(27.9, y, seg, 12, SONG))
        y -= (len(seg) * 12 + 17.5)
    # 学号 / 姓名（自下而上）
    y = H - 283.5
    out.append(vtext(53.1, y, "学号", 12, HEI))
    out.append(line(54.8, y - 26.6, 54.8, y - 123.0))
    out.append(vtext(53.1, y - 132.0, "姓名", 12, HEI))
    out.append(line(54.8, y - 158.6, 54.8, y - 255.0))
    # 密封线：点线 + 密 封 线（自下而上）
    out.append(line(75.4, H - 145.5, 75.4, H - 661.5, dash="1 4.3"))
    for label, y_bu in [("密", 272.7), ("封", 405.2), ("线", 537.7)]:
        out.append(vtext(76.0, H - y_bu, label, 12, KAI))
    return out


def footer():
    y = H - 65.4
    return [
        text(
            XC,
            y,
            "高等数学分析期末试卷(A)     共 6 页     第 1 页",
            10,
            SONG,
            anchor="middle",
        )
    ]


def build(page=True, widget=False):
    body = []
    body += header_block()
    body += sidebar()
    body += footer()
    inner = "\n  ".join(body)
    if widget:
        # 深色背景下展示：白色纸面 + 外边距
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 900" '
            'width="680" height="900">\n'
            '  <rect x="0" y="0" width="680" height="900" rx="10" fill="#1e1f22"/>\n'
            '  <g transform="translate(42.36,29)">\n'
            '    <rect x="0" y="0" width="595.28" height="841.89" fill="#ffffff" '
            'stroke="#3c3f41" stroke-width="0.5"/>\n'
            "  %s\n" % inner
            + "  </g>\n</svg>\n"
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 595.28 841.89" '
        'width="595.28" height="841.89">\n'
        '  <rect x="0" y="0" width="595.28" height="841.89" fill="#ffffff"/>\n'
        "  %s\n</svg>\n" % inner
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--widget", action="store_true", help="额外输出网页嵌入版")
    ap.add_argument("--out", default="preview/layout.svg")
    ap.add_argument("--widget-out", default="layout_widget.svg")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(build(widget=False))
    print("written:", args.out)
    if args.widget:
        with open(args.widget_out, "w", encoding="utf-8") as f:
            f.write(build(widget=True))
        print("written:", args.widget_out)


if __name__ == "__main__":
    main()
