import jsonlines
import os
import re

def rm_license(line):
    return line.replace('.. SPDX-License-Identifier: CC-BY-SA-2.0-UK', '')

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def extract_header(lines):
    header_lines = []
    for line in lines:
        if (line.startswith('****') or
                (line.startswith('*') and len(set(line.strip())) == 1 and len(line.strip()) > 10)):
            break
        header_lines.append(line)
    return ''.join(header_lines)

def is_special_header(line):
    return line.startswith('*') and len(set(line.strip())) == 1 and len(line.strip()) > 10

def process_rst_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        header = extract_header(lines)
        print(len(lines))

        text = ''.join(lines)
        word_count = count_words(text)
        print(f"Total words: {word_count}")

        entries = []
        words_per_entry = 200
        start_index = 0
        while start_index < word_count:
            end_index = min(start_index + words_per_entry, word_count)

            # Ensure that the header is prepended to the entry
            entry_text = text.split()[start_index:end_index]
            if is_special_header(entry_text[0]):
                header_end = entry_text.index('EMUlator (QEMU)') + 1
                entry_text = entry_text[:header_end]
            
            entry = {'text': header + rm_license(' '.join(entry_text))}
            entries.append(entry)
            start_index = end_index

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
create_jsonl_from_rst_directory(target_dir, 'dev-manual-all-latestest.jsonl')
