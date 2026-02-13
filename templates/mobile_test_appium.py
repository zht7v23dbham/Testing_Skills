import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import time

class TestAppAdvertising:
    """
    移动端广告测试脚本 (Appium + Python)
    覆盖: 开屏广告、DeepLink 唤起
    """
    
    @pytest.fixture(scope="function")
    def driver(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.app_package = "com.example.ad.demo"
        options.app_activity = ".MainActivity"
        options.no_reset = True
        
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        yield driver
        driver.quit()

    def test_splash_ad_skip(self, driver):
        """
        [开屏广告] 验证开屏广告展示及跳过
        """
        # 等待开屏广告容器
        ad_container = driver.find_element(AppiumBy.ID, "com.example.ad.demo:id/splash_container")
        assert ad_container.is_displayed()
        
        # 等待跳过按钮 (显式等待建议使用 WebDriverWait)
        time.sleep(2) 
        skip_btn = driver.find_element(AppiumBy.ID, "com.example.ad.demo:id/btn_skip")
        skip_btn.click()
        
        # 验证进入首页
        home_tab = driver.find_element(AppiumBy.ID, "com.example.ad.demo:id/tab_home")
        assert home_tab.is_displayed()

    def test_deeplink_launch(self, driver):
        """
        [DeepLink] 验证通过 URL Scheme 唤起 App 指定页
        """
        # 模拟从浏览器唤起
        deep_link = "ad-demo://detail?id=1001"
        driver.get(deep_link)
        
        # 验证是否跳转到详情页
        title = driver.find_element(AppiumBy.ID, "com.example.ad.demo:id/page_title")
        assert title.text == "商品详情"

if __name__ == "__main__":
    pytest.main(["-v", "mobile_test_appium.py"])
