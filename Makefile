# 试卷模板 Makefile —— 一键编译（XeLaTeX）
#
#   make            编译试卷（跑两遍，页脚「共 X 页」才正确）
#   make quick      只跑一遍，快速看效果
#   make preview    重新生成版式示意图 preview/layout.svg
#   make clean      清理辅助文件，保留 PDF
#   make cleanall   清理辅助文件和生成的 PDF
#
# 换主文件（例如想直接编译示例）：make MAIN=example-exam

MAIN   ?= main
ENGINE ?= xelatex
OPTS    = -xelatex -interaction=nonstopmode -synctex=1

.PHONY: all quick preview clean cleanall

all:
	latexmk $(OPTS) $(MAIN).tex

quick:
	$(ENGINE) -interaction=nonstopmode $(MAIN).tex

preview:
	python3 tools/make_preview.py

clean:
	latexmk -c $(MAIN).tex

cleanall:
	latexmk -C $(MAIN).tex
