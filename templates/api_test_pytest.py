import pytest
import requests

class TestApiExample:
    """
    接口自动化测试模板 (Python + Pytest + Requests)
    覆盖九大测试维度示例
    """
    
    BASE_URL = "https://api.example.com"
    
    @pytest.fixture(scope="class")
    def auth_token(self):
        """
        前置条件：获取认证 Token
        """
        # 实际项目中应调用登录接口获取
        return "mock_token_12345"

    def test_positive_scenario(self, auth_token):
        """
        [正向测试] 正常业务流程
        维度覆盖: 1.正向测试, 5.权限与认证
        """
        url = f"{self.BASE_URL}/api/resource"
        headers = {"Authorization": f"Bearer {auth_token}"}
        payload = {"name": "test_item", "quantity": 1}
        
        # 发送请求
        response = requests.post(url, json=payload, headers=headers)
        
        # 断言状态码
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        
        # 断言响应数据结构
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["name"] == "test_item"
        
        # 断言数据一致性 (维度 8)
        # assert db.query("select name from items where id=...", ...) == "test_item"

    @pytest.mark.parametrize("invalid_param", [
        None,           # 维度 3: 边界值 (Null)
        "",             # 维度 3: 边界值 (Empty)
        "a" * 1000,     # 维度 3: 边界值 (超长字符串)
        -1              # 维度 3: 边界值 (负数)
    ])
    def test_boundary_values(self, auth_token, invalid_param):
        """
        [边界值测试] 验证参数边界
        维度覆盖: 2.逆向测试, 3.边界值测试
        """
        url = f"{self.BASE_URL}/api/resource"
        headers = {"Authorization": f"Bearer {auth_token}"}
        payload = {"quantity": invalid_param}
        
        response = requests.post(url, json=payload, headers=headers)
        
        # 预期失败或特定错误码
        assert response.status_code in [400, 422]

    def test_idempotency(self, auth_token):
        """
        [幂等性测试] 重复提交不应产生副作用
        维度覆盖: 6.幂等性测试
        """
        url = f"{self.BASE_URL}/api/resource"
        headers = {"Authorization": f"Bearer {auth_token}"}
        payload = {"id": 1001, "action": "update"}
        
        # 第一次请求
        resp1 = requests.post(url, json=payload, headers=headers)
        assert resp1.status_code == 200
        
        # 第二次请求 (相同参数)
        resp2 = requests.post(url, json=payload, headers=headers)
        assert resp2.status_code == 200 # 或根据业务逻辑返回 "已处理"
        
        # 验证数据未被重复修改

if __name__ == "__main__":
    pytest.main(["-v", "api_test_template.py"])
