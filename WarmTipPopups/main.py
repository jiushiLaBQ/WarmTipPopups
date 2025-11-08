# 导入所需模块
import tkinter as tk  # 用于创建图形用户界面
import random  # 用于生成随机数和随机选择元素
import threading  # 用于创建多线程，实现多个窗口同时弹出
import time  # 用于控制弹窗弹出的时间间隔

def create_tip_window(tip_text):
    """创建单个提示窗口的通用函数"""
    window = tk.Tk()
    # 获取屏幕宽高
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # 窗口大小
    window_width = 250
    window_height = 60
    # 随机位置（确保窗口完全显示）
    x = random.randrange(0, screen_width - window_width)
    y = random.randrange(0, screen_height - window_height)
    # 设置窗口标题和位置
    window.title('专属提示')
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # 随机背景颜色
    bg_colors = [
        'lightpink', 'skyblue', 'lightgreen', 'lavender',
        'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine'
    ]
    bg = random.choice(bg_colors)
    # 创建标签
    tk.Label(
        window,
        text=tip_text,
        bg=bg,
        font=('微软雅黑', 13),
        width=30,
        height=6
    ).pack()
    # 窗口置顶
    window.attributes('-topmost', True)
    window.mainloop()

def show_warm_tips():
    """显示批量随机提示弹窗"""
    tips = [
        '愿深海的祝福与你我同在', '我想看的世界，在你眼里', '我心甘情愿被你困住',
        '下次一起去看海吧', '脸颊沾到颜料的你很可爱', '聊天记录是三万行情书', '早安，我的小保镖',
        '海风能吹散所有烦恼', '期待下一次见面', '喂喂喂，猜猜我是谁？',
        '画累了，需要见面充能', '我祝你，希望永不灭', '愿所有烦恼都消失',
        '又见面了，保镖小姐', '我的小鱼已经认识你了', '你相信，海底也会燃起火焰吗',
        '我想看的世界，在你眼里', '只是摸两下耳朵可不够', '会好起来的', '答应过你的，绝不会失约',
        '你是我唯一的选择', '你需要的话，我随时有空', '你从来都不是可怕的女巫', '想要哪条鱼，全都抓给你',
        '我祝你，希望永不灭', '要对你救助的小动物负责哦', '只要你会来，等待就值得',
        '我对你产生意义了吗','明年，我要你对我更贪心一点','那就和我在一起，溺死在同一片海里吧'
    ]
    # 创建线程列表
    threads = []
    # 弹窗数量（可调整）
    for i in range(300):
        tip = random.choice(tips)
        # 创建线程时绑定当前随机到的提示文字
        t = threading.Thread(target=create_tip_window, args=(tip,))
        threads.append(t)
        time.sleep(0.005)  # 控制弹窗弹出速度
        threads[i].start()

if __name__ == "__main__":
    # 先显示欢迎窗口
    create_tip_window("祁煜，我的名字")
    # 关闭欢迎窗口后，再显示批量提示弹窗
    show_warm_tips()