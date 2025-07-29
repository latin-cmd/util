'''
title: 文本处理工具 - 添加/删除/替换文本
level: 2
competition:
    - 文件处理
    - 文本操作
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
from typing import List, Optional, Union

class TextProcessor:
    """文本处理工具类"""
    
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding
    
    def add_text_simple(self, file_path: str, text: str, position: str = "end") -> bool:
        """
        简单文本添加方法
        
        Args:
            file_path: 文件路径
            text: 要添加的文本
            position: 添加位置 ("start", "end", "before_line", "after_line")
        """
        try:
            with open(file_path, "r", encoding=self.encoding) as file:
                content = file.read()
            
            if position == "start":
                new_content = text + content
            elif position == "end":
                new_content = content + text
            elif position == "before_line":
                lines = content.split('\n')
                new_content = text + '\n' + content
            elif position == "after_line":
                lines = content.split('\n')
                new_content = content + '\n' + text
            else:
                print(f"错误：不支持的位置参数 {position}")
                return False
            
            if new_content == content:
                print(f"添加失败：内容未发生变化")
                return False
            
            with open(file_path, "w", encoding=self.encoding) as file:
                file.write(new_content)
            
            print(f"成功添加文本到文件：{file_path}")
            return True
            
        except Exception as e:
            print(f"添加文本时出错: {e}")
            return False
    
    def add_text_mmap(self, file_path: str, text: str, position: str = "end") -> bool:
        """
        使用内存映射的文本添加方法（适用于大文件）
        """
        try:
            with open(file_path, "r", encoding=self.encoding) as file:
                with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as m:
                    content = m.read().decode(self.encoding)
            
            # 使用与简单方法相同的逻辑
            return self.add_text_simple(file_path, text, position)
            
        except Exception as e:
            print(f"内存映射添加文本时出错: {e}")
            return False
    
    def remove_text(self, file_path: str, text: str, use_regex: bool = False) -> bool:
        """
        删除文本方法
        
        Args:
            file_path: 文件路径
            text: 要删除的文本
            use_regex: 是否使用正则表达式
        """
        try:
            with open(file_path, "r", encoding=self.encoding) as file:
                content = file.read()
            
            if use_regex:
                pattern = text  # 直接使用正则表达式
            else:
                pattern = re.escape(text)  # 转义特殊字符
            
            new_content = re.sub(pattern, '', content)
            
            if new_content == content:
                print(f"删除失败：未找到匹配的文本")
                return False
            
            with open(file_path, "w", encoding=self.encoding) as file:
                file.write(new_content)
            
            print(f"成功删除文本：{file_path}")
            return True
            
        except Exception as e:
            print(f"删除文本时出错: {e}")
            return False
    
    def replace_text(self, file_path: str, old_text: str, new_text: str, use_regex: bool = False) -> bool:
        """
        替换文本方法
        """
        try:
            with open(file_path, "r", encoding=self.encoding) as file:
                content = file.read()
            
            if use_regex:
                pattern = old_text
            else:
                pattern = re.escape(old_text)
            
            new_content = re.sub(pattern, new_text, content)
            
            if new_content == content:
                print(f"替换失败：未找到匹配的文本")
                return False
            
            with open(file_path, "w", encoding=self.encoding) as file:
                file.write(new_content)
            
            print(f"成功替换文本：{file_path}")
            return True
            
        except Exception as e:
            print(f"替换文本时出错: {e}")
            return False

def process_files(
    directories: List[str],
    file_type: str,
    operation: str,
    text: str,
    encoding: str = "utf-8",
    exclude_files: Optional[List[str]] = None,
    method: str = "simple",
    **kwargs
) -> int:
    """
    批量处理文件
    
    Args:
        directories: 要搜索的目录列表
        file_type: 文件类型（如 "txt", "py"）
        operation: 操作类型 ("add", "remove", "replace")
        text: 要处理的文本
        encoding: 文件编码
        exclude_files: 要排除的文件名列表
        method: 处理方法 ("simple", "mmap")
        **kwargs: 其他参数（如 new_text, position, use_regex 等）
    """
    processor = TextProcessor(encoding)
    modified_count = 0
    
    try:
        for directory in directories:
            pattern = os.path.join(directory, f'*.{file_type}')
            files = glob.glob(pattern)
            
            print(f"在目录 {directory} 中找到 {len(files)} 个 {file_type} 文件")
            
            for file_path in files:
                # 检查是否在排除列表中
                if exclude_files:
                    file_name = os.path.basename(file_path)
                    if any(exclude in file_name for exclude in exclude_files):
                        continue
                
                success = False
                
                if operation == "add":
                    position = kwargs.get("position", "end")
                    if method == "simple":
                        success = processor.add_text_simple(file_path, text, position)
                    elif method == "mmap":
                        success = processor.add_text_mmap(file_path, text, position)
                
                elif operation == "remove":
                    use_regex = kwargs.get("use_regex", False)
                    success = processor.remove_text(file_path, text, use_regex)
                
                elif operation == "replace":
                    new_text = kwargs.get("new_text", "")
                    use_regex = kwargs.get("use_regex", False)
                    success = processor.replace_text(file_path, text, new_text, use_regex)
                
                if success:
                    modified_count += 1
        
        print(f"总共处理了 {modified_count} 个文件")
        return modified_count
        
    except Exception as e:
        print(f"批量处理文件时出错: {e}")
        return 0

if __name__ == "__main__":
    # 示例用法
    directories = ["."]
    file_type = "txt"
    operation = "remove"  # "add", "remove", "replace"
    text = 1
    encoding = "utf-8"
    exclude_files = ["Readme.md"]
    method = "simple"  # "simple", "mmap"
    
    # 添加文本到文件末尾
    process_files(
        directories=directories,
        file_type=file_type,
        operation=operation,
        text=text,
        encoding=encoding,
        exclude_files=exclude_files,
        method=method,
        position="end"
    ) 