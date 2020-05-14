"""
Created by joe on 2019/12/6 
"""
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ChromeBrowser(object):
    """chrome web driver"""

    def __init__(self, prefs, *args):
        """
        init
        :param prefs: 首选项
            {
            "profile.managed_default_content_settings.images": 2    不加载图片
            "permissions.default.stylesheet": 2    优化css加载
            }
        :param args: 启动参数
            [
            -headless   无头模式
            --disable-gpu   禁用GPU加速
            --window-size=1280,800  设置窗口大小
            ]

        """
        options = Options()
        for arg in args:
            options.add_argument(arg)

        options.add_experimental_option("prefs", prefs)

        self.__driver = webdriver.Chrome(options=options)
        self.__driver_wait = WebDriverWait(self.__driver, 10)

    def goto(self, url):
        """
        前往指定页面
        :param url: 页面url
        :return:
        """
        self.__driver.get(url)

    def screenshots(self, path, selector=None, position=None):
        """
        从网页中截图
        :param path: 截图保存路径
        :param selector: 需要截图区域的选择器（可选）
        :param position: 截图位置（可选）
                {
                    "left": 0,
                    "top": 0,
                    "right": 0,
                    "bottom": 0
                }
        :return:
        """
        if not (selector or position):
            self.__driver.get_screenshot_as_file(path)
        else:
            img_bytes = self.__driver.get_screenshot_as_png()
            image = Image.open(BytesIO(img_bytes))
            if selector:
                element = self.__driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                location = element.location
                size = element.size
                left = location['x']
                top = location['y']
                right = left + size['width']
                bottom = top + size['height']
                position = {
                    "left": left,
                    "top": top,
                    "right": right,
                    "bottom": bottom
                }
            new_img = image.crop((position["left"], position["top"], position["right"], position["bottom"]))
            new_img.save(path)
