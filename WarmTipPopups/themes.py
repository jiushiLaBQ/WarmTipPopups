# 莫兰迪主题配置文件

THEMES = {
    "浪漫": {
        "colors": [
            '#D4B5B0',  # 灰粉
            '#C9A9A6',  # 脏粉
            '#E8D5D0',  # 浅粉灰
            '#BF9B9B',  # 暗粉
            '#DCC5C0',  # 藕粉
        ],
        "font": ("微软雅黑", 13),
        "particle": "heart",
        "title": "💕 浪漫莫兰迪",
        "particle_colors": ['#D4B5B0', '#C9A9A6', '#BF9B9B', '#E8D5D0']
    },
    "清新": {
        "colors": [
            '#B5C4B1',  # 灰绿
            '#A8B8A0',  # 薄荷灰
            '#C5D4C0',  # 浅绿灰
            '#9DB59A',  # 暗绿
            '#D0DDD0',  # 奶绿
        ],
        "font": ("微软雅黑", 13),
        "particle": "flower",
        "title": "🌸 清新莫兰迪",
        "particle_colors": ['#B5C4B1', '#A8B8A0', '#9DB59A', '#C5D4C0']
    },
    "神秘": {
        "colors": [
            '#C5B9CD',  # 灰紫
            '#B0A3B8',  # 暗紫
            '#D4C8DE',  # 浅紫灰
            '#9E92A8',  # 薰衣草灰
            '#DDD0E5',  # 淡紫
        ],
        "font": ("微软雅黑", 13),
        "particle": "star",
        "title": "✨ 神秘莫兰迪",
        "particle_colors": ['#C5B9CD', '#B0A3B8', '#9E92A8', '#D4C8DE']
    },
    "温暖": {
        "colors": [
            '#D5C4A1',  # 脏橘
            '#C4B48E',  # 杏色
            '#E0D4B8',  # 浅杏灰
            '#B8A882',  # 暗杏
            '#DDD0B5',  # 奶茶色
        ],
        "font": ("微软雅黑", 13),
        "particle": "heart",
        "title": "☀️ 温暖莫兰迪",
        "particle_colors": ['#D5C4A1', '#C4B48E', '#B8A882', '#E0D4B8']
    },
    "海洋": {
        "colors": [
            '#A7C4D4',  # 雾霾蓝
            '#96B5C5',  # 灰蓝
            '#B8D0DE',  # 浅蓝灰
            '#85A5B5',  # 暗蓝
            '#C8DDE8',  # 天蓝灰
        ],
        "font": ("微软雅黑", 13),
        "particle": "star",
        "title": "🌊 海洋莫兰迪",
        "particle_colors": ['#A7C4D4', '#96B5C5', '#85A5B5', '#B8D0DE']
    }
}

def get_theme_names():
    """获取所有主题名称"""
    return list(THEMES.keys())

def get_theme(theme_name):
    """获取指定主题配置"""
    return THEMES.get(theme_name, THEMES["浪漫"])

def get_random_theme():
    """随机获取一个主题"""
    import random
    return random.choice(list(THEMES.values()))
