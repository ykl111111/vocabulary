import os
import json
import textwrap

INPUT_DIR = "data"      # 存放 JSON 文件的目录
OUTPUT_DIR = "html"    # 生成 HTML 文件的目录

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_html(data):
    """
    根据单个 JSON 对象 data，生成带缩进的 HTML 字符串。
    """
    word = data.get("word", "")
    phon = data.get("phonetics", {})
    definitions = data.get("definitions", [])
    phrases = data.get("phrases", [])
    examples = data.get("examples", [])

    # HTML 头部
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '  <head>',
        '    <meta charset="UTF-8">',
        f'    <title>{word}</title>',
        '    <style>',
        '      body {',
        '        font-family: Arial, sans-serif;',
        '        margin: 40px;',
        '        line-height: 1.6;',
        '      }',
        '      h1 { color: #2c3e50; }',
        '      .section { margin-bottom: 30px; }',
        '      .gray { color: gray; }',
        '    </style>',
        '  </head>',
        '  <body>',
        f'    <h1>{word}</h1>',
    ]

    # 发音部分
    html_lines += [
        '    <div class="section phonetics">',
        f'      <strong>British:</strong> {phon.get("british", "")}<br>',
        f'      <strong>American:</strong> {phon.get("american", "")}',
        '    </div>',
    ]

    # 定义部分
    html_lines.append('    <div class="section definitions">')
    html_lines.append('      <h2>Definitions</h2>')
    for d in definitions:
        block = [
            '      <p>',
            f'        <strong>{d.get("partOfSpeech", "")}:</strong> {d.get("definition", "")}<br>',
            f'        <span class="gray">{d.get("chineseTranslation", "")}</span><br>',
            f'        <span class="gray">Level: {d.get("level", "")} | Frequency: {d.get("frequency", "")} | Register: {d.get("register", "")}</span>',
            '      </p>',
        ]
        html_lines += block
    html_lines.append('    </div>')

    # 短语部分
    if phrases:
        html_lines.append('    <div class="section phrases">')
        html_lines.append('      <h2>Phrases</h2>')
        for p in phrases:
            block = [
                '      <p>',
                f'        <strong>{p.get("phrase", "")}:</strong> {p.get("meaning", "")}<br>',
                f'        <i>{p.get("example", "")}</i><br>',
                f'        <span class="gray">{p.get("exampleTranslation", "")}</span>',
                '      </p>',
            ]
            html_lines += block
        html_lines.append('    </div>')

    # 例句部分
    if examples:
        html_lines.append('    <div class="section examples">')
        html_lines.append('      <h2>Examples</h2>')
        for e in examples:
            block = [
                '      <p>',
                f'        {e.get("sentence", "")}<br>',
                f'        <span class="gray">{e.get("translation", "")}</span>',
                '      </p>',
            ]
            html_lines += block
        html_lines.append('    </div>')

    # HTML 尾部
    html_lines += [
        '  </body>',
        '</html>',
    ]

    # 将列表形式的行合并为一个字符串，行与行之间自动加换行符
    return "\n".join(html_lines)

def batch_generate(input_dir, output_dir):
    """
    批量读取 input_dir 下所有 .json 文件，生成对应的 .html 文件到 output_dir。
    """
    for filename in os.listdir(input_dir):
        if not filename.endswith(".json"):
            continue

        json_path = os.path.join(input_dir, filename)
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ 读取或解析失败: {filename} → {e}")
            continue

        html_content = generate_html(data)
        base_name = os.path.splitext(filename)[0]
        html_path = os.path.join(output_dir, f"{base_name}.html")

        try:
            with open(html_path, "w", encoding="utf-8") as out_file:
                out_file.write(html_content)
            print(f"✅ 已生成: {html_path}")
        except Exception as e:
            print(f"❌ 写入失败: {html_path} → {e}")

if __name__ == "__main__":
    batch_generate(INPUT_DIR, OUTPUT_DIR)
