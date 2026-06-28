# 弹窗类 - 包含动画和交互功能
import tkinter as tk
import random
from collections import deque
from config import (POPUP_WIDTH, POPUP_HEIGHT, POPUP_ANIMATION_SPEED,
                    POPUP_MOVE_SPEED, POPUP_FADE_SPEED, POPUP_MAX_COUNT,
                    FONT_FAMILY, FONT_SIZE)

class AnimatedPopup:
    """带动画和交互的弹窗类"""

    # 类变量：管理所有活跃窗口
    active_windows = deque(maxlen=POPUP_MAX_COUNT)
    collected_count = 0  # 收集的爱心数量

    def __init__(self, tip_text, theme, master=None):
        self.tip_text = tip_text
        self.theme = theme
        self.window = tk.Toplevel(master) if master else tk.Tk()
        self.alpha = 0.0  # 当前透明度
        self.dx = random.choice([-POPUP_MOVE_SPEED, POPUP_MOVE_SPEED])  # 水平速度
        self.dy = random.choice([-POPUP_MOVE_SPEED//2, POPUP_MOVE_SPEED//2])  # 垂直速度
        self.is_alive = True
        self.is_paused = False

        self._setup_window()
        self._create_widgets()
        self._setup_bindings()
        AnimatedPopup.active_windows.append(self)

    def _setup_window(self):
        """配置窗口基础属性"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # 随机位置
        x = random.randrange(0, screen_width - POPUP_WIDTH)
        y = random.randrange(0, screen_height - POPUP_HEIGHT)

        self.window.title('专属提示')
        self.window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}+{x}+{y}")
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)  # 无边框窗口
        self.window.attributes('-alpha', 0.0)  # 初始透明

    def _create_widgets(self):
        """创建窗口组件"""
        bg = random.choice(self.theme['colors'])
        font = self.theme['font']

        # 主框架
        self.frame = tk.Frame(self.window, bg=bg, bd=2, relief='raised')
        self.frame.pack(fill='both', expand=True)

        # 提示文本
        self.label = tk.Label(
            self.frame,
            text=self.tip_text,
            bg=bg,
            font=font,
            wraplength=POPUP_WIDTH - 20
        )
        self.label.pack(pady=10, padx=10, expand=True)

        # 收集爱心按钮（莫兰迪风格）
        self.close_btn = tk.Button(
            self.frame,
            text='♡',
            bg=bg,
            fg='#8B7D7D',
            font=('Arial', 12),
            command=self._on_collect,
            relief='flat',
            cursor='hand2',
            activebackground=bg,
            activeforeground='#D4B5B0'
        )
        self.close_btn.place(relx=1.0, rely=0.0, x=-8, y=5, anchor='ne')

    def _setup_bindings(self):
        """设置事件绑定"""
        # 拖动功能
        self.frame.bind('<Button-1>', self._start_drag)
        self.frame.bind('<B1-Motion>', self._on_drag)
        self.label.bind('<Button-1>', self._start_drag)
        self.label.bind('<B1-Motion>', self._on_drag)

        # 右键菜单
        self.window.bind('<Button-3>', self._show_context_menu)

        # 窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _start_drag(self, event):
        """开始拖动"""
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        """拖动窗口"""
        x = self.window.winfo_x() + (event.x - self._drag_x)
        y = self.window.winfo_y() + (event.y - self._drag_y)
        self.window.geometry(f'+{x}+{y}')

    def _show_context_menu(self, event):
        """显示右键菜单"""
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="关闭所有", command=self._close_all)
        menu.add_command(label="暂停" if not self.is_paused else "继续",
                        command=self._toggle_pause)
        menu.add_separator()
        menu.add_command(label="关闭", command=self._on_close)
        menu.post(event.x_root, event.y_root)

    def _on_collect(self):
        """收集爱心"""
        AnimatedPopup.collected_count += 1
        self._on_close()

    def _on_close(self):
        """关闭窗口"""
        if self.is_alive:
            self.is_alive = False
            self._fade_out()

    def _fade_out(self):
        """淡出动画"""
        if self.alpha > 0:
            self.alpha -= POPUP_FADE_SPEED
            self.alpha = max(0, self.alpha)
            self.window.attributes('-alpha', self.alpha)
            self.window.after(POPUP_ANIMATION_SPEED, self._fade_out)
        else:
            self.window.destroy()
            if self in AnimatedPopup.active_windows:
                AnimatedPopup.active_windows.remove(self)

    def _close_all(self):
        """关闭所有窗口"""
        for win in list(AnimatedPopup.active_windows):
            win._on_close()

    def _toggle_pause(self):
        """切换暂停状态"""
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self._move()

    def fade_in(self):
        """淡入动画"""
        if self.alpha < 1.0:
            self.alpha += POPUP_FADE_SPEED
            self.alpha = min(1.0, self.alpha)
            self.window.attributes('-alpha', self.alpha)
            self.window.after(POPUP_ANIMATION_SPEED, self.fade_in)
        else:
            # 淡入完成后开始移动
            self._move()

    def _move(self):
        """移动动画"""
        if not self.is_alive or self.is_paused:
            return

        x = self.window.winfo_x() + self.dx
        y = self.window.winfo_y() + self.dy

        # 边界检测 - 反弹
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        if x <= 0 or x >= screen_width - POPUP_WIDTH:
            self.dx = -self.dx
        if y <= 0 or y >= screen_height - POPUP_HEIGHT:
            self.dy = -self.dy

        self.window.geometry(f'+{x}+{y}')
        self.window.after(POPUP_ANIMATION_SPEED, self._move)

    def show(self):
        """显示弹窗（带动画）"""
        self.fade_in()

    @classmethod
    def get_collected_count(cls):
        """获取收集数量"""
        return cls.collected_count

    @classmethod
    def close_all_windows(cls):
        """关闭所有活跃窗口"""
        for win in list(cls.active_windows):
            win._on_close()
