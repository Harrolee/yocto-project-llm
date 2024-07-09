import jsonlines
import os

def rm_license(line):
    return line.replace('.. SPDX-License-Identifier: CC-BY-SA-2.0-UK', '')

def extract_header(lines):
    header_lines = []
    for line in lines:
        if line.startswith('****'):
            break
        header_lines.append(line)
    return ''.join(header_lines)

def process_rst_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
        
        header = rm_license(extract_header(lines))

        entries = []
        is_first = True
        for i in range(0, len(lines), 100):
            entry_text = '\n'.join(lines[i:i+100])
            if not is_first:
                entry_text = header + '\n' + entry_text
            entry = {'text': rm_license(entry_text)}
            entries.append(entry)
            is_first = False
    return entries

def create_jsonl_from_rst_directory(directory_path, output_path):
    with jsonlines.open(output_path, 'w') as writer:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                if file_name.endswith('.rst'):
                    file_path = os.path.join(root, file_name)
                    entries = process_rst_file(file_path)
                    writer.write_all(entries)

target_dir = "/Users/lee/yocto-llm/yocto-docs/documentation/dev-manual"
create_jsonl_from_rst_directory(target_dir, 'dev-manual-nonl.jsonl')
