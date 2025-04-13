# Wallpaper Generator

## 项目功能

自动从[有知有行](https://youzhiyouxing.cn/data/market)获取市场温度数据，并生成带有该信息的壁纸图片。

## 使用说明

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 准备资源文件：
   - 确保项目目录下有`wallpaper_prot.png`作为基础壁纸
   - 确保有`bgothm.ttf`字体文件用于文字渲染

3. 运行程序：
   ```
   python gen.py
   ```

## 配置选项

- 壁纸保存路径：默认保存在`figures/`目录下
- 字体设置：当前使用`bgothm.ttf`字体

## 计划任务

程序会自动设置开机启动，并在每天1:00自动更新壁纸。

## 注意事项

- 需要联网才能获取市场温度数据
- 需要Windows系统支持
- 需要管理员权限设置壁纸和开机启动