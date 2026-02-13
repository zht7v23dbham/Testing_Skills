import pytest
import requests
import time
import json

class TestKuaishouAdsAPI:
    """
    快手磁力引擎 Marketing API 接口自动化测试模板 (Python + Pytest)
    适配快手广告层级结构 (Campaign -> Unit -> Creative)
    """
    
    # 快手 API 生产环境地址 (示例)
    BASE_URL = "https://api.e.kuaishou.com/v1"
    
    # 你的开发者 Access Token
    ACCESS_TOKEN = "YOUR_KWAI_ACCESS_TOKEN"
    ADVERTISER_ID = 12345678 # 广告主 ID
    
    @pytest.fixture(scope="class")
    def common_headers(self):
        """
        公共请求头: 快手使用 Access-Token
        """
        return {
            "Content-Type": "application/json",
            "Access-Token": self.ACCESS_TOKEN
        }

    def test_get_campaigns(self, common_headers):
        """
        [正向测试] 获取广告计划列表
        覆盖维度: 1.正向测试, 5.权限与认证
        """
        url = f"{self.BASE_URL}/campaign/list"
        params = {
            "advertiser_id": self.ADVERTISER_ID,
            "page": 1,
            "page_size": 20
        }
        
        response = requests.get(url, params=params, headers=common_headers)
        
        assert response.status_code == 200, f"HTTP Error: {response.status_code}"
        data = response.json()
        
        # 快手成功状态码通常为 0 (具体视文档而定，有时为 1，此处假设 0)
        assert data["code"] == 0, f"API Error: {data.get('message')}"
        assert "list" in data["data"]

    def test_create_unit_invalid_bid(self, common_headers):
        """
        [边界值测试] 创建广告组 - 出价异常
        覆盖维度: 3.边界值测试, 9.业务逻辑约束
        """
        url = f"{self.BASE_URL}/ad_unit/create"
        payload = {
            "advertiser_id": self.ADVERTISER_ID,
            "campaign_id": 10001,
            "unit_name": f"Test_Invalid_Bid_{int(time.time())}",
            "bid_type": 1, # OCPM
            "bid": -100,   # 负数出价 (边界值)
            "optimization_goal": 3
        }
        
        response = requests.post(url, json=payload, headers=common_headers)
        data = response.json()
        
        # 预期失败
        assert data["code"] != 0
        print(f"Expected Error: {data.get('message')}")

    def test_ocpm_deep_conversion(self, common_headers):
        """
        [场景测试] OCPM 深度转化双出价
        覆盖维度: 4.参数组合测试
        """
        url = f"{self.BASE_URL}/ad_unit/create"
        payload = {
            "advertiser_id": self.ADVERTISER_ID,
            "campaign_id": 10001,
            "unit_name": f"Test_Deep_Conv_{int(time.time())}",
            "bid_type": 1, # OCPM
            "optimization_goal": 5, # 激活
            "bid": 3000, # 激活出价 30元
            "deep_conversion_type": 3, # 次留
            "deep_bid": 6000 # 次留出价 60元
        }
        
        # 模拟请求发送 (实际运行需有效 ID)
        # response = requests.post(url, json=payload, headers=common_headers)
        pass

if __name__ == "__main__":
    pytest.main(["-v", "kuaishou_ads_pytest.py"])
