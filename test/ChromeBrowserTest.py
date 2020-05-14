"""
Created by joe on 2020/5/13

测试代码
"""
from src.chrome_browser import ChromeBrowser

browser = ChromeBrowser({"profile.managed_default_content_settings.images": 2, "permissions.default.stylesheet": 2})

browser.goto("https://www.baidu.com")
print()
