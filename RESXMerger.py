import xml.etree.ElementTree as ET
import json

def parse_resx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {data.attrib['name']: data.find('value').text for data in root.findall('data')}

def merge_translations(ja_dict, en_dict):
    merged = {}
    unmatched = {'ja': {}, 'en': {}}
    
    for key in ja_dict:
        if key in en_dict:
            if ja_dict[key] == en_dict[key]:
                merged[key] = ja_dict[key]
            else:
                merged[key] = f"{ja_dict[key]} {en_dict[key]}"
        else:
            unmatched['ja'][key] = ja_dict[key]
    
    for key in en_dict:
        if key not in ja_dict:
            unmatched['en'][key] = en_dict[key]
    
    return merged, unmatched

def create_merged_resx(merged_dict, output_file):
    root = ET.Element('root')
    for key, value in merged_dict.items():
        data = ET.SubElement(root, 'data', name=key, attrib={'xml:space': 'preserve'})
        value_elem = ET.SubElement(data, 'value')
        value_elem.text = value
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def preview_results(merged_dict, limit=5):
    print("プレビュー（最初の5件）:")
    for i, (key, value) in enumerate(list(merged_dict.items())[:limit]):
        print(f"  <data name=\"{key}\" xml:space=\"preserve\">")
        print(f"    <value>{value}</value>")
        print("  </data>")
    print(f"... 他 {len(merged_dict) - limit} 件")

def write_unmatched_log(unmatched, log_file):
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(unmatched, f, ensure_ascii=False, indent=2)

def main(ja_file, en_file, output_file, log_file):
    ja_dict = parse_resx(ja_file)
    en_dict = parse_resx(en_file)
    
    merged_dict, unmatched = merge_translations(ja_dict, en_dict)
    create_merged_resx(merged_dict, output_file)
    write_unmatched_log(unmatched, log_file)
    
    preview_results(merged_dict)
    
    print("\n未マッチの項目:")
    print(f"日本語ファイルのみ: {len(unmatched['ja'])} 件")
    print(f"英語ファイルのみ: {len(unmatched['en'])} 件")
    print(f"未マッチの項目の詳細は {log_file} に出力されました。")

if __name__ == "__main__":
    ja_file = input("日本語のresxファイルパスを入力してください: ")
    en_file = input("英語のresxファイルパスを入力してください: ")
    output_file = input("出力ファイルのパスを入力してください: ")
    log_file = input("ログファイルのパスを入力してください: ")
    
    main(ja_file, en_file, output_file, log_file)