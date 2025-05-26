import tkinter as tk
from tkinter import filedialog,messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys
import md_to_latex
import json
from pathlib import Path

path=sys.path[0]
path=Path(path)


class Record():
    def __init__(self,record_path):
        self.record_path = Path(record_path)
        self.load()
    def load(self):
        with open(self.record_path, 'r', encoding='utf-8') as f:
            text = f.read()
            self.record = json.loads(text)
    def save(self):
        with open(self.record_path, 'w', encoding='utf-8') as f:
            text = json.dumps(self.record,ensure_ascii=False,indent=4)
            f.write(text)

record_path=path / "record.json"
record=Record(record_path)

def updata_file_path(file_path):
    if not file_path:
        return
    md_path_ = Path(file_path).resolve()
    customer_convert_config_path_=md_path_.parent / "customer_convert_config.yaml"
    customer_convert_template_path_=md_path_.parent / "customer_convert_template.txt"
    output_path_ = md_path_.with_suffix(".tex")

    if md_path_.suffix == ".md":  # 判断是否为 .md
        md_path_entry.delete(0, tk.END)  # 清空 tkinter 的 Entry 组件中的内容
        md_path_entry.insert(0, str(md_path_))

        customer_convert_template_path_entry.delete(0, tk.END)
        customer_convert_template_path_entry.insert(0, str(customer_convert_template_path_))
        
        customer_convert_config_path_entry.delete(0, tk.END)
        customer_convert_config_path_entry.insert(0, str(customer_convert_config_path_))

        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, str(output_path_))
    else:
        messagebox.showwarning("警告", "请打开一个Markdown文件")

def select_file(event=None):
    file_path = filedialog.askopenfilename()
    updata_file_path(file_path)
def drop_file(event):
    files = event.data
    f=files.split(' ')
    if len(f)>=2:
        messagebox.showwarning("警告", "请拖入一个Markdown文件\n(也有可能文件名有特殊字符，例如空格，可以尝试点击选取文件)")
    else:
        file_path=f[0]
        updata_file_path(file_path)

def perform_task():
    md_path = md_path_entry.get()
    customer_convert_config_path  = customer_convert_config_path_entry.get()
    customer_convert_template_path = customer_convert_template_path_entry.get()
    output_path=output_path_entry.get()

    try:
        md_to_latex.convert(md_path=md_path,
                            customer_convert_config_path=customer_convert_config_path,
                            customer_convert_template_path=customer_convert_template_path,
                            output_path=output_path)
        confirm_button.config(bg="green")
        confirm_button.config(text="转换成功")
        # 记忆转换历史
        record.record['md_path']=md_path
        record.record['customer_convert_config_path']=customer_convert_config_path
        record.record['customer_convert_template_path']=customer_convert_template_path
        record.record['output_path'] = output_path
        record.save()
    except:
        confirm_button.config(bg="red")
        confirm_button.config(text="转换失败")
    def reset_color():
        confirm_button.config(bg="white")
        confirm_button.config(text="点击转换")

    confirm_button.after(1000, reset_color)


# 创建一个窗口
window = TkinterDnD.Tk()
window.title("Markdown转LaTeX")
# window.resizable(True, False)
window.minsize(300, 500)
window.configure(background='white')

# 文件输入区

file_interaction_frame = tk.Frame(window)
file_interaction_frame.grid(row=0, column=0,sticky="nsew")
file_interaction_frame.grid_columnconfigure(0, weight=1)
file_interaction_frame.grid_rowconfigure(0, weight=1)

file_select_frame = tk.Frame(file_interaction_frame, borderwidth=2,relief="solid",height=150)
file_select_frame.grid(row=0, column=0,padx=10,pady=20,sticky="nsew")
file_select_frame.grid_propagate(False)
file_select_frame.grid_columnconfigure(0, weight=1)
file_select_frame.grid_rowconfigure(0, weight=1)

file_select_frame.drop_target_register(DND_FILES)
file_select_frame.dnd_bind('<<Drop>>', drop_file)

file_select_bottom = tk.Label(file_select_frame, text="将Markdown文件拖放至此处\n\n或\n\n点击选择文件",bg='lightgray',bd=2, cursor='hand2')
file_select_bottom.grid(row=0, column=0,sticky="nsew")
file_select_bottom.bind('<Button-1>', select_file)

file_path_frame = tk.Frame(file_interaction_frame)
file_path_frame.grid(row=1, column=0,sticky='nsew')
file_path_frame.grid_columnconfigure(0, weight=1)

md_path_entry = tk.Entry(file_path_frame,relief="solid")
customer_convert_config_path_entry = tk.Entry(file_path_frame,relief="solid")
customer_convert_template_path_entry = tk.Entry(file_path_frame,relief="solid")
output_path_entry = tk.Entry(file_path_frame,relief="solid")

md_path_label = tk.Label(file_path_frame,text='Markdown文件路径:')
customer_convert_config_path_label = tk.Label(file_path_frame,text='自定转化配置文件路径:')
customer_convert_template_path_label = tk.Label(file_path_frame,text='自定转化模版文件路径:')
output_path_label = tk.Label(file_path_frame,text='输出路径:')

# 加载记录
md_path_entry.insert(0, record.record['md_path'])
customer_convert_template_path_entry.insert(0, record.record['customer_convert_template_path'])
customer_convert_config_path_entry.insert(0, record.record['customer_convert_config_path'])
output_path_entry.insert(0, record.record['output_path'])

md_path_label.grid(row=0,column=0,sticky='w',padx=10)
md_path_entry.grid(row=1,column=0,sticky='nsew',padx=10,pady=(0,10))

customer_convert_config_path_label.grid(row=2,column=0,sticky='w',padx=10)
customer_convert_config_path_entry.grid(row=3,column=0,sticky='nsew',padx=10,pady=(0,10))

customer_convert_template_path_label.grid(row=4,column=0,sticky='w',padx=10)
customer_convert_template_path_entry.grid(row=5,column=0,sticky='nsew',padx=10,pady=(0,10))

output_path_label.grid(row=6,column=0,sticky='w',padx=10)
output_path_entry.grid(row=7,column=0,sticky='nsew',padx=10,pady=(0,10))

# 交互区
interaction_frame = tk.Frame(window, bg="white")
interaction_frame.grid(row=1, column=0,sticky="nsew")
interaction_frame.grid_rowconfigure(0, weight=1)
interaction_frame.grid_columnconfigure(0, weight=1)

confirm_button = tk.Button(interaction_frame, text="点击转换",width=20,height=2 ,bg= "white" ,relief="solid", command=perform_task)
confirm_button.grid(row=0, column=0,padx=10, pady=10)

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)
window.mainloop()
