'''
title: 删除特定文件特定文本
level: 2
competition:
    - 文件处理
    - 删除特定文本
import:
    - os
    - re
    - glob
    - mmap
'''

import os
import re
import glob
import mmap

def remove_test_small(input_file_path, input_test, input_encoding="utf-8"):

    try:
        with open(input_file_path, "r", encoding=input_encoding) as file:
            content = file.read();

        # pattern = re.escape(test)

        # new_content = re.sub(pattern, '', content)

        new_content = content.replace(input_test, '')

        if new_content == content:
            print(f"删除脚本栈-第一层-未找到{input_test}文本")
            return False
        else:
            with open(input_file_path, "w", encoding=input_encoding) as file:
                file.write(new_content)
            print(f"删除脚本栈-第一层-成功删除{input_test}文本")
            return True

    except Exception as e:
        print(f"删除脚本栈-第一层-删除文本时出错: {e}")
        return False
        
def remove_test_mmap(input_file_path, input_test, input_encoding="utf-8"):

    try:
        with open(input_file_path, "r", encoding=input_encoding) as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as m:
                content = m.read().decode(input_encoding)

        pattern = re.escape(input_test)

        new_content = re.sub(pattern, '', content)

        # new_content = content.replace(input_test, '')

        if new_content == content:
            print(f"mmap-删除脚本栈-第一层-未找到{input_test}文本")
            return False
        else:
            with open(input_file_path, "w", encoding=input_encoding) as file:
                file.write(new_content)
            print(f"mmap-删除脚本栈-第一层-成功删除{input_test}文本")
            return True

    except Exception as e:
        print(f"mmap-删除脚本栈-第一层-删除文本时出错: {e}")
        return False

def search_test(input_list, input_type, input_test, input_encoding="utf-8", except_file=None, input_weight="small"):

    try:
        processed_count = 0
        modified_count = 0

        for lists in input_list:
            pattern = os.path.join(lists, f'*.{input_type}')

            files = glob.glob(pattern)

            print(f"搜索脚本栈-第二层-找到{len(files)}个{input_type}文件")

            for file in files:
                if except_file and except_file in file:
                    continue
                processed_count += 1
                if input_weight == "small":
                    if remove_test_small(file, input_test, input_encoding):
                        modified_count += 1
                elif input_weight == "mmap":
                    if remove_test_mmap(file, input_test, input_encoding):
                        modified_count += 1

        print(f"搜索脚本栈-第二层-处理了{modified_count}个文件")

        return modified_count

    except Exception as e:
        print(f"搜索脚本栈-第二层-搜索文本时出错: {e}")
        return False

if __name__ == "__main__":
    input_list = [ "." ]
    input_type = "txt"
    input_test = "test"
    input_encoding = "utf-8"
    except_file = "Readme.md"
    input_weight = "small"
    search_test(input_list, input_type, input_test, input_encoding, except_file, input_weight)