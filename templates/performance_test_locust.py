from locust import HttpUser, task, between, events
import logging

class AdvertisingUser(HttpUser):
    """
    广告业务性能测试脚本 (Locust)
    模拟场景：大量用户浏览广告(高频) -> 少量用户点击广告(低频) -> 极少用户转化(极低频)
    """
    
    # 模拟用户在两个操作之间的思考时间 (秒)
    wait_time = between(0.5, 2.0)
    
    def on_start(self):
        """用户初始化：例如登录获取 Token"""
        # self.client.post("/login", json={"username":"test"})
        pass

    @task(100) # 权重 100: 曝光是最高频的操作
    def view_ad_impression(self):
        with self.client.get("/api/v1/ad/impression", params={"ad_id": "1001"}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Impression failed: {response.status_code}")

    @task(5) # 权重 5: 点击率通常较低 (如 5%)
    def click_ad(self):
        self.client.post("/api/v1/ad/click", json={"ad_id": "1001", "click_id": "uuid_123"})

    @task(1) # 权重 1: 转化率最低 (如 1%)
    def convert_ad(self):
        self.client.post("/api/v1/ad/conversion", json={"click_id": "uuid_123", "event": "purchase"})

# 运行命令: locust -f performance_test_locust.py --host=https://test-api.example.com
