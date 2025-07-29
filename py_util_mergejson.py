'''
title: 文本处理工具 - 合并json文件
level: 2
competition:
    - 文件处理
    - 合并json文件
import:
    - os
    - re
    - glob
    - mmap
'''
import json
import os
import glob
from pathlib import Path
from typing import List, Dict, Any

class JSONMerger:
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding

    def merge_files(self, file_paths: List[str], output_file: str) -> Dict[str, Any]:
        """
        合并多个JSON文件
        
        Args:
            file_paths: JSON文件路径列表
            output_file: 输出文件路径
            
        Returns:
            包含处理结果的字典
        """
        merged_data = []
        total_items = 0
        processed_files = 0
        error_files = []

        print("开始合并JSON文件...")

        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding=self.encoding) as file:
                    data = json.load(file)

                if isinstance(data, list):
                    merged_data.extend(data)
                    items_count = len(data)
                    total_items += items_count
                    processed_files += 1
                    print(f"✓ 已处理 {file_path}: {items_count} 条记录")
                else:
                    print(f"⚠ 警告: {file_path} 不是数组格式")
                    error_files.append(file_path)
            except json.JSONDecodeError as e:
                print(f"✗ 错误: 无法解析 {file_path}: {e}")
                error_files.append(file_path)
            except FileNotFoundError:
                print(f"✗ 错误: 文件不存在 {file_path}")
                error_files.append(file_path)
            except Exception as e:
                print(f"✗ 错误: 处理 {file_path} 时出错: {e}")
                error_files.append(file_path)

        # 保存合并后的数据
        success = self._save_merged_data(merged_data, output_file)
        
        result = {
            'success': success,
            'total_items': total_items,
            'processed_files': processed_files,
            'error_files': error_files,
            'output_file': output_file
        }
        
        if success:
            result['file_size_mb'] = os.path.getsize(output_file) / (1024*1024)
            print(f"\n✓ 合并完成!")
            print(f"总共合并了 {total_items} 条记录")
            print(f"输出文件: {output_file}")
            print(f"文件大小: {result['file_size_mb']:.2f} MB")
        else:
            print(f"\n✗ 合并失败!")
        
        return result
        
    def _save_merged_data(self, data: List[Dict], output_file: str) -> bool:
        """保存合并后的数据"""
        try:
            with open(output_file, 'w', encoding=self.encoding) as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"✗ 错误: 保存合并后的数据时出错: {e}")
            return False

def merge_json_from_directories(
    directories: List[str], 
    file_pattern: str = "matweb_materials_1.json",
    output_file: str = "merged_materials.json",
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    从指定目录合并JSON文件
    
    Args:
        directories: 目录列表
        file_pattern: 文件名模式
        output_file: 输出文件名
        encoding: 文件编码
        
    Returns:
        处理结果字典
    """
    merger = JSONMerger(encoding)
    
    # 构建文件路径列表
    file_paths = []
    for directory in directories:
        if '*' in file_pattern or '?' in file_pattern:
            # 使用glob模式匹配
            pattern = os.path.join(directory, file_pattern)
            matched_files = glob.glob(pattern)
            file_paths.extend(matched_files)
            if not matched_files:
                print(f"⚠ 跳过: 在 {directory} 中没有找到匹配 {file_pattern} 的文件")
        else:
            # 直接文件路径
            file_path = os.path.join(directory, file_pattern)
            if os.path.exists(file_path):
                file_paths.append(file_path)
            else:
                print(f"⚠ 跳过: {file_path} 不存在")

    if not file_paths:
        print("✗ 错误: 没有找到任何文件")
        return {
            'success': False,
            'total_items': 0,
            'processed_files': 0,
            'error_files': []
        }

    return merger.merge_files(file_paths, output_file)

if __name__ == "__main__":
    # 默认配置
    directories = [
        "3M1-100", "3M101-200", "3M201-300", "3M301-400", "3M401-500",
        "3M501-600", "3M601-700", "3M701-800", "3M801-900", "3M901-1000"
    ]
    
    result = merge_json_from_directories(
        directories=directories,
        file_pattern="matweb_materials_1.json",
        output_file="merged_3m_materials.json",
        encoding="utf-8"
    )
    
    # 输出结果摘要
    print(f"\n=== 处理摘要 ===")
    print(f"成功: {'是' if result['success'] else '否'}")
    print(f"处理文件数: {result['processed_files']}")
    print(f"总记录数: {result['total_items']}")
    print(f"错误文件数: {len(result['error_files'])}")