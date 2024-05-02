import mistune
from urllib.parse import unquote

# 用于对解析到的Markdown元素进行转换，转化为LaTeX




class LaTeXRender(mistune.BaseRenderer):
    def __init__(self, escape=True, allow_harmful_protocols=None):
        super(LaTeXRender, self).__init__()
        self._allow_harmful_protocols = allow_harmful_protocols
        self._escape = escape
        self.table_template_file=""
        self.table_template_text=""
        self.image_template=""

    def render_token(self, token, state):
        # backward compitable with v2
        func = self._get_method(token['type'])
        attrs = token.get('attrs')

        if 'raw' in token:
            text = token['raw']
        elif 'children' in token:
            text = self.render_tokens(token['children'], state)
        else:
            if attrs:
                return func(**attrs)
            else:
                return func()
        if attrs:
            return func(text, **attrs)
        else:
            return func(text)
    
    ###########################

    ### inline level ###
    
    #普通文本
    def text(self, text: str) -> str:
        return text

    #*强调*
    def emphasis(self, text):
        return '\\emph{' + text + '}'

    #**加粗**
    def strong(self, text):
        return '\\textbf{' + text + '}'

    #链接[text](url "title")
    def link(self, text: str, url: str, title="链接") -> str:
        t=""
        if text =="表":
            t=self.table_template_file.replace("<title>",title)
            t=t.replace("<url>",unquote(url))
        elif text =="图":
            t=self.image_template.replace("<title>",title)
            t=t.replace("<url>",unquote(url))
        return t

    #图像![alt](url "title")
    def image(self, alt: str, url: str, title="图片") -> str:
        t=""
        t=self.image_template.replace("<title>",title)
        t=t.replace("<url>",unquote(url))
        return t

    #`行内代码`
    def codespan(self, text: str) -> str:
        return text

    def linebreak(self) -> str:
        return '\\\\'

    def softbreak(self) -> str:
        return '\n'

    # 行内HTML
    def inline_html(self, html: str) -> str:
        return html

    ### block level ###

    #段落
    def paragraph(self, text: str) -> str:
        return "\n"+text + "\n"

    #标题
    def heading(self, text: str, level: int, **attrs) -> str:
        heading_types = ['section', 'subsection', 'subsubsection']
        return "\n\\" + heading_types[level-1] + "{" + text + "}\n"

    def blank_line(self) -> str:
        return ''

    def thematic_break(self) -> str:
        return "\\noindent\\rule{\\textwidth}{1pt}\n"

    def block_text(self, text: str) -> str:
        return text+'\n'

    def block_code(self, code: str, info=None) -> str:
        return code

    def block_quote(self, text: str) -> str:
        return "\n\\begin{quote}" + text + "\\end{quote}\n"

    def block_html(self, html: str) -> str:
        return ""

    def block_error(self, text: str) -> str:
        raise NotImplementedError()

    def list(self, text: str, ordered: bool, **attrs) -> str:
        if not ordered:
            return "\n\\begin{itemize}\n" + text + "\\end{itemize}\n"
        else: 
            return "\n\\begin{enumerate}\n" + text + "\\end{enumerate}\n"

    def list_item(self, text: str) -> str:
       return "\\item " + text+"\n"
    
    ### provide by math plugin ###

    #行间公式
    def block_math(self, text):
        return "\n\\begin{equation}\n"+text+"\n\\end{equation}\n"
    
    #行内公式
    def inline_math(self, text):
        return "$"+text+"$"

    ### provide by table plugin ###

    #自定函数，csv转latex
    def csv_latex(self,csv):
        row=csv.split("\n")
        table=[]
        head=""
        for i,r in enumerate(row):
            row[i]=r.split(",")
            if i == 0:
                head=r.replace(',', ' & ')+"\\\\"
            else:
                table.append(r.replace(',', ' & '))
        t=self.table_template_text.replace("<align>","c"*len(row[0]))
        t=t.replace("<head>", head)
        t=t.replace("<body>", "\\\\\n        ".join(table)+"\\\\")
        return t
    
    #表格
    def table(self, text):
        return self.csv_latex(text)

    def table_head(self, text):
        return text[:-1]

    def table_body(self, text):
        return text

    def table_row(self, text):
        return "\n"+text[:-1]

    def table_cell(self, text, align=None, head=False):
        return text+","
