import os
import xml.etree.ElementTree as ET
import re

def read_and_process_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    xml_content = f'<root>{file_content}</root>'
    root = ET.fromstring(xml_content)

    text_lines = []
    for textline in root.findall(".//node[@type='RIL_TEXTLINE']"):
        words = []
        for word in textline.findall(".//node[@type='RIL_WORD']"):
            if word.text:
                cleaned_text = re.sub(r'[\d.,:;!?()\"\'-]', '', word.text)
                cleaned_text = ' '.join(cleaned_text.split())
                words.append(cleaned_text)
        line = ' '.join(words).strip()
        if line: 
            text_lines.append(line)

    return "\n".join(text_lines)

def process_and_copy_files(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(root, source_dir)
        target_root = os.path.join(target_dir, rel_path)
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                processed_text = read_and_process_xml(file_path)
                target_file_path = os.path.join(target_root, os.path.splitext(file)[0] + '.txt')
                with open(target_file_path, 'w', encoding='utf-8') as f:
                    f.write(processed_text)

source_directory = 'data'
target_directory = 'txt_data'

process_and_copy_files(source_directory, target_directory)
