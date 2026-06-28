# 文件加载模块
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def load_tips_from_txt(file_path):
    """
    从 TXT 文件加载提示语

    支持格式：
    - 每行一条提示语
    - # 开头的行会被忽略（注释）
    - 空行会被忽略
    """
    tips = []
    try:
        # 尝试多种编码
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1']
        content = None

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError("无法识别文件编码")

        # 解析内容
        for line in content.splitlines():
            line = line.strip()
            # 跳过空行和注释
            if line and not line.startswith('#'):
                tips.append(line)

        return tips

    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
    except Exception as e:
        raise Exception(f"加载文件失败: {str(e)}")


def load_tips_from_file_dialog(parent=None):
    """通过文件对话框加载提示语"""
    file_path = filedialog.askopenfilename(
        parent=parent,
        title="选择提示语文件",
        filetypes=[
            ("文本文件", "*.txt"),
            ("所有文件", "*.*")
        ]
    )

    if not file_path:
        return None

    try:
        tips = load_tips_from_txt(file_path)
        if tips:
            messagebox.showinfo(
                "加载成功",
                f"成功加载 {len(tips)} 条提示语\n\n"
                f"文件: {os.path.basename(file_path)}"
            )
            return tips
        else:
            messagebox.showwarning(
                "加载警告",
                "文件中没有找到有效的提示语\n\n"
                "请确保每行一条提示语，# 开头的行会被忽略"
            )
            return None
    except Exception as e:
        messagebox.showerror("加载失败", str(e))
        return None


def save_tips_to_txt(tips, file_path=None):
    """保存提示语到 TXT 文件"""
    if file_path is None:
        file_path = filedialog.asksaveasfilename(
            title="保存提示语文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt")]
        )

    if not file_path:
        return False

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# 温馨提示语文件\n")
            f.write("# 每行一条提示语\n")
            f.write("# 以 # 开头的行会被忽略\n\n")
            for tip in tips:
                f.write(tip + '\n')

        messagebox.showinfo("保存成功", f"已保存 {len(tips)} 条提示语")
        return True
    except Exception as e:
        messagebox.showerror("保存失败", str(e))
        return False
