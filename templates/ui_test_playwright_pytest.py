import pytest
from playwright.sync_api import Page, expect

class LoginPage:
    """
    Page Object Model (POM) 示例：登录页面
    将页面元素定位与业务逻辑封装，提高代码可维护性
    """
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.error_message = page.locator(".error-msg")

    def navigate(self):
        self.page.goto("https://example.com/login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

class TestUIExample:
    """
    Playwright UI 自动化测试示例
    """

    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self, page: Page):
        """
        前置/后置处理：每个用例开始前打印日志，结束后截图
        """
        print(f"\nStarting test: {page.url}")
        yield
        # 失败截图逻辑通常在 conftest.py 的 hook 中实现，这里仅作演示
        if page.url:
            page.screenshot(path=f"output/screenshot_{int(time.time())}.png")

    def test_login_success(self, page: Page):
        """
        [正向测试] 用户登录成功
        """
        login_page = LoginPage(page)
        login_page.navigate()
        
        # 执行登录
        login_page.login("test_user", "password123")
        
        # 断言：URL 跳转或出现特定元素
        # expect(page).to_have_url("https://example.com/dashboard")
        # expect(page.locator("text=Welcome")).to_be_visible()

    def test_login_failure(self, page: Page):
        """
        [逆向测试] 密码错误
        """
        login_page = LoginPage(page)
        login_page.navigate()
        
        login_page.login("test_user", "wrong_password")
        
        # 断言：错误提示可见
        expect(login_page.error_message).to_be_visible()
        expect(login_page.error_message).to_contain_text("Invalid credentials")

    def test_network_interception(self, page: Page):
        """
        [高级技巧] 网络拦截与 Mock
        """
        # Mock 一个 API 响应
        page.route("**/api/user/profile", lambda route: route.fulfill(
            status=200,
            body='{"id": 1, "name": "Mocked User"}',
            headers={"Content-Type": "application/json"}
        ))
        
        page.goto("https://example.com/profile")
        # 验证页面是否显示了 Mock 的数据
        expect(page.locator("text=Mocked User")).to_be_visible()

import time
if __name__ == "__main__":
    # 运行测试：pytest -v ui_test_playwright_pytest.py
    pytest.main(["-v", "ui_test_playwright_pytest.py"])
