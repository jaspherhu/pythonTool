# -*- coding: utf-8 -*-

# 原文件内容
import os
import random
import json
import string  # 新增导入
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import threading
# 在文件顶部新增导入
import re
import csv  # 添加导入
import platform
import chardet
import shutil  # 确保在调用copyfile之前导入
import sys

# 新增配置路径常量
MAPPING_CONFIG_PATH = 'mapping_config.json'
VERSION = "20250302"
# 新增全局常量：关键字最小长度
MIN_KEYWORD_LENGTH = 4


def get_script_dir():
    """获取脚本所在目录的绝对路径"""
    if getattr(sys, 'frozen', False):  # 打包成exe的情况
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
    

def generate_fixed_mapping():
    """生成随机字母数字映射表并保存到文件"""
    # 包含所有大写字母、小写字母和数字
    chars = list(
        string.ascii_uppercase +  # A-Z (26)
        string.ascii_lowercase +  # a-z (26)
        string.digits             # 0-9 (10)
    )
    
    # 创建打乱后的目标字符列表
    shuffled = chars.copy()
    random.shuffle(shuffled)
    
    # 生成映射关系
    mapping = {orig: tgt for orig, tgt in zip(chars, shuffled)}
    return mapping, {v:k for k,v in mapping.items()}

def load_or_create_mapping():
    """从配置文件加载或创建新映射表"""
    MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')

    if os.path.exists(MAPPING_CONFIG_PATH):
        try:
            with open(MAPPING_CONFIG_PATH, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
                if validate_mapping(mapping):
                    return mapping, {v:k for k,v in mapping.items()}
                else:
                    messagebox.showwarning("配置问题", "映射表校验失败，已创建新表")
        except Exception as e:
            messagebox.showwarning("配置错误", f"配置文件加载失败：{str(e)}\n已创建新映射表")
    else:
        # 首次运行时不显示警告
        pass
    
    # 创建新映射表
    mapping, reverse_mapping = generate_fixed_mapping()
    MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')
    save_reverse_mapping(mapping, MAPPING_CONFIG_PATH)
    return mapping, reverse_mapping

def validate_mapping(mapping):
    """验证映射表有效性"""
    required_chars = set(
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits
    )
    return (
        len(mapping) == 62 and
        set(mapping.keys()) == required_chars and
        len(set(mapping.values())) == 62
    )

def save_reverse_mapping(mapping, filename):
    try:
        reverse_mapping = {}
        # 修改日志提示方式（移除self引用）
        conflict_log = []
        for k, v in mapping.items():
            if v in reverse_mapping:
                conflict_log.append(f"冲突警告：{v} 已被 {reverse_mapping[v]} 映射")
            reverse_mapping[v] = k
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reverse_mapping, f, ensure_ascii=False, indent=2)
            
        return conflict_log  # 返回冲突日志供调用者处理
    except Exception as e:
        raise RuntimeError(f"保存映射表失败：{str(e)}")
    
# ... [保留原有固定映射表和替换函数代码] ...
# 新增随机字符串生成函数（放在Application类外）
def generate_random_mapped(length=8):
    """生成指定长度的随机字母数字组合"""
    # chars = string.ascii_letters + string.digits
    chars = string.ascii_letters  # 仅包含大小写字母
    return ''.join(random.choice(chars) for _ in range(length))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # 必须首先初始化父类

        # 可以在文件顶部添加版本常量
        self.title(f"时代换电代码转换器 - v{VERSION}")  # 动态版本号

        # 样式配置
        self.style = ttk.Style()

        if platform.system() == 'Windows':
            self.style.theme_use('vista')  # Windows系统使用vista主题
        else:
            self.style.theme_use('clam')   # 其他系统使用clam主题

        
        # 深色系配色方案（提高可读性）
        self.style.configure("Primary.TButton", 
                            foreground="green",
                            background="#2c3e50",  # 深蓝灰
                            font=('微软雅黑', 10, 'bold'))
        
        self.style.configure("Warning.TButton", 
                            foreground="red",
                            background="#c0392b",  # 深红色
                            font=('微软雅黑', 10, 'bold'))
        
        self.style.configure("Success.TButton",
                            foreground="green",
                            background="#27ae60",  # 深绿色
                            font=('微软雅黑', 10, 'bold'))
        
        self.style.configure("Info.TButton",
                            foreground="red",
                            background="#2980b9",  # 深蓝色
                            font=('微软雅黑', 10, 'bold'))
        
        # 通用按钮样式（用于非主要操作）
        self.style.configure("TButton",
                            foreground="#2c3e50",
                            background="#ecf0f1",
                            font=('微软雅黑', 9))
        
        # 先初始化配置路径
        self.keyword_config_path = os.path.join(get_script_dir(), 'keyword_config.csv')
        
        # 先尝试加载现有配置
        self.keywords = self._load_existing_config()
        
        # 空配置保护（仅在首次运行时创建默认）
        if not self.keywords and not os.path.exists(self.keyword_config_path):
            self._create_default_keyword_config()
        else:
            # 当配置文件存在但加载失败时保留原文件
            pass

        # 初始化其他组件
        sorted_keywords = sorted(self.keywords.keys(), key=len, reverse=True)
        self.keyword_pattern = re.compile(
            r'(?<!\w)(' + '|'.join(map(re.escape, sorted_keywords)) + r')(?!\w)',
            flags=re.UNICODE
        )

        # 其余初始化代码保持不变...
        self.encoding_var = tk.StringVar(value='gb2312')
        self.encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin1']
        
        # 初始化应用状态
        self.selected_dir = ""
        # self.mapping, _ = generate_fixed_mapping()
        self.filter_extensions = ['.c', '.h', '.cpp', '.hpp', '.make', '.ini']
        self.log_counter = 0

        # 配置文件与脚本同目录
        MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')
        # 修改初始化映射表的方式
        self.mapping, self.reverse_mapping = load_or_create_mapping()
        
        # 配置界面
        self._setup_main_frame()
        self.create_widgets()
        self.setup_logging()

    def extract_and_save_keywords(self):
        """提取关键字并保存到CSV文件"""
        if not self._validate_directory():
            return

        self.log_message("开始提取关键字...")
        try:
            # 通过实例调用静态方法
            keywords = self.extract_keywords_from_folder(self.selected_dir)
            keyword_csv_path = os.path.join(get_script_dir(), 'keywords_extracted.csv')
            self.save_keywords_to_csv(keywords, keyword_csv_path)
            
            self.keywords.update({kw: "" for kw in keywords})
            self._refresh_keyword_list()
            messagebox.showinfo("完成", f"共提取 {len(keywords)} 个关键字")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _load_existing_config(self):
        """安全加载现有配置文件（自动补全空映射值）"""
        if os.path.exists(self.keyword_config_path):
            try:
                with open(self.keyword_config_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    if reader.fieldnames != ["Original", "Mapped"]:
                        raise ValueError("CSV文件格式错误")
                    
                    keywords = {}
                    existing_values = set()
                    
                    for row in reader:
                        original = row['Original'].strip()
                        mapped = row['Mapped'].strip()
                        
                        if not original:
                            continue  # 跳过原始词为空的行
                            
                        # 自动生成映射值逻辑
                        if not mapped:
                            # 生成唯一随机值
                            while True:
                                mapped = generate_random_mapped()
                                if mapped not in existing_values:
                                    break
                            # 记录自动生成日志
                            self.log_message(f"自动生成映射：{original} → {mapped}")
                            
                        # 冲突检测（保留最后出现的映射关系）
                        if mapped in existing_values:
                            self.log_message(f"映射冲突：{mapped} 已存在，将覆盖")
                            
                        keywords[original] = mapped
                        existing_values.add(mapped)
                    
                    return keywords
                    
            except Exception as e:
                error_backup = f"{self.keyword_config_path}.error"
                shutil.copyfile(self.keyword_config_path, error_backup)
                messagebox.showerror("配置错误", f"配置已备份至：{error_backup}\n错误：{str(e)}")
                return {}
        return {}

    def _load_keyword_config(self):
        keyword_map = {}
        if os.path.exists(self.keyword_config_path):
            try:
                with open(self.keyword_config_path, 'r', newline='', encoding='utf-8') as f:
                    # 验证CSV有效性
                    header = f.readline().strip().split(',')
                    if header != ["Original", "Mapped"]:
                        raise ValueError("CSV文件头不匹配")
                    
                    f.seek(0)
                    reader = csv.DictReader(f)
                    for row in reader:
                        keyword = row['Original'].strip()
                        mapped = row['Mapped'].strip()
                        if keyword and mapped:
                            keyword_map[keyword] = mapped
            except Exception as e:
                messagebox.showwarning("配置错误", f"CSV加载失败：{str(e)}")
                # 创建备份
                shutil.copyfile(self.keyword_config_path, f"{self.keyword_config_path}.bak")
        else:
            self._create_default_keyword_config()
        return keyword_map

    def _create_default_keyword_config(self):
        """仅在文件不存在时创建默认配置"""
        if os.path.exists(self.keyword_config_path):
            return
            
        default_pairs = [
            ('hufan', 'dady'),
            ('you', 'kitty'),
            ('usr', 'baby')
        ]
        
        try:
            with open(self.keyword_config_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Original", "Mapped"])
                for k, v in default_pairs:
                    writer.writerow([k, v])
            self.keywords = dict(default_pairs)
        except Exception as e:
            messagebox.showerror("初始化错误", f"创建默认配置失败：{str(e)}")

            
    def _setup_main_frame(self):
        self.geometry("680x450")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def _build_log_section(self, parent):
        """构建日志区域组件"""
        log_frame = ttk.LabelFrame(parent, text="操作日志")
        log_frame.grid(row=3, column=0, sticky='nsew', pady=5)
        
        # 配置日志区布局权重
        parent.rowconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 创建日志文本框
        self.log_text = tk.Text(log_frame, height=8, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # 滚动条
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def _refresh_keyword_list(self):
        """刷新关键词列表"""
        if not hasattr(self, 'kw_listbox') or self.kw_listbox is None:
            return  # 如果未初始化，直接返回

        self.kw_listbox.delete(0, tk.END)
        for kw, mapped in sorted(self.keywords.items()):
            self.kw_listbox.insert(tk.END, f"{kw} → {mapped}")  # 显示键值对
    
    def _add_keyword(self):
        """带映射值输入的增强版本"""
        new_kw = self.new_kw_entry.get().strip()
        if not new_kw:
            return
        
        if new_kw in self.keywords:
            messagebox.showwarning("重复添加", f"关键词 '{new_kw}' 已存在")
            return
        
        # 弹出映射值输入对话框
        mapped_value = tk.simpledialog.askstring(
            "映射值输入",
            f"请输入'{new_kw}'的映射值（留空自动生成）:",
            parent=self.keyword_win
        )
        
        # 用户取消输入或关闭对话框
        if mapped_value is None:  
            return
        
        # 自动生成逻辑
        if not mapped_value.strip():
            # 生成唯一随机值
            existing_values = set(self.keywords.values())
            while True:
                mapped_value = generate_random_mapped()
                if mapped_value not in existing_values:
                    break
        
        self.keywords[new_kw] = mapped_value
        self._refresh_keyword_list()
        self.new_kw_entry.delete(0, tk.END)
        
        # 自动滚动到新增条目
        last_index = self.kw_listbox.size() - 1
        self.kw_listbox.see(last_index)

    # 增强删除方法
    def _del_keyword(self):
        """删除选中关键词（处理键值对显示）"""
        selections = self.kw_listbox.curselection()
        if not selections:
            return
        
        # 收集所有要删除的关键词
        to_delete = set()
        for idx in reversed(selections):
            display_text = self.kw_listbox.get(idx)
            original = display_text.split(" → ")[0]
            to_delete.add(original)
        
        # 批量删除
        for kw in to_delete:
            if kw in self.keywords:
                del self.keywords[kw]
        
        self._refresh_keyword_list()

    def _save_keywords(self):
        """保存时执行完整性检查（扩展冲突检测）"""
        # 原始词冲突检查
        if len(self.keywords) != len(set(self.keywords.keys())):
            duplicates = [k for k,v in collections.Counter(self.keywords.keys()).items() if v>1]
            messagebox.showwarning("原始词冲突", f"发现重复原始词：{duplicates}")
            return
        
        """保存时执行完整性检查"""
        # 有效性检查
        invalid_entries = [
            k for k,v in self.keywords.items() 
            if not k.strip() or not v.strip()
        ]
        if invalid_entries:
            messagebox.showwarning("无效条目", f"发现空条目：{invalid_entries}")
            return

        # 冲突检查
        value_count = {}
        for k, v in self.keywords.items():
            value_count[v] = value_count.get(v, 0) + 1
        
        conflicts = [v for v, count in value_count.items() if count > 1]
        if conflicts:
            # 改为自动处理冲突
            for c in conflicts:
                new_value = generate_random_mapped()
                for k in [k for k,v in self.keywords.items() if v == c]:
                    self.keywords[k] = new_value
            self.log_message(f"自动修复冲突：{len(conflicts)}处")

        # 保存操作
        try:
            with open(self.keyword_config_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Original", "Mapped"])
                for k, v in sorted(self.keywords.items()):
                    writer.writerow([k, v])
            messagebox.showinfo("保存成功", "配置已更新")
        except Exception as e:
            messagebox.showerror("保存失败", str(e))
            
    def show_keywords(self):
        """显示关键词管理窗口"""
        self.keyword_win = tk.Toplevel(self)
        self.keyword_win.title("关键词管理")
        self.keyword_win.geometry("600x500")

        # 创建带滚动条的文本框
        text_frame = ttk.Frame(self.keyword_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加配置来源信息
        config_status = f"配置文件路径：{self.keyword_config_path}\n"
        config_status += "✅ 配置文件存在\n" if os.path.exists(self.keyword_config_path) else "⚠️ 配置文件不存在\n"
        text.insert(tk.END, config_status + "\n")

        """增强的配置展示界面"""
         # 添加有效性检查
        total_keywords = len(self.keywords)
        unique_values = len(set(self.keywords.values())) if total_keywords > 0 else 0

        # 唯一映射率计算保护
        unique_ratio = unique_values / total_keywords if total_keywords > 0 else 0
        
        # 最长关键词检查
        longest_key = max(self.keywords.keys(), key=len) if total_keywords > 0 else "无"

        # 在计算前添加保护
        total = len(self.keywords)
        unique_ratio = len(set(self.keywords.values())) / total if total > 0 else 0
        longest = max(self.keywords.keys(), key=len) if total > 0 else "无"

        text.insert(tk.END, "\n映射有效性检查：\n")
        text.insert(tk.END, f"• 唯一映射率：{unique_ratio:.1%}\n")  # 自动处理零值
        text.insert(tk.END, f"• 最长关键词：{longest_key}\n")  # 添加空值保护
        
        # 控制面板
        control_frame = ttk.Frame(self.keyword_win)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Label(control_frame, text="新关键词:").pack(side=tk.LEFT)
        self.new_kw_entry = ttk.Entry(control_frame, width=25)
        self.new_kw_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="添加", command=self._add_keyword).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="删除选中", command=self._del_keyword).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="保存", command=self._save_keywords).pack(side=tk.RIGHT, padx=2)

        # 关键词列表
        list_frame = ttk.Frame(self.keyword_win)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.kw_listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.EXTENDED,
            font=('Consolas', 10)
        )
        scrollbar = ttk.Scrollbar(list_frame, command=self.kw_listbox.yview)
        self.kw_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.kw_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 加载初始数据
        self._refresh_keyword_list()

        # 加载并显示当前关键词
        try:
            current_keywords = self._load_keyword_config()
            text.insert(tk.END, f"当前关键词总数：{len(current_keywords)}\n\n")
            for i, (k, v) in enumerate(sorted(self.keywords.items()), 1):
                text.insert(tk.END, f"{i:03d}. {k} → {v}\n")  # 显示映射关系
        except Exception as e:
            text.insert(tk.END, f"加载关键词失败：{str(e)}")
        
        text.configure(state=tk.DISABLED)

    def _validate_directory(self):
        """验证目标文件夹有效性"""
        if not self.selected_dir:
            messagebox.showerror("错误", "请先选择目标文件夹")
            return False
        if not os.path.isdir(self.selected_dir):
            messagebox.showerror("错误", f"无效的文件夹路径：{self.selected_dir}")
            return False
        return True

    # 在Application类中添加新方法
    def start_keyword_conversion(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """启动关键词转换线程"""
        self.filter_extensions = [ext.strip() for ext in self.ext_entry.get().split(',')]
        threading.Thread(target=self.run_keyword_conversion).start()

    def run_keyword_conversion(self):
        """执行独立的关键词替换"""
        if not self._validate_directory():
            return
        
        try:
            self.progress['value'] = 0
            target_files = list(self.get_target_files())
            total_files = len(target_files)
            
            for i, file_path in enumerate(target_files, 1):
                try:
                    # 添加编码自动检测
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        detected_encoding = chardet.detect(raw_data)['encoding'] or self.encoding_var.get()
                    
                    # 使用检测到的编码重新打开文件
                    with open(file_path, 'r+', encoding=detected_encoding, errors='replace') as f:
                        content = f.read()
                        replaced = self._replace_keyword_only(content)
                        
                        # 只有内容变化时才写入
                        if content != replaced:
                            f.seek(0)
                            f.write(replaced)
                            f.truncate()
                            self.log_message(f"成功修改：{os.path.basename(file_path)}")
                        else:
                            self.log_message(f"无变化跳过：{os.path.basename(file_path)}")
                            
                except Exception as e:
                    self.log_message(f"处理失败：{file_path} - {str(e)}")
                
                self.progress['value'] = (i / total_files) * 100
                self.update_idletasks()
            
            self.show_result(True, "关键词替换完成！")
        except Exception as e:
            self.log_message(f"系统错误：{str(e)}")

    def start_char_mapping(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """启动字符映射线程"""
        self.filter_extensions = [ext.strip() for ext in self.ext_entry.get().split(',')]
        threading.Thread(target=self.run_char_mapping).start()

    def run_char_mapping(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """执行独立的字符映射"""
        self._execute_conversion(is_char_mapping=True)

    def _execute_conversion(self, is_char_mapping):
        """通用转换执行方法"""
        try:
            self.progress['value'] = 0
            target_files = list(self.get_target_files())
            total_files = len(target_files)
            
            for i, file_path in enumerate(target_files, 1):
                try:
                    with open(file_path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                        content = f.read()
                        
                        # 根据标志位执行不同替换
                        if is_char_mapping:
                            replaced = self._replace_char_only(content)
                        else:
                            replaced = self._replace_keyword_only(content)
                        
                        f.seek(0)
                        f.write(replaced)
                        f.truncate()
                    self.log_message(f"成功处理：{os.path.basename(file_path)}")
                except Exception as e:
                    self.log_message(f"处理失败：{file_path} - {str(e)}")
                
                self.progress['value'] = (i / total_files) * 100
                self.update_idletasks()
            
            self.show_result(True, f"{'字符映射' if is_char_mapping else '关键词替换'}完成！")
        except Exception as e:
            self.log_message(f"系统错误：{str(e)}")

    def _replace_keyword_only(self, content):
        """仅执行关键词替换（带调试日志）"""
        def replacer(match):
            original = match.group(1)
            mapped = self.keywords.get(original, original)
            if original != mapped:
                self.log_message(f"替换关键词: {original} → {mapped}")
            return mapped
        
        return self.keyword_pattern.sub(replacer, content)

    def _replace_char_only(self, content):
        """仅执行字符映射"""
        trans_table = str.maketrans(self.mapping)
        return content.translate(trans_table)

    def check_mapping_conflicts(self):
        """检查映射冲突（用于恢复前验证）"""
        value_map = {}
        conflicts = []
        
        with open(self.keyword_config_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                original = row['Original'].strip()
                mapped = row['Mapped'].strip()
                
                if mapped in value_map:
                    conflicts.append(f"{mapped} → {value_map[mapped]} 与 {original}")
                value_map[mapped] = original
        
        if conflicts:
            msg = "发现反向映射冲突：\n" + "\n".join(conflicts)
            return messagebox.askyesno(
                "映射冲突", 
                msg + "\n\n是否继续恢复？可能会覆盖部分映射关系"
            )
        return True
    # 添加恢复方法
    def start_keyword_restore(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """关键词恢复"""
        if not os.path.exists(self.keyword_config_path):
            messagebox.showerror("错误", "找不到关键词映射表文件")
            return
        
        if not self.check_mapping_conflicts():
            return  # 用户取消操作
        
        threading.Thread(target=self.run_keyword_restore).start()

    def run_keyword_restore(self):
        """执行关键词恢复"""
        self._execute_restore(restore_type='keyword')

    def start_char_restore(self):
        if not self._validate_directory():
            return  # 验证失败直接返回
        """字符映射恢复"""
        reverse_path = os.path.join(get_script_dir(), 'reverse_mapping.json')
        if not os.path.exists(reverse_path):
            messagebox.showerror("错误", "找不到字符反向映射表文件")
            return
        threading.Thread(target=self.run_char_restore).start()

    def run_char_restore(self):
        """执行字符映射恢复"""
        self._execute_restore(restore_type='char')

    def _execute_restore(self, restore_type):
        """通用恢复执行方法"""
        try:
            reverse_mapping = {}
            if restore_type == 'keyword':
                # 读取CSV构建反向映射表（处理多对一情况）
                with open(self.keyword_config_path, 'r') as f:
                    reader = csv.DictReader(f)
                    temp_map = {}
                    conflict_count = 0
                    
                    for row in reader:
                        mapped = row['Mapped'].strip()
                        original = row['Original'].strip()
                        if mapped in temp_map and temp_map[mapped] != original:
                            self.log_message(f"映射冲突：{mapped} 对应多个原始值")
                            conflict_count += 1
                        temp_map[mapped] = original
                    
                    if conflict_count > 0:
                        messagebox.showwarning("映射冲突", 
                            f"发现{conflict_count}处映射冲突，将使用最后出现的映射关系")
                    
                    # 按长度降序排序避免部分匹配
                    sorted_keys = sorted(temp_map.keys(), key=len, reverse=True)
                    reverse_mapping = {
                        k: temp_map[k] 
                        for k in sorted_keys
                        if k and temp_map[k]
                    }
                    
                    # 构建正则表达式模式
                    restore_pattern = re.compile(
                        r'(?<!\w)(' + '|'.join(map(re.escape, sorted_keys)) + r')(?!\w)',
                        flags=re.UNICODE
                    )
            # ... [保持原有字符恢复逻辑不变] ...

            # 修改后的恢复处理流程
            self.progress['value'] = 0
            target_files = list(self.get_target_files())
            total_files = len(target_files)
            
            for i, file_path in enumerate(target_files, 1):
                try:
                    with open(file_path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                        content = f.read()
                        
                        if restore_type == 'keyword':
                            # 使用正则表达式进行整词替换
                            def replacer(match):
                                return reverse_mapping[match.group(1)]
                            
                            restored = restore_pattern.sub(replacer, content)
                        else:
                            # 保持原有字符级恢复逻辑
                            restored = ''.join([reverse_mapping.get(c, c) for c in content])
                        
                        # 只有内容变化时才写入
                        if content != restored:
                            f.seek(0)
                            f.write(restored)
                            f.truncate()
                            self.log_message(f"成功恢复：{os.path.basename(file_path)}")
                        else:
                            self.log_message(f"无变化跳过：{os.path.basename(file_path)}")
                            
                except Exception as e:
                    self.log_message(f"恢复失败：{file_path} - {str(e)}")
                
                self.progress['value'] = (i / total_files) * 100
                self.update_idletasks()
            
            self.show_result(True, f"{'关键词' if restore_type == 'keyword' else '字符'}恢复完成！")
        except Exception as e:
            self.log_message(f"恢复操作异常：{str(e)}")

    # 新增：构建其他UI组件的方法
    def _build_action_buttons(self, parent):
        action_frame = ttk.LabelFrame(parent, text="功能操作区")
        action_frame.grid(row=1, column=0, pady=10, sticky='ew', padx=5)
        
        # 第一列：关键词替换操作
        kw_frame = ttk.Frame(action_frame)
        kw_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(kw_frame, text="关键词替换").pack(anchor=tk.W)
        ttk.Button(
            kw_frame,
            text="开始关键词转换",
            command=self.start_keyword_conversion,
            style="Primary.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距
        
        ttk.Button(
            kw_frame,
            text="恢复关键词转换",
            command=self.start_keyword_restore,
            style="Warning.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距

        # 第二列：字符映射操作
        char_frame = ttk.Frame(action_frame)
        char_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        ttk.Label(char_frame, text="字符映射").pack(anchor=tk.W)
        ttk.Button(
            char_frame,
            text="开始字符映射",
            command=self.start_char_mapping,
            style="Success.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距
        
        ttk.Button(
            char_frame,
            text="恢复字符映射",
            command=self.start_char_restore,
            style="Info.TButton"
        ).pack(fill=tk.X, pady=2, padx=5, ipady=3)  # 增加内边距

        # 公共操作按钮
        common_frame = ttk.Frame(action_frame)
        common_frame.pack(side=tk.LEFT, padx=10)
        ttk.Button(common_frame, text="映射表", command=self.show_mapping).grid(row=0, column=0, padx=2)
        ttk.Button(common_frame, text="关键词", command=self.show_keywords).grid(row=0, column=1, padx=2)


    def _build_progress_bar(self, parent):
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.grid(row=2, column=0, sticky='ew', pady=5)

    def refresh_mapping(self):
        MAPPING_CONFIG_PATH = os.path.join(get_script_dir(), 'mapping_config.json')
        if os.path.exists(MAPPING_CONFIG_PATH):
            os.remove(MAPPING_CONFIG_PATH)
        self.mapping, self.reverse_mapping = load_or_create_mapping()
        messagebox.showinfo("完成", "已生成新映射表")

    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 配置区组件
        self._build_config_section(main_frame)
        
        # 新增：操作按钮区
        self._build_action_buttons(main_frame)
        
        # 新增：进度条
        self._build_progress_bar(main_frame)
        
        # 新增：日志区
        self._build_log_section(main_frame)

        # 修复按钮添加方式
        ttk.Button(
            self.config_frame,  # 使用实例变量
            text="刷新映射表", 
            command=self.refresh_mapping
        ).grid(row=0, column=4, padx=5, sticky='e')  # 添加具体布局参数

        ttk.Button(
            self.config_frame,
            text="提取关键字",
            command=self.extract_and_save_keywords
        ).grid(row=0, column=5, padx=10, sticky='e')
    
    def _build_config_section(self, parent):
        self.config_frame = ttk.LabelFrame(parent, text="配置设置")
        self.config_frame.grid(row=0, column=0, sticky='ew', pady=5)
        
        # 文件扩展名设置
        ttk.Label(self.config_frame, text="文件扩展名:").grid(row=0, column=0, sticky='w', padx=5)
        self.ext_entry = ttk.Entry(self.config_frame, width=25)
        self.ext_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.ext_entry.insert(0, ".c, .h, .cpp, .hpp, .make, .ini")

        # 编码选择设置（修复组合框定义）
        ttk.Label(self.config_frame, text="文件编码:").grid(row=0, column=2, sticky='w', padx=5)
        # 正确代码
        self.encoding_combo = ttk.Combobox(
            self.config_frame,
            textvariable=self.encoding_var,
            values=self.encodings,
            width=12,
            state='readonly'
        )
        self.encoding_combo.grid(row=0, column=3, sticky='ew', padx=5)

        # 刷新按钮（添加具体布局参数）
        ttk.Button(
            self.config_frame,
            text="刷新映射表",
            command=self.refresh_mapping
        ).grid(row=0, column=4, padx=5, sticky='e')

        # 配置列权重
        self.config_frame.columnconfigure(1, weight=1)
        self.config_frame.columnconfigure(3, weight=1)
        self.config_frame.columnconfigure(4, weight=1)

        # 目录选择部分
        dir_frame = ttk.Frame(self.config_frame)
        dir_frame.grid(row=1, column=0, columnspan=5, pady=5, sticky='ew')  # 修正跨列数
        
        ttk.Label(dir_frame, text="目标文件夹:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(dir_frame, text="浏览...", command=self.select_directory).pack(side=tk.RIGHT)


    def _filter_keywords(self, content):
        """过滤C/C++关键词并返回受保护的位置集合"""
        keyword_positions = set()
        # 查找所有关键词并记录字符位置
        for match in self.keyword_pattern.finditer(content):
            start, end = match.span()
            keyword_positions.update(range(start, end))
        return keyword_positions
    
    # 保留其他方法不变...
    def select_directory(self):
        dir_path = filedialog.askdirectory(title="选择目标文件夹")
        if dir_path:
            self.selected_dir = dir_path
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, dir_path)
            self.log_message(f"已选择目录：{dir_path}")
        else:  # 用户取消选择时清空路径
            self.selected_dir = ""
            self.dir_entry.delete(0, tk.END)

    def show_result(self, success, message):
        if success:
            messagebox.showinfo("操作成功", message)
        else:
            messagebox.showerror("操作失败", message)  
    
    def setup_logging(self):
        if not os.path.exists('operation.log'):
            open('operation.log', 'w').close()
            
    def log_message(self, message, show_gui=True):
        """增强的日志记录方法"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[AutoFix] {timestamp} - {message}\n"
        
        # 写入文件日志
        with open('operation.log', 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        # 更新GUI日志
        if show_gui and hasattr(self, 'log_text'):
            self.log_text.configure(state=tk.NORMAL)
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            self.log_text.configure(state=tk.DISABLED)
    
    def show_mapping(self):
        mapping_window = tk.Toplevel(self)
        mapping_window.title("字符映射表预览")
        
        tree = ttk.Treeview(mapping_window, columns=('Original', 'Mapped'), show='headings')
        tree.heading('Original', text="原始字符")
        tree.heading('Mapped', text="映射字符")
    
        # 显示所有字符映射关系
        for k, v in self.mapping.items():
            tree.insert('', tk.END, values=(k, v))  # 不再过滤小写字母
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def start_conversion(self):
        self.filter_extensions = [ext.strip() for ext in self.ext_entry.get().split(',')]
        threading.Thread(target=self.run_conversion).start()

    # 没啥用了,可以删除
    def run_restore(self):
        """执行恢复操作的完整实现"""
        try:
            # 改为：
            reverse_path = os.path.join(get_script_dir(), 'reverse_mapping.json')
            with open(reverse_path, 'r', encoding='utf-8') as f:
                reverse_mapping = json.load(f)

            self.progress['value'] = 0
            total_files = sum(1 for _ in self.get_target_files())
            processed = 0

            for root, _, files in os.walk(self.selected_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in self.filter_extensions):
                        path = os.path.join(root, file)
                        try:
                            with open(path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                                content = f.read()
                                restored = ''.join([reverse_mapping.get(c, c) for c in content])
                                f.seek(0)
                                f.write(restored)
                                f.truncate()
                            self.log_message(f"成功恢复文件：{path}")
                        except Exception as e:
                            self.log_message(f"恢复失败：{path} - {str(e)}")
                        
                        processed += 1
                        self.progress['value'] = (processed / total_files) * 100
                        self.update_idletasks()

            self.show_result(True, f"恢复完成！共处理{processed}个文件")
        except Exception as e:
            self.log_message(f"恢复操作异常：{str(e)}")
            self.show_result(False, f"恢复失败：{str(e)}")
            
    # 没啥用了,可以删除
    def start_restore(self):
        if not os.path.exists('reverse_mapping.json'):
            messagebox.showerror("错误", "找不到反向映射表文件")
            return
        threading.Thread(target=self.run_restore).start()

    def _replace_keywords(self, content):
        """执行两阶段替换：关键词→字符映射"""
        # 阶段1：关键词替换
        def keyword_replacer(match):
            original = match.group(0)
            mapped = self.keywords.get(original, original)
            if mapped != original:
                self.log_message(f"关键词替换: {original} → {mapped}")
            return mapped
        
        # 按长度降序排序避免部分匹配
        sorted_keys = sorted(self.keywords.keys(), key=len, reverse=True)
        keyword_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b'
        )
        phase1_content = keyword_pattern.sub(keyword_replacer, content)
        
        # 阶段2：字符级映射
        phase2_content = []
        for c in phase1_content:
            # 保留已替换关键词的内容
            phase2_content.append(self.mapping.get(c, c))
        return ''.join(phase2_content)

    def run_conversion(self):
        """执行转换操作的完整实现"""
        self.progress['value'] = 0
        total_files = sum(1 for _ in self.get_target_files())
        
        processed = 0
        for root, _, files in os.walk(self.selected_dir):
            for file in files:
                if any(file.endswith(ext) for ext in self.filter_extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r+', encoding=self.encoding_var.get(), errors='replace') as f:
                            content = f.read()
                            # 调用修正后的替换方法
                            replaced = self._replace_keywords(content)
                            
                            f.seek(0)
                            f.write(replaced)
                            f.truncate()
                        self.log_message(f"成功处理文件：{path}")
                    except Exception as e:  # 添加缺失的except块
                        self.log_message(f"处理失败：{path} - {str(e)}")
                    
                    processed += 1
                    self.progress['value'] = (processed / total_files) * 100
                    self.update_idletasks()
        
        self.show_result(True, f"转换完成！共处理{processed}个文件")
        reverse_path = os.path.join(get_script_dir(), 'reverse_mapping.json')
        save_reverse_mapping(self.mapping, reverse_path)
    
    def get_target_files(self):
        for root, _, files in os.walk(self.selected_dir):
            for file in files:
                if any(file.endswith(ext) for ext in self.filter_extensions):
                    yield os.path.join(root, file)
    
    # ... [保留原有目录选择和其他方法] ...

    @staticmethod
    def extract_keywords_from_file(file_path):
        """从单个文件中提取关键字，并过滤长度小于等于 MIN_KEYWORD_LENGTH 的词"""
        keyword_pattern = re.compile(
            r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\s*[\(;:])'  # 匹配函数名和变量名
        )
        keywords = set()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = keyword_pattern.findall(content)
                # 使用全局常量过滤长度大于 MIN_KEYWORD_LENGTH 的关键字
                keywords.update(match for match in matches if len(match) > MIN_KEYWORD_LENGTH)
        except Exception as e:
            print(f"无法读取文件 {file_path}：{str(e)}")
        return keywords


    @staticmethod
    def extract_keywords_from_folder(folder_path):
        """从文件夹中提取所有.c和.h文件的关键字"""
        all_keywords = set()
        extensions = ['.c', '.h', '.cpp', '.hpp', '.make', '.cpp']
        for root, _, files in os.walk(folder_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    # 通过类名调用静态方法
                    keywords = Application.extract_keywords_from_file(file_path)
                    all_keywords.update(keywords)
        return all_keywords

    @staticmethod
    def save_keywords_to_csv(keywords, output_file):
        """将关键字保存到CSV文件，仅保存长度大于 MIN_KEYWORD_LENGTH 的关键字"""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Keyword"])
                # 使用全局常量过滤长度大于 MIN_KEYWORD_LENGTH 的关键字
                for keyword in sorted(keyword for keyword in keywords if len(keyword) > MIN_KEYWORD_LENGTH):
                    writer.writerow([keyword])
        except Exception as e:
            raise RuntimeError(f"保存失败：{str(e)}")


if __name__ == "__main__":
    app = Application()
    app.mainloop()