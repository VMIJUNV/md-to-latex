import mistune
from LaTeXRenderer import LaTeXRender
from mistune.plugins.math import math
from mistune.plugins.table import table

Markdown_Path="Paper/test.md"
Template_Path="Tool/template.latex"
Latex_Path="Paper/output.tex"


# 表格模板(markdown原生)
table_template_text='''
\\begin{table}[H]
    \\centering
    \\begin{tabular}{<align>}
        \\toprule
        <head>
        \\midrule
        <body>
        \\bottomrule
    \\end{tabular}
\\end{table}
'''

# 表格模板(引用文件)
table_template_file='''
\\begin{table}[H]
    \\centering
    \\caption{<title>}
    \\label{<title>}
    \\csvautobooktabular{\\rootpath<url>}
\\end{table}
'''

# 图片模板
image_template='''
\\begin{figure}[H]
    \\centering
    \\includegraphics[width=0.4\\textwidth]{\\rootpath<url>}
    \\caption{<title>}
    \\label{<title>}
\\end{figure}
'''


with open(Markdown_Path, 'r', encoding='utf-8') as f:
    markdown_text = f.read()

with open(Template_Path, 'r', encoding='utf-8') as f:
    template = f.read()

render=LaTeXRender()
render.table_template_file=table_template_file
render.table_template_text=table_template_text
render.image_template=image_template

markdown = mistune.create_markdown(renderer=render,plugins=[math,table])

latex=markdown(markdown_text)

latex=template.replace("<!-- 插入 -->",latex)

with open(Latex_Path,'w',encoding='utf-8') as f:
    f.write(latex)
