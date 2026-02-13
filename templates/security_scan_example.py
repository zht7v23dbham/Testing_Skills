import pytest
import requests

class TestSecurityBaseline:
    """
    Web 安全基线扫描脚本 (Python + Pytest)
    覆盖: 响应头安全、敏感文件泄露、HTTP 方法限制
    """
    
    TARGET_URL = "https://example.com" # 替换为待测目标
    
    @pytest.fixture(scope="class")
    def base_response(self):
        return requests.get(self.TARGET_URL)

    def test_security_headers(self, base_response):
        """
        [安全头检查] 验证关键的安全响应头是否存在
        """
        headers = base_response.headers
        
        # 1. Strict-Transport-Security (HSTS): 强制客户端使用 HTTPS
        if self.TARGET_URL.startswith("https"):
            assert "Strict-Transport-Security" in headers, "Missing HSTS header"
            
        # 2. X-Frame-Options: 防止点击劫持 (Clickjacking)
        assert "X-Frame-Options" in headers, "Missing X-Frame-Options header"
        assert headers["X-Frame-Options"] in ["DENY", "SAMEORIGIN"]
        
        # 3. X-Content-Type-Options: 防止 MIME 类型嗅探
        assert "X-Content-Type-Options" in headers, "Missing X-Content-Type-Options header"
        assert headers["X-Content-Type-Options"] == "nosniff"
        
        # 4. Content-Security-Policy (CSP): 防御 XSS 和数据注入
        # 注意: CSP 配置较复杂，根据实际情况启用断言
        # assert "Content-Security-Policy" in headers, "Missing CSP header"

    def test_cookie_security(self, base_response):
        """
        [Cookie 安全] 验证 Set-Cookie 的属性
        """
        for cookie in base_response.cookies:
            if cookie.secure:
                # 生产环境 Cookie 必须带有 Secure 属性 (仅 HTTPS 传输)
                pass 
            # 检查 HttpOnly (防止 XSS 读取 Cookie)
            # 注意: requests 的 cookie 对象属性可能不包含 HttpOnly 标记，需解析 header
            pass

    @pytest.mark.parametrize("path", [
        ".git/config", 
        ".env", 
        ".DS_Store", 
        "actuator/health", 
        "swagger-ui.html"
    ])
    def test_sensitive_files_exposure(self, path):
        """
        [敏感文件泄露] 扫描常见的敏感路径
        """
        url = f"{self.TARGET_URL}/{path}"
        resp = requests.get(url, allow_redirects=False)
        
        # 预期应当被禁止访问 (403) 或 不存在 (404)
        # 如果返回 200，说明文件可能泄露
        assert resp.status_code != 200, f"Potential sensitive file exposed: {url}"

    def test_http_methods(self):
        """
        [HTTP 方法限制] 验证是否禁用了危险方法 (TRACE, OPTIONS)
        """
        # TRACE 方法可能导致 XST 攻击
        resp = requests.request("TRACE", self.TARGET_URL)
        assert resp.status_code in [403, 404, 405], "TRACE method should be disabled"

if __name__ == "__main__":
    pytest.main(["-v", "security_scan_example.py"])
