# 文本处理工具集

这是一个Python文本处理工具集，提供了JSON文件合并和文本操作功能。

## 🚀 功能特性

### 1. JSON文件合并工具 (`py_util_mergejson.py`)
- **批量合并JSON文件**：支持从多个目录合并JSON文件
- **灵活的文件匹配**：支持通配符模式匹配文件
- **数据验证**：自动验证JSON格式并处理错误
- **进度显示**：实时显示处理进度和结果统计

### 2. 文本处理工具 (`py_util_test.py`)
- **文本添加**：向文件添加文本内容（支持文件开头、结尾、指定位置）
- **文本删除**：删除文件中的指定文本（支持正则表达式）
- **文本替换**：替换文件中的文本内容（支持正则表达式）
- **批量处理**：支持批量处理指定目录下的文件
- **大文件支持**：使用内存映射处理大文件

## 📁 项目结构

```
sed/
├── py_util_mergejson.py    # JSON文件合并工具
├── py_util_test.py         # 文本处理工具
├── backup_py.md           # 备份文档
└── README.md              # 项目说明文档
```

## 🛠️ 使用方法

### JSON文件合并

```python
from py_util_mergejson import merge_json_from_directories

# 合并指定目录的JSON文件
result = merge_json_from_directories(
    directories=["dir1", "dir2", "dir3"],
    file_pattern="*.json",
    output_file="merged_output.json",
    encoding="utf-8"
)
```

#### 命令行使用
```bash
python py_util_mergejson.py
```

默认配置会合并以下目录的 `matweb_materials_1.json` 文件：
- 3M1-100, 3M101-200, ..., 3M901-1000

### 文本处理

#### 基本用法
```python
from py_util_test import process_files

# 批量添加文本到txt文件
process_files(
    directories=["."],
    file_type="txt",
    operation="add",
    text="新添加的文本",
    position="end"
)

# 批量删除文本
process_files(
    directories=["."],
    file_type="py",
    operation="remove",
    text="要删除的文本",
    use_regex=False
)

# 批量替换文本
process_files(
    directories=["."],
    file_type="md",
    operation="replace",
    text="旧文本",
    new_text="新文本",
    use_regex=False
)
```

#### 高级选项
- **排除文件**：使用 `exclude_files` 参数排除特定文件
- **正则表达式**：设置 `use_regex=True` 使用正则表达式
- **内存映射**：设置 `method="mmap"` 处理大文件

## 📊 输出示例

### JSON合并结果
```
开始合并JSON文件...
✓ 已处理 data1.json: 150 条记录
✓ 已处理 data2.json: 200 条记录
✓ 已处理 data3.json: 175 条记录

✓ 合并完成!
总共合并了 525 条记录
输出文件: merged_output.json
文件大小: 2.35 MB
```

### 文本处理结果
```
在目录 . 中找到 5 个 txt 文件
成功添加文本到文件：file1.txt
成功添加文本到文件：file2.txt
成功添加文本到文件：file3.txt
总共处理了 3 个文件
```

## ⚙️ 技术特性

- **跨平台支持**：基于Python，支持Windows/Linux/macOS
- **编码支持**：默认UTF-8编码，可自定义
- **错误处理**：完善的异常处理和错误报告
- **进度反馈**：实时显示处理进度
- **灵活配置**：支持多种参数配置

## 🔧 依赖要求

- Python 3.6+
- 标准库（无需额外安装）

## 📝 注意事项

1. **文件备份**：建议在处理前备份重要文件
2. **编码问题**：确保文件编码与指定的编码参数一致
3. **正则表达式**：使用正则表达式时请注意转义特殊字符
4. **大文件处理**：对于超大文件建议使用内存映射模式

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具集。

## 📄 许可证

MIT License - 详见项目许可证文件。