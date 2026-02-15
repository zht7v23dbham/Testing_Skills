import streamlit as st
import requests
import json
import diff_match_patch as dmp_module
from typing import Dict, Any, Optional

def fetch_api(url: str, method: str = "GET", payload: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
    """
    通用 API 请求函数
    Args:
        url: 目标 URL
        method: HTTP 方法
        payload: 请求体
        headers: 请求头
    Returns:
        JSON 响应数据或错误信息
    """
    try:
        if method == "GET":
            resp = requests.get(url, params=payload, headers=headers)
        else:
            resp = requests.post(url, json=payload, headers=headers)
        return {"status": resp.status_code, "data": resp.json(), "time": resp.elapsed.total_seconds()}
    except Exception as e:
        return {"error": str(e)}

def main():
    st.set_page_config(page_title="API Diff Tool", layout="wide")
    st.title("🔍 API 响应对比工具 (QA Expert Edition)")
    
    st.sidebar.header("配置")
    method = st.sidebar.selectbox("Method", ["GET", "POST"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("环境 A (基准)")
        url_a = st.text_input("URL A", placeholder="https://prod-api.example.com/v1/user")
        
    with col2:
        st.subheader("环境 B (测试)")
        url_b = st.text_input("URL B", placeholder="https://test-api.example.com/v1/user")
        
    params = st.text_area("请求参数 (JSON)", value="{}", height=100)
    
    if st.button("🚀 开始对比", use_container_width=True):
        try:
            payload = json.loads(params)
        except json.JSONDecodeError:
            st.error("JSON 格式错误")
            return

        with st.spinner("Requesting..."):
            res_a = fetch_api(url_a, method, payload)
            res_b = fetch_api(url_b, method, payload)
            
        # 展示结果
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Status A", res_a.get("status", "Error"))
            st.json(res_a, expanded=True)
            
        with c2:
            st.metric("Status B", res_b.get("status", "Error"), delta_color="inverse")
            st.json(res_b, expanded=True)
            
        # 对比逻辑
        st.divider()
        st.subheader("📊 差异分析")
        
        if res_a == res_b:
            st.success("✅ 响应完全一致")
        else:
            st.error("❌ 发现差异")
            # 简单展示差异字段 (实际项目可引入 deepdiff)
            st.code(f"A: {res_a}\nB: {res_b}", language="json")

if __name__ == "__main__":
    main()
