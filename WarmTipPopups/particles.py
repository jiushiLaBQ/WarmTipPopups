# 莫兰迪粒子效果模块
import tkinter as tk
import random
from config import PARTICLE_SYMBOLS, PARTICLE_COUNT, PARTICLE_FALL_SPEED

class Particle:
    """单个粒子类"""

    def __init__(self, canvas, symbol, x, y, colors):
        self.canvas = canvas
        self.symbol = symbol
        self.x = x
        self.y = y
        self.colors = colors  # 莫兰迪颜色列表
        self.speed = random.uniform(0.5, PARTICLE_FALL_SPEED * 2)
        self.drift = random.uniform(-0.8, 0.8)  # 水平漂移（减小幅度）
        self.opacity = 0.9
        self.text_id = None

    def create(self):
        """创建粒子"""
        self.text_id = self.canvas.create_text(
            self.x, self.y,
            text=self.symbol,
            font=('Arial', random.randint(10, 20)),
            fill=random.choice(self.colors)
        )

    def update(self):
        """更新粒子位置"""
        if self.text_id is None:
            return False

        self.y += self.speed
        self.x += self.drift
        self.opacity -= 0.003  # 减慢消失速度

        if self.opacity <= 0 or self.y > self.canvas.winfo_height():
            self.canvas.delete(self.text_id)
            return False

        self.canvas.coords(self.text_id, self.x, self.y)
        return True


class ParticleEffect:
    """莫兰迪粒子效果管理器"""

    def __init__(self, parent, particle_type='heart', particle_colors=None):
        self.parent = parent
        self.particle_type = particle_type
        # 使用主题提供的莫兰迪颜色，或默认颜色
        self.particle_colors = particle_colors or [
            '#D4B5B0',  # 莫兰迪粉
            '#B5C4B1',  # 莫兰迪绿
            '#C5B9CD',  # 莫兰迪紫
            '#D5C4A1',  # 莫兰迪杏
            '#A7C4D4',  # 莫兰迪蓝
        ]
        self.particles = []
        self.canvas = None
        self.is_running = False

    def start(self):
        """启动粒子效果"""
        # 创建全屏透明 Canvas
        self.canvas = tk.Canvas(
            self.parent,
            width=self.parent.winfo_screenwidth(),
            height=self.parent.winfo_screenheight(),
            bg='black',
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)
        self.canvas.tk.call('wm', 'attributes', '.', '-transparentcolor', 'black')
        self.canvas.configure(bg='black')

        self.is_running = True
        self._spawn_particles()
        self._animate()

    def stop(self):
        """停止粒子效果"""
        self.is_running = False
        if self.canvas:
            self.canvas.destroy()

    def _spawn_particles(self):
        """生成新粒子"""
        if not self.is_running:
            return

        symbols = PARTICLE_SYMBOLS.get(self.particle_type, PARTICLE_SYMBOLS['heart'])

        if len(self.particles) < PARTICLE_COUNT:
            symbol = random.choice(symbols)
            x = random.randint(0, self.parent.winfo_screenwidth())
            y = random.randint(-50, -10)

            particle = Particle(self.canvas, symbol, x, y, self.particle_colors)
            particle.create()
            self.particles.append(particle)

        self.parent.after(150, self._spawn_particles)  # 降低生成频率

    def _animate(self):
        """动画循环"""
        if not self.is_running:
            return

        # 更新所有粒子
        self.particles = [p for p in self.particles if p.update()]

        self.parent.after(30, self._animate)


def create_particle_effect(parent, particle_type='heart', particle_colors=None):
    """创建并返回粒子效果实例"""
    return ParticleEffect(parent, particle_type, particle_colors)
