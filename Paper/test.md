# 介绍

Word和LaTeX是论文写作常用的排版软件，二者各有优缺点，没有优劣之分。但是笔者作为一名理科生，更偏向于用LaTeX来排版，首先LaTeX对数学公式的支持更完善，排版的效果优美，其次是LaTeX分离了内容与形式，排版逻辑清晰，最后LaTeX是以文本形式保存的，文章的管理和编辑轻便。

但是LaTeX的语法复杂，编译卡顿，源代码的阅读性也不好，直接使用LaTeX来写文章并不是一个舒服的选择。与此同时Markdown作为一种标记语言，语法简单、易于学习、轻量简洁，更容易让作者专注于内容的创作，所以笔者认为前期使用Markdown创作内容，后期使用LaTeX调整格式是一个不错的选择。

目前可以使用软件pandoc将Markdown转化为LaTeX，笔者我认为这个方法实现的效果不够优雅，功能也比较少。

为此笔者亲自设计了一个转换方案，这套方案有以下优点和特点:
1.  **模板化:** 通过预定义的模板，用户可以提前设定文章的格式，使得Markdown文本可以专注于内容创作，而无需担心格式问题。
2.  **图表引用:** 在Markdwon中可以利用链接快捷方便的调用图片和表格文件，本方案会自动处理这些文件，并将其转化为LaTeX格式。
3.  **嵌入LaTeX源码:** 支持在Markdown中嵌入LaTeX代码，这让本方案有了极大的灵活性，实现论文引用、交叉引用等复杂的排版功能。
4.  **定制化:** 本项目的设计考虑到了用户可能的不同需求，部分功能可以根据用户的实际需求进行简单的代码修改，以实现更多定制化功能。
5.  **简洁优雅:** 本项目生成的LaTeX代码简洁优雅，易于阅读和维护。

# 演示

## 段落标题列表

演示文本**演示文本**演示文本*example*演示文本

-   无序列表
-   无序列表
    1.  有序列表1
    2.  有序列表2

## 公式

行内公式: $\mathrm{e}^{x}=1+x+\frac{x^{2}}{2 !}+\cdots+\frac{x^{n}}{n !}+o\left(x^{n}\right)$。

行间公式:
$$
f(x)=f\left(x_{0}\right)+f^{\prime}\left(x_{0}\right)\left(x-x_{0}\right)+\frac{f^{\prime \prime}\left(x_{0}\right)}{2 !}\left(x-x_{0}\right)^{2}+\cdots
$$



## 图表
### 图片
![图](/Data/测试图1.jpeg "图片测试1")

[图](/Data/测试图2.jpg "图片测试2")

### 表格

|第一列|第二列|第三列|第四列|第五列|
|:---:|:---:|:---:|:---:|:---:|
|1|2|3|4|5|

[表](/Data/测试表.csv "表格测试")


## 嵌入Latex代码

引用图`\ref{图片测试1}`。

引用论文`\cite{lu_deepxde_2021}`。

自动生成参考文献。
~~~
\newpage
\bibliographystyle{plain}
\bibliography{\rootpath/Data/docu.bib}
~~~
