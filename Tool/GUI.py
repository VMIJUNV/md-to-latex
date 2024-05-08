import tkinter as tk
from tkinter import filedialog,messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import os.path as op
import sys
import md_to_latex

path=sys.path[0]
history_path=op.join(path,"history.txt")
template_path=op.join(path,"template.latex")

def select_file_path(event=None):
    file_path = filedialog.askopenfilename()
    f=os.path.normpath(file_path)
    file_base, file_extension = op.splitext(f)
    if file_extension==".md":
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, f)
    else:
        messagebox.showwarning("警告", "请打开一个Markdown文件")

def drop(event):
    files = event.data
    f=files.split(' ')
    if len(f)>=2:
        messagebox.showwarning("警告", "请拖入一个Markdown文件\n(也有可能文件名有特殊字符，例如空格，可以尝试点击选取文件)")
    else:
        f=f[0]
        f=os.path.normpath(f)
        file_base, file_extension = op.splitext(f)
        if file_extension==".md":
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, f)
        else:
            messagebox.showwarning("警告", "请拖入一个Markdown文件\n(也有可能文件名有特殊字符，例如空格，可以尝试点击选取文件)")


def perform_task():
    file_path = file_path_entry.get()
    try:
        md_to_latex.main(file_path)
        confirm_button.config(bg="green")
        confirm_button.config(text="转换成功")
        # 记忆转换历史
        with open(history_path,'w',encoding='utf-8') as f:
            f.write(file_path)
    except:
        confirm_button.config(bg="red")
        confirm_button.config(text="转换失败")
    confirm_button.after(1000, reset_color)
def reset_color():
    confirm_button.config(bg="white")
    confirm_button.config(text="点击转换")

def open_template():
    os.system("start notepad.exe "+template_path)


# 创建一个窗口
window = TkinterDnD.Tk()
window.title("Markdown转LaTeX")
window.resizable(False, False)
window.configure(background='white')

# 文件输入区
file_select_frame = tk.Frame(window, borderwidth=2,relief="solid")
file_select_frame.pack(padx=10, pady=10)

file_select_frame.drop_target_register(DND_FILES)
file_select_frame.dnd_bind('<<Drop>>', drop)


file_select_bottom = tk.Label(file_select_frame, text="将Markdown文件拖放至此处\n\n或\n\n点击选择文件", width=40,height=10,bg='lightgray',bd=2, cursor='hand2')
file_select_bottom.pack(padx=10, pady=10)
file_select_bottom.bind('<Button-1>', select_file_path)

file_path_entry = tk.Entry(file_select_frame,width=40,relief="solid")
with open(history_path, 'r', encoding='utf-8') as f:
    history = f.read()
    file_path_entry.insert(0, history)
file_path_entry.pack(padx=10, pady=10)

# 交互区
interaction_frame = tk.Frame(window, bg="white")
interaction_frame.pack(padx=10, pady=10)
confirm_button = tk.Button(interaction_frame, text="点击转换",width=20,height=2 ,bg= "white" ,relief="solid", command=perform_task)
confirm_button.pack(pady=20,padx=10,side="left")

template_button = tk.Button(interaction_frame, text="打开模板",width=10,height=2 ,bg= "white" ,relief="solid", command=open_template)
template_button.pack(pady=20,padx=10,side="right")

window.mainloop()
