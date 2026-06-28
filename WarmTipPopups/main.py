# 温馨提示弹窗 - 主程序
import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading

from config import DEFAULT_TIPS, POPUP_MAX_COUNT
from themes import THEMES, get_theme_names, get_theme
from popup import AnimatedPopup
from particles import ParticleEffect
from file_loader import load_tips_from_file_dialog
from ending import show_ending_card


class WarmTipApp:
    """温馨提示弹窗应用"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💕 温馨提示弹窗")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        # 莫兰迪风格背景色
        self.root.configure(bg='#F5F0EB')

        # 状态变量
        self.tips = list(DEFAULT_TIPS)
        self.current_theme = "浪漫"
        self.particle_effect = None
        self.is_running = False

        self._setup_ui()

    def _setup_ui(self):
        """设置用户界面"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="💕 温馨提示弹窗",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=10)

        # 主题选择
        theme_frame = tk.LabelFrame(self.root, text="选择主题", padx=10, pady=5)
        theme_frame.pack(fill='x', padx=20, pady=5)

        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_names = get_theme_names()

        for i, name in enumerate(theme_names):
            rb = tk.Radiobutton(
                theme_frame,
                text=f"{THEMES[name]['title']}",
                variable=self.theme_var,
                value=name,
                command=self._on_theme_change
            )
            rb.grid(row=i//3, column=i%3, sticky='w', padx=5)

        # 提示语管理
        tips_frame = tk.LabelFrame(self.root, text="提示语管理", padx=10, pady=5)
        tips_frame.pack(fill='both', expand=True, padx=20, pady=5)

        # 提示语列表
        self.tips_listbox = tk.Listbox(tips_frame, height=8)
        self.tips_listbox.pack(fill='both', expand=True)

        # 添加滚动条
        scrollbar = tk.Scrollbar(self.tips_listbox)
        scrollbar.pack(side='right', fill='y')
        self.tips_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tips_listbox.yview)

        # 更新列表显示
        self._update_tips_list()

        # 按钮区域
        btn_frame = tk.Frame(tips_frame)
        btn_frame.pack(fill='x', pady=5)

        tk.Button(
            btn_frame,
            text="📁 导入TXT文件",
            command=self._import_tips
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="➕ 添加",
            command=self._add_tip
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="➖ 删除",
            command=self._delete_tip
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="💾 保存",
            command=self._save_tips
        ).pack(side='left', padx=5)

        # 控制区域
        control_frame = tk.LabelFrame(self.root, text="控制面板", padx=10, pady=5)
        control_frame.pack(fill='x', padx=20, pady=5)

        # 弹窗数量
        count_frame = tk.Frame(control_frame)
        count_frame.pack(fill='x', pady=2)

        tk.Label(count_frame, text="弹窗数量:").pack(side='left')
        self.count_var = tk.IntVar(value=100)
        self.count_scale = tk.Scale(
            count_frame,
            from_=10,
            to=POPUP_MAX_COUNT,
            orient='horizontal',
            variable=self.count_var
        )
        self.count_scale.pack(side='left', fill='x', expand=True)

        # 粒子效果开关
        self.particle_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            control_frame,
            text="✨ 启用粒子效果",
            variable=self.particle_var
        ).pack(anchor='w')

        # 结束卡片开关
        self.ending_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            control_frame,
            text="🎉 显示结束卡片",
            variable=self.ending_var
        ).pack(anchor='w')

        # 结束语输入
        ending_frame = tk.Frame(control_frame)
        ending_frame.pack(fill='x', pady=(5, 0))

        tk.Label(ending_frame, text="结束语:").pack(side='left')
        self.ending_entry = tk.Entry(ending_frame, width=30)
        self.ending_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.ending_entry.insert(0, "愿这份温暖，永远陪伴着你")

        # 启动按钮（莫兰迪粉配色）
        self.start_btn = tk.Button(
            self.root,
            text="🚀 启动弹窗",
            font=("微软雅黑", 12, "bold"),
            bg="#D4B5B0",
            fg="#5D4E4E",
            activebackground="#C9A9A6",
            command=self._start_popups
        )
        self.start_btn.pack(pady=10, fill='x', padx=20)

        # 状态栏
        self.status_label = tk.Label(
            self.root,
            text=f"已加载 {len(self.tips)} 条提示语 | 收集爱心: 0",
            relief='sunken',
            anchor='w'
        )
        self.status_label.pack(side='bottom', fill='x')

    def _update_tips_list(self):
        """更新提示语列表"""
        self.tips_listbox.delete(0, tk.END)
        for tip in self.tips:
            self.tips_listbox.insert(tk.END, tip[:30] + "..." if len(tip) > 30 else tip)

    def _on_theme_change(self):
        """主题改变回调"""
        self.current_theme = self.theme_var.get()

    def _import_tips(self):
        """导入提示语文件"""
        new_tips = load_tips_from_file_dialog(self.root)
        if new_tips:
            self.tips.extend(new_tips)
            # 去重
            self.tips = list(dict.fromkeys(self.tips))
            self._update_tips_list()
            self._update_status()

    def _add_tip(self):
        """添加新提示语"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加提示语")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="输入新的提示语:").pack(pady=10)

        entry = tk.Entry(dialog, width=40)
        entry.pack(pady=5)
        entry.focus()

        def add():
            tip = entry.get().strip()
            if tip:
                self.tips.append(tip)
                self._update_tips_list()
                self._update_status()
                dialog.destroy()

        tk.Button(dialog, text="添加", command=add).pack(pady=10)
        entry.bind('<Return>', lambda e: add())

    def _delete_tip(self):
        """删除选中的提示语"""
        selection = self.tips_listbox.curselection()
        if selection:
            index = selection[0]
            self.tips.pop(index)
            self._update_tips_list()
            self._update_status()

    def _save_tips(self):
        """保存提示语到文件"""
        from file_loader import save_tips_to_txt
        save_tips_to_txt(self.tips)

    def _update_status(self):
        """更新状态栏"""
        collected = AnimatedPopup.get_collected_count()
        self.status_label.config(
            text=f"已加载 {len(self.tips)} 条提示语 | 收集爱心: {collected}"
        )

    def _start_popups(self):
        """启动弹窗"""
        if self.is_running:
            AnimatedPopup.close_all_windows()
            if self.particle_effect:
                self.particle_effect.stop()
            self.start_btn.config(text="🚀 启动弹窗", bg="#D4B5B0")
            self.is_running = False
            return

        if not self.tips:
            messagebox.showwarning("警告", "请先添加或导入提示语！")
            return

        self.is_running = True
        self.start_btn.config(text="⏹ 停止弹窗", bg="#C9A9A6")

        # 启动粒子效果（使用莫兰迪配色）
        if self.particle_var.get():
            theme = get_theme(self.current_theme)
            particle_colors = theme.get('particle_colors', None)
            self.particle_effect = ParticleEffect(self.root, theme['particle'], particle_colors)
            self.particle_effect.start()

        # 启动弹窗
        count = self.count_var.get()
        threading.Thread(target=self._create_popups, args=(count,), daemon=True).start()

        # 定期更新状态
        self._periodic_update()

    def _create_popups(self, count):
        """创建弹窗（在新线程中运行）"""
        theme = get_theme(self.current_theme)

        for i in range(count):
            if not self.is_running:
                break

            tip = random.choice(self.tips)

            # 在主线程中创建窗口
            self.root.after(0, lambda t=tip, th=theme: self._create_single_popup(t, th))
            threading.Event().wait(0.15)  # 控制弹出速度（稍缓）

        # 弹窗创建完成后，等待一会儿再显示结束卡片
        if self.is_running and self.ending_var.get():
            threading.Event().wait(2)  # 等待2秒
            ending_msg = self.ending_entry.get().strip() or "愿这份温暖，永远陪伴着你"
            self.root.after(0, lambda msg=ending_msg: self._show_ending(msg))

    def _create_single_popup(self, tip, theme):
        """创建单个弹窗"""
        if self.is_running:
            popup = AnimatedPopup(tip, theme, self.root)
            popup.show()

    def _show_ending(self, message):
        """显示结束卡片"""
        # 停止粒子效果
        if self.particle_effect:
            self.particle_effect.stop()

        # 显示全屏结束卡片
        show_ending_card(self.root, self.current_theme, message)

        # 重置状态
        self.is_running = False
        self.start_btn.config(text="🚀 启动弹窗", bg="#D4B5B0")

    def _periodic_update(self):
        """定期更新状态"""
        if self.is_running:
            self._update_status()
            self.root.after(1000, self._periodic_update)

    def run(self):
        """运行应用"""
        self.root.mainloop()


if __name__ == "__main__":
    app = WarmTipApp()
    app.run()
