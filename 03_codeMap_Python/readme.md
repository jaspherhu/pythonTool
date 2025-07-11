# 时代换电代码转换器 v20250302

## 功能概述

### 核心功能
1. **字符映射转换**
   - 支持大小写字母+数字的随机映射
   - 自动生成并保存映射配置文件
   - 映射表有效性验证
   - 字符级批量替换

2. **关键词替换**
   - CSV配置文件管理关键词映射
   - 正则表达式整词匹配替换
   - 自动生成唯一映射值
   - 冲突检测与自动修复

3. **恢复功能**
   - 支持字符映射反向恢复
   - 关键词映射反向恢复
   - 冲突提示与选择性覆盖

4. **附加功能**
   - 文件编码自动检测（支持UTF-8/GBK等）
   - 多线程处理
   - 操作日志记录
   - 实时进度显示
   - 深色/浅色主题自动适配

### 配置管理
- 可配置处理文件扩展名
- 可视化映射表管理
- 关键词增删改查界面
- 配置文件自动备份

## 使用步骤

### 基础操作流程
1. **选择目标文件夹**
   - 点击"浏览..."按钮选择需要处理的目录
   - 支持递归处理子目录

2. **设置文件过滤**
   - 在"文件扩展名"输入框指定处理类型（默认.c,.h）
   - 使用逗号分隔多个扩展名

3. **选择编码方式**
   - 通过下拉菜单选择文件编码（默认gb2312）
   - 支持自动编码检测

4. **执行转换操作**
   - 字符映射：点击"开始字符映射"
   - 关键词替换：点击"开始关键词转换"
   - 进度条实时显示处理进度

### 高级功能使用
**映射表管理**
1. 点击"映射表"按钮查看当前字符映射
2. 点击"刷新映射表"生成新映射关系
3. 恢复时自动使用反向映射表

**关键词管理**
1. 点击"关键词"打开管理窗口
2. 支持添加/删除/自动生成映射值
3. CSV配置文件自动保存路径：
   `脚本目录/keyword_config.csv`

**恢复操作**
1. 字符恢复：点击"恢复字符映射"
2. 关键词恢复：点击"恢复关键词"
3. 处理前自动检测映射冲突

## 注意事项
1. **配置文件路径**
   - 字符映射表：`mapping_config.json`
   - 反向映射表：`reverse_mapping.json`
   - 操作日志：`operation.log`

2. **安全机制**
   - 处理前自动备份冲突配置
   - 文件修改前进行编码验证
   - 异常处理自动跳过问题文件

3. **兼容性**
   - 支持Windows/macOS/Linux
   - 兼容Python 3.6+环境
   - 可打包为独立exe程序

## 版本信息
当前版本：20250302  
更新日期：2025年3月2日  
运行依赖：Python 3.6+ + Tkinter

## how to use this software
1. 安装依赖：`pip install -r requirements.txt`
2. 运行脚本：`python code-change-a09.py`
3. 按照提示操作即可

## how to run this software
1. 运行exe软件 
2. 设置对象代码的总的目录
3. 选择编码格式
4. 选择扩展名
5. 点击提取关键词
6. 点击查看关键词
7. 将关键词放到keyword_config.csv中
8. 再次打开exe软件
9. 点击查看关键词
10. 查看自动随机生成映射后的关键词
11. 点击开始转换

## how to build exe
pyinstaller --onefile --name codeFuse --icon=ysicons.ico code-change-a09.py