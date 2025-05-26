import mistune
from urllib.parse import unquote

# 用于对解析到的Markdown元素进行转换，转化为LaTeX




class LaTeXRender(mistune.BaseRenderer):
    def __init__(self,my_config, escape=True, allow_harmful_protocols=None):
        super(LaTeXRender, self).__init__()
        self._allow_harmful_protocols = allow_harmful_protocols
        self._escape = escape
        self.my_config=my_config
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
        t=self.my_config["text"]
        t=t.replace("<text>",text)
        return t

    #*强调*
    def emphasis(self, text):
        t=self.my_config["emphasis"]
        t=t.replace("<text>",text)
        return t

    #**加粗**
    def strong(self, text):
        t=self.my_config["strong"]
        t=t.replace("<text>",text)
        return t

    #链接[text](url "title")
    def link(self, text: str, url: str, title="链接") -> str:
        t = self.my_config["link"]
        t=t.replace("<text>",text)
        t=t.replace("<url>",unquote(url))
        t=t.replace("<title>",title)
        return t

    #图像![alt](url "title")
    def image(self, alt: str, url: str, title="图片") -> str:
        t=self.my_config["image"]
        t=t.replace("<title>",title)
        t=t.replace("<url>",unquote(url))
        t=t.replace("<alt>",alt)
        return t

    #`行内代码`
    def codespan(self, text: str) -> str:
        t=self.my_config["codespan"]
        t=t.replace("<text>",text)
        return t

    def linebreak(self) -> str:
        t=self.my_config["linebreak"]
        return t

    def softbreak(self) -> str:
        t=self.my_config["softbreak"]
        return t

    # 行内HTML
    def inline_html(self, html: str) -> str:
        t=self.my_config["inline_html"]
        t=t.replace("<html>",html)
        return t

    ### block level ###

    #段落
    def paragraph(self, text: str) -> str:
        t=self.my_config["paragraph"]
        t=t.replace("<text>",text)
        return t

    #标题
    def heading(self, text: str, level: int, **attrs) -> str:
        heading_types = ['section', 'subsection', 'subsubsection']
        t=self.my_config["heading"]
        t=t.replace("<text>",text)
        t=t.replace("<heading_types>",heading_types[level-1])
        return t

    def blank_line(self) -> str:
        t=self.my_config["blank_line"]
        return t
    def thematic_break(self) -> str:
        t=self.my_config["thematic_break"]
        return t

    def block_text(self, text: str) -> str:
        t=self.my_config["block_text"]
        t=t.replace("<text>",text)
        return t

    def block_code(self, code: str, info=None) -> str:
        t=self.my_config["block_code"]
        t=t.replace("<code>",code)
        return t

    def block_quote(self, text: str) -> str:
        t=self.my_config["block_quote"]
        t=t.replace("<text>",text)
        return t

    def block_html(self, html: str) -> str:
        t=self.my_config["block_html"]
        t=t.replace("<html>",html)
        return t

    def block_error(self, text: str) -> str:
        raise NotImplementedError()

    def list(self, text: str, ordered: bool, **attrs) -> str:
        if ordered:
            t=self.ordered_list(text, **attrs)
        else: 
            t=self.disordered_list(text, **attrs)
        return t

    def ordered_list(self, text: str, **attrs) -> str:
        t=self.my_config["ordered_list"]
        t=t.replace("<text>",text)
        return t

    def disordered_list(self, text: str, **attrs) -> str:
        t=self.my_config["disordered_list"]
        t=t.replace("<text>",text)
        return t

    def list_item(self, text: str) -> str:
        t=self.my_config["list_item"]
        t=t.replace("<text>",text)
        return t
    
    ### provide by math plugin ###

    #行间公式
    def block_math(self, text):
        t=self.my_config["block_math"]
        t=t.replace("<text>",text)
        return t
    
    #行内公式
    def inline_math(self, text):
        t=self.my_config["inline_math"]
        t=t.replace("<text>",text)
        return t

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
        align="c"*len(row[0])
        body="\\\\\n        ".join(table)+"\\\\"
        return head,align,body
    
    #表格
    def table(self, text):
        head,align,body = self.csv_latex(text)
        t=self.my_config["table"]
        t=t.replace("<head>", head)
        t=t.replace("<align>", align)
        t=t.replace("<body>", body)
        return t

    def table_head(self, text):
        return text[:-1]

    def table_body(self, text):
        return text

    def table_row(self, text):
        return "\n"+text[:-1]

    def table_cell(self, text, align=None, head=False):
        return text+","
