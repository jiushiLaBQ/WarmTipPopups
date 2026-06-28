# 全屏精美卡片结束效果
import tkinter as tk
import random

# 莫兰迪卡片配色
CARD_THEMES = {
    "浪漫": {
        "bg": "#F5E6E8",      # 浅粉灰背景
        "accent": "#D4B5B0",  # 灰粉强调色
        "text": "#6B5B5B",    # 深灰棕文字
        "border": "#C9A9A6",  # 脏粉边框
        "sub_text": "#8B7D7D" # 浅灰棕副文字
    },
    "清新": {
        "bg": "#E8F0E8",      # 浅绿灰背景
        "accent": "#B5C4B1",  # 灰绿强调色
        "text": "#5B6B5B",    # 深灰绿文字
        "border": "#A8B8A0",  # 薄荷灰边框
        "sub_text": "#7D8B7D" # 浅灰绿副文字
    },
    "神秘": {
        "bg": "#EDE8F0",      # 浅紫灰背景
        "accent": "#C5B9CD",  # 灰紫强调色
        "text": "#5B5B6B",    # 深灰紫文字
        "border": "#B0A3B8",  # 暗紫边框
        "sub_text": "#7D7D8B" # 浅灰紫副文字
    },
    "温暖": {
        "bg": "#F0EDE5",      # 浅杏灰背景
        "accent": "#D5C4A1",  # 脏橘强调色
        "text": "#6B6350",    # 深灰杏文字
        "border": "#C4B48E",  # 杏色边框
        "sub_text": "#8B8068" # 浅灰杏副文字
    },
    "海洋": {
        "bg": "#E5EEF2",      # 浅蓝灰背景
        "accent": "#A7C4D4",  # 雾霾蓝强调色
        "text": "#506070",    # 深灰蓝文字
        "border": "#96B5C5",  # 灰蓝边框
        "sub_text": "#687888" # 浅灰蓝副文字
    }
}


class EndingCard:
    """全屏精美卡片"""

    def __init__(self, master, theme_name="浪漫", message=None):
        self.master = master
        self.theme_name = theme_name
        self.theme = CARD_THEMES.get(theme_name, CARD_THEMES["浪漫"])

        # 默认结束语
        self.message = message or "愿这份温暖，永远陪伴着你"
        self.sub_message = "💕 Created with WarmTipPopups"

        # 创建全屏窗口
        self.window = tk.Toplevel(master)
        self.window.attributes('-fullscreen', True)
        self.window.attributes('-topmost', True)

        # 透明度
        self.alpha = 0.0

        self._setup_ui()

    def _setup_ui(self):
        """设置界面"""
        # 全屏背景
        self.canvas = tk.Canvas(
            self.window,
            width=self.window.winfo_screenwidth(),
            height=self.window.winfo_screenheight(),
            bg=self.theme['bg'],
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)

        # 装饰性边框
        self._draw_decorations()

        # 中央内容区域
        self._create_center_content()

        # 绑定点击事件关闭
        self.canvas.bind('<Button-1>', lambda e: self._close())
        self.window.bind('<Escape>', lambda e: self._close())

    def _draw_decorations(self):
        """绘制装饰元素"""
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()

        # 上下装饰线
        line_y_top = screen_h // 2 - 100
        line_y_bottom = screen_h // 2 + 100

        self.canvas.create_line(
            100, line_y_top, screen_w - 100, line_y_top,
            fill=self.theme['accent'], width=2, dash=(10, 5)
        )
        self.canvas.create_line(
            100, line_y_bottom, screen_w - 100, line_y_bottom,
            fill=self.theme['accent'], width=2, dash=(10, 5)
        )

        # 四角装饰
        corner_size = 30
        corners = [
            (50, 50), (screen_w - 50, 50),
            (50, screen_h - 50), (screen_w - 50, screen_h - 50)
        ]
        for x, y in corners:
            self.canvas.create_text(
                x, y, text='✦',
                font=('Arial', 16),
                fill=self.theme['accent']
            )

        # 随机散落的小装饰
        decorations = ['♡', '✦', '✿', '·']
        for _ in range(20):
            x = random.randint(100, screen_w - 100)
            y = random.randint(100, screen_h - 100)
            # 避开中央区域
            if abs(x - screen_w//2) > 150 or abs(y - screen_h//2) > 120:
                self.canvas.create_text(
                    x, y,
                    text=random.choice(decorations),
                    font=('Arial', random.randint(8, 14)),
                    fill=self.theme['accent']
                )

    def _create_center_content(self):
        """创建中央内容"""
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()

        # 主标题
        self.main_text = self.canvas.create_text(
            screen_w // 2, screen_h // 2 - 30,
            text=self.message,
            font=('微软雅黑', 28, 'bold'),
            fill=self.theme['text'],
            anchor='center'
        )

        # 副标题
        self.sub_text = self.canvas.create_text(
            screen_w // 2, screen_h // 2 + 40,
            text=self.sub_message,
            font=('微软雅黑', 14),
            fill=self.theme['sub_text'],
            anchor='center'
        )

        # 提示文字
        self.hint_text = self.canvas.create_text(
            screen_w // 2, screen_h - 80,
            text='点击任意位置结束',
            font=('微软雅黑', 12),
            fill=self.theme['sub_text'],
            anchor='center'
        )

    def show(self, duration=None):
        """显示卡片（带淡入动画）"""
        self._fade_in()

        # 自动关闭（可选）
        if duration:
            self.window.after(duration, self._close)

    def _fade_in(self):
        """淡入动画"""
        if self.alpha < 1.0:
            self.alpha += 0.05
            self.alpha = min(1.0, self.alpha)
            self.window.attributes('-alpha', self.alpha)
            self.window.after(30, self._fade_in)

    def _close(self):
        """关闭卡片并退出程序"""
        self._fade_out()

    def _fade_out(self):
        """淡出动画后退出程序"""
        if self.alpha > 0:
            self.alpha -= 0.05
            self.alpha = max(0, self.alpha)
            self.window.attributes('-alpha', self.alpha)
            self.window.after(30, self._fade_out)
        else:
            self.window.destroy()
            # 关闭整个程序
            self.master.destroy()


def show_ending_card(master, theme_name="浪漫", message=None):
    """显示结束卡片的便捷函数"""
    card = EndingCard(master, theme_name, message)
    card.show()
    return card
