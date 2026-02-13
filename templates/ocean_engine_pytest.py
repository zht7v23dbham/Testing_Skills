import pytest
import requests
import time
import json

class TestOceanEngineAPI:
    """
    巨量引擎 Marketing API 接口自动化测试模板 (Python + Pytest)
    适配 v3.0 新版架构 (Project -> Promotion)
    """
    
    # 巨量引擎 API 地址
    BASE_URL = "https://api.oceanengine.com/open_api/v3.0"
    
    # 你的开发者 Access Token
    ACCESS_TOKEN = "YOUR_OCEAN_ACCESS_TOKEN"
    ADVERTISER_ID = 12345678 # 广告主 ID
    
    @pytest.fixture(scope="class")
    def common_headers(self):
        """
        公共请求头: 巨量引擎使用 Access-Token
        """
        return {
            "Content-Type": "application/json",
            "Access-Token": self.ACCESS_TOKEN
        }

    def test_get_project_list(self, common_headers):
        """
        [正向测试] 获取推广项目列表
        覆盖维度: 1.正向测试, 5.权限与认证
        """
        url = f"{self.BASE_URL}/project/list/"
        params = {
            "advertiser_id": self.ADVERTISER_ID,
            "page": 1,
            "page_size": 10
        }
        
        response = requests.get(url, params=params, headers=common_headers)
        
        assert response.status_code == 200, f"HTTP Error: {response.status_code}"
        data = response.json()
        
        # 巨量引擎成功状态码为 0
        assert data["code"] == 0, f"API Error: {data.get('message')}"
        assert "list" in data["data"]

    def test_create_project_budget_boundary(self, common_headers):
        """
        [边界值测试] 创建项目 - 预算低于最小值
        覆盖维度: 3.边界值测试, 9.业务逻辑约束
        """
        url = f"{self.BASE_URL}/project/create/"
        payload = {
            "advertiser_id": self.ADVERTISER_ID,
            "operation_type": "CREATE",
            "landing_type": "APP",
            "name": f"Test_Budget_Low_{int(time.time())}",
            "marketing_goal": "VIDEO_AND_IMAGE",
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": 10 # 极低预算，通常要求 >= 300 或 1000
        }
        
        response = requests.post(url, json=payload, headers=common_headers)
        data = response.json()
        
        # 预期失败
        assert data["code"] != 0
        print(f"Expected Error: {data.get('message')}")

    def test_qianchuan_campaign_create(self, common_headers):
        """
        [场景测试] 巨量千川 - 创建计划 (注意千川接口前缀不同)
        覆盖维度: 4.参数组合测试
        """
        # 千川 API 通常有独立的前缀或版本
        qc_url = "https://api.oceanengine.com/open_api/v1.0/qianchuan/campaign/create/"
        
        payload = {
            "advertiser_id": self.ADVERTISER_ID,
            "marketing_goal": "LIVE_PROM_GOODS", # 直播带货
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": 300
        }
        
        # 模拟请求
        # response = requests.post(qc_url, json=payload, headers=common_headers)
        pass

if __name__ == "__main__":
    pytest.main(["-v", "ocean_engine_pytest.py"])
