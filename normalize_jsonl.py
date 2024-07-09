import jsonlines
import re

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def process_jsonl_file(input_path, output_path):
    with jsonlines.open(input_path, 'r') as reader, jsonlines.open(output_path, 'w') as writer:
        for entry in reader:
            text = entry['text']
            words = count_words(text)

            if words > 200:
                header_match = re.search(r'{"text": "(.+?)\n', text)
                header = header_match.group(1) if header_match else ''

                parts = text.split('\n')[1:]

                start_index = 0
                while start_index < len(parts):
                    end_index = min(start_index + 200, len(parts))
                    # entry_text = f'{header}\n{"\n".join(parts[start_index:end_index])}'
                    entry_text = header + '\n' + '\n'.join(parts[start_index:end_index])

                    writer.write({'text': entry_text})
                    start_index = end_index

            else:
                writer.write(entry)

# Replace 'input.jsonl' and 'output.jsonl' with your actual input and output file names
process_jsonl_file('input.jsonl', 'output.jsonl')
