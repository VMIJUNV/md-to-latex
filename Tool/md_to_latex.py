import mistune
import yaml
import sys
from LaTeXRenderer import LaTeXRender
from mistune.plugins.math import math
from mistune.plugins.table import table
from pathlib import Path

path = Path(sys.path[0])

default_convert_template_path = path / "default_convert_template.txt"
default_convert_config_path = path / "default_convert_config.yaml"

def convert(md_path,customer_convert_template_path,customer_convert_config_path,output_path):
    md_path = Path(md_path)
    customer_convert_template_path = Path(customer_convert_template_path)
    customer_convert_config_path = Path(customer_convert_config_path)
    output_path  = Path(output_path)
    with open(md_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    with open(default_convert_template_path, 'r', encoding='utf-8') as f:
        default_convert_template = f.read()
    with open(default_convert_config_path, 'r') as f:
        default_convert_config = yaml.load(f, Loader=yaml.FullLoader)

    if customer_convert_template_path.exists():
        with open(customer_convert_template_path, 'r', encoding='utf-8') as f:
            customer_convert_template = f.read()
        template=customer_convert_template 
    else:
        template = default_convert_template

    if customer_convert_config_path.exists():
        with open(customer_convert_config_path, 'r') as f:
            customer_convert_config = yaml.load(f, Loader=yaml.FullLoader)
        # config = default_convert_config | customer_convert_config
        config = {**default_convert_config, **customer_convert_config}
    else:
        config = default_convert_config

    render=LaTeXRender(my_config=config)

    markdown = mistune.create_markdown(renderer=render,plugins=[math,table])

    latex=markdown(markdown_text)

    latex=template.replace("<!-- Insert -->",latex)

    with open(output_path,'w', encoding='utf-8') as f:
        f.write(latex)


if __name__=="__main__":
    md_file_path = path.parent / "Paper" /"markdown"/ "test.md"
    file_dir = md_file_path.parent
    customer_convert_template_path = file_dir / "customer_convert_template.txt"
    customer_convert_config_path = file_dir / "customer_convert_config.yaml"
    output_path = file_dir / ".." / "latex" / "test.tex"
    convert(md_path=md_file_path,
            customer_convert_template_path=customer_convert_template_path,
            customer_convert_config_path=customer_convert_config_path,
            output_path=output_path)

