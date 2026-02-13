import pytest
import requests
import time
import json

class TestTencentAdsAPI:
    """
    腾讯广告 Marketing API 接口自动化测试模板 (Python + Pytest)
    针对沙箱环境 (Sandbox) 设计，包含 OAuth 2.0 鉴权、公共参数处理及错误码断言。
    """
    
    # 沙箱环境 API 地址
    BASE_URL = "https://sandbox-api.e.qq.com/v1.3"
    
    # 你的开发者 Access Token (建议从环境变量或配置文件读取)
    ACCESS_TOKEN = "YOUR_SANDBOX_ACCESS_TOKEN"
    ACCOUNT_ID = 12345678 # 你的测试账号 ID
    
    @pytest.fixture(scope="class")
    def common_headers(self):
        """
        公共请求头
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}" # 标准 OAuth 2.0 Bearer Token
        }

    def test_get_campaigns_list(self, common_headers):
        """
        [正向测试] 获取推广计划列表
        覆盖维度: 1.正向测试, 5.权限与认证
        """
        url = f"{self.BASE_URL}/campaigns/get"
        params = {
            "account_id": self.ACCOUNT_ID,
            "filtering": json.dumps([{"field": "promoted_object_type", "operator": "EQUALS", "values": ["PROMOTED_OBJECT_TYPE_LINK"]}]),
            "page": 1,
            "page_size": 10
        }
        
        # GET 请求带 Query 参数
        response = requests.get(url, params=params, headers=common_headers)
        
        # 断言 HTTP 状态码
        assert response.status_code == 200, f"HTTP Error: {response.status_code}"
        
        data = response.json()
        
        # 断言业务状态码 (code=0 表示成功)
        assert data["code"] == 0, f"API Error: {data['message']}"
        
        # 断言分页数据结构
        assert "list" in data["data"]
        assert "page_info" in data["data"]
        assert data["data"]["page_info"]["page"] == 1

    def test_create_campaign_invalid_budget(self, common_headers):
        """
        [边界值测试] 创建推广计划 - 预算低于最小值
        覆盖维度: 3.边界值测试, 9.业务逻辑约束
        """
        url = f"{self.BASE_URL}/campaigns/add"
        payload = {
            "account_id": self.ACCOUNT_ID,
            "campaign_name": f"Test_Invalid_Budget_{int(time.time())}",
            "campaign_type": "CAMPAIGN_TYPE_NORMAL",
            "promoted_object_type": "PROMOTED_OBJECT_TYPE_LINK",
            "daily_budget": 100 # 预算仅 1 元 (100分)，通常低于最小限制 (如 50元)
        }
        
        response = requests.post(url, json=payload, headers=common_headers)
        data = response.json()
        
        # 预期失败，返回特定错误码 (例如 18002 预算错误)
        assert data["code"] != 0
        # assert data["code"] == 18002 
        print(f"Expected Error: {data['message']}")

    @pytest.mark.parametrize("invalid_token", ["", "invalid_token_123", "expired_token"])
    def test_auth_failure(self, invalid_token):
        """
        [权限测试] 无效 Token 访问
        覆盖维度: 5.权限与认证
        """
        url = f"{self.BASE_URL}/campaigns/get"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {invalid_token}"
        }
        params = {"account_id": self.ACCOUNT_ID}
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        # 预期鉴权失败 (code=10002 或其他鉴权错误码)
        assert data["code"] != 0
        # assert data["code"] in [10002, 10003]

if __name__ == "__main__":
    pytest.main(["-v", "tencent_ads_pytest.py"])
