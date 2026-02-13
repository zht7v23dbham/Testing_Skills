import pytest
import requests
import time
import threading

class TestRedPacketCampaign:
    """
    春节红包雨活动接口自动化测试示例
    对应: examples/example_ad_campaign_test.md
    """
    
    BASE_URL = "https://api.example.com/v1"
    
    @pytest.fixture(scope="class")
    def user_token(self):
        # 模拟获取登录 Token
        return "user_token_mock_123"

    def test_claim_redpacket_success(self, user_token):
        """
        [正向测试] 用户首次领取红包成功
        """
        url = f"{self.BASE_URL}/redpacket/claim"
        headers = {"Authorization": f"Bearer {user_token}"}
        payload = {"activity_id": "spring_2025"}
        
        resp = requests.post(url, json=payload, headers=headers)
        
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert resp.json()["data"]["amount"] > 0

    def test_claim_idempotency(self, user_token):
        """
        [幂等性测试] 快速多次点击仅第一次生效
        """
        url = f"{self.BASE_URL}/redpacket/claim"
        headers = {"Authorization": f"Bearer {user_token}"}
        payload = {"activity_id": "spring_2025"}
        
        # 第一次请求
        resp1 = requests.post(url, json=payload, headers=headers)
        
        # 第二次请求
        resp2 = requests.post(url, json=payload, headers=headers)
        
        # 验证逻辑：第一次成功，第二次提示已领取
        if resp1.json()["code"] == 0:
            assert resp2.json()["code"] == 1001 # 假设 1001 为已领取
        else:
            pytest.fail("First request failed unexpectedly")

    def test_concurrency_inventory(self, user_token):
        """
        [并发测试] 模拟并发抢红包 (简化版)
        """
        url = f"{self.BASE_URL}/redpacket/claim"
        headers = {"Authorization": f"Bearer {user_token}"}
        
        def claim():
            requests.post(url, json={"activity_id": "spring_2025"}, headers=headers)
            
        threads = []
        for _ in range(10):
            t = threading.Thread(target=claim)
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
        # 验证库存是否为负 (需调用查库存接口)
        stock_resp = requests.get(f"{self.BASE_URL}/redpacket/stock")
        assert stock_resp.json()["data"]["stock"] >= 0

if __name__ == "__main__":
    pytest.main(["-v", "example_ad_campaign_pytest.py"])
