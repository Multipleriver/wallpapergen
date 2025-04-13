import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import os
import time
import subprocess
import socket
import win32api
import win32con
import win32gui

def get_web_data(url):
    """从指定网页获取数据"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取全市场温度
        # 根据终端输出中的HTML结构定位温度元素
        market_temp_span = soup.find('span', {'class': 'tw-font-medium tw-text-orange'})
        
        if not market_temp_span:
            print("尝试查找市场温度元素，当前页面HTML结构:")
            print(soup.prettify()[:1000])  # 打印前1000字符用于调试
            print("所有span元素:", [str(tag) for tag in soup.find_all('span')[:10]])
            raise ValueError("未找到市场温度元素，请检查网页结构是否已更改")
        else:
            print("找到的温度元素:", market_temp_span)
        market_temp = market_temp_span.text.strip().replace('°', '')
        
        return {
            'market_temp': market_temp
        }
    except Exception as e:
        print(f"获取网页数据时出错: {e}")
        return None

def modify_wallpaper(data, is_offline=False):
    """修改壁纸并添加数据"""
    try:
        # 打开原始壁纸
        img = Image.open('wallpaper_prot.png')
        draw = ImageDraw.Draw(img)
        
        # 设置字体和大小
        font_large = ImageFont.truetype('bgothm.ttf', 96)
        font_medium = ImageFont.truetype('bgothm.ttf', 64)
        font_small = ImageFont.truetype('bgothm.ttf', 36)
        
        if is_offline:
            # 添加离线提示
            label_text = "Not connected to the internet"
            text_width = draw.textlength(label_text, font=font_large)
            x = (img.width - text_width) / 2
            draw.text((x, img.height - 800), label_text, font=font_large, fill='white')
        else:
            # 添加全市场温度
            label_text = "Market Temperature: "
            temp_text = f"{data['market_temp']}°"
            full_text = label_text + temp_text
            text_width = draw.textlength(full_text, font=font_large)
            x = (img.width - text_width) / 2
            
            # 绘制标签(白色)
            draw.text((x, img.height - 850), label_text, font=font_large, fill='white')
            
            # 绘制温度值(橙色)
            label_width = draw.textlength(label_text, font=font_large)
            draw.text((x + label_width, img.height - 850), temp_text, font=font_large, fill='orange')
        
        # 确保figures目录存在
        if not os.path.exists('figures'):
            os.makedirs('figures')
            
        # 保存修改后的壁纸，保存2张是因为幻灯片文件夹若只有一个文件是无法播放的
        img.save('figures/wallpaper_modified_0.png')
        img.save('figures/wallpaper_modified_1.png')
        print("壁纸修改并保存成功")
    except Exception as e:
        print(f"修改壁纸时出错: {e}")

def is_internet_connected():
    """检查网络连接状态"""
    try:
        # 尝试连接多个可靠的网站
        socket.create_connection(("www.google.com", 80), timeout=5)
        socket.create_connection(("www.baidu.com", 80), timeout=5)
        return True
    except OSError:
        try:
            # 如果Google不可用，尝试百度
            socket.create_connection(("www.baidu.com", 80), timeout=5)
            return True
        except OSError:
            print("网络连接检测失败")
            return False

def set_startup():
    """设置开机自启动"""
    try:
        key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, 
                                  "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                                  0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(key, "WallpaperUpdater", 0, win32con.REG_SZ, 
                             os.path.abspath(__file__))
        win32api.RegCloseKey(key)
        print("已设置开机自启动")
    except Exception as e:
        print(f"设置开机自启动失败: {e}")

def set_wallpaper(image_path):
    """设置壁纸"""
    try:
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, image_path, 0)
    except Exception as e:
        print(f"设置壁纸失败: {e}")

def schedule_update():
    """定时更新任务"""
    try:
        now = time.localtime()
        if now.tm_hour == 1 and now.tm_min == 0:  # 每天1点执行
            update_wallpaper()
    except Exception as e:
        print(f"程序运行出错: {e}")

def update_wallpaper():
    """更新壁纸"""
    url = "https://youzhiyouxing.cn/data/market"
    if is_internet_connected():
        data = get_web_data(url)
        if data:
            modify_wallpaper(data)
            # set_wallpaper(os.path.abspath('figures/wallpaper_modified.png'))
    else:
        modify_wallpaper(None, is_offline=True)
        # set_wallpaper(os.path.abspath('figures/wallpaper_modified.png'))

if __name__ == "__main__":
    set_startup()
    update_wallpaper()
    schedule_update()