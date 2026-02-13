from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import logging
import time
import random

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MockServer")

app = FastAPI(title="Ad Attribution Mock Server")

@app.get("/mock/attribution/callback")
async def attribution_callback(click_id: str, event_type: str = "activate"):
    """
    模拟媒体侧接收归因回调
    URL: http://localhost:8000/mock/attribution/callback?click_id=xxx&event_type=activate
    """
    logger.info(f"Received Callback: click_id={click_id}, event={event_type}")
    
    # 模拟随机延迟 (网络抖动)
    time.sleep(random.uniform(0.1, 0.5))
    
    # 模拟随机失败 (测试重试机制)
    if random.random() < 0.1: # 10% 概率失败
        return {"code": 500, "message": "Internal Mock Error"}
        
    return {"code": 0, "message": "success", "data": {"status": "processed"}}

@app.post("/mock/payment/notify")
async def payment_notify(request: Request):
    """
    模拟支付成功异步通知
    """
    body = await request.json()
    logger.info(f"Payment Notify: {body}")
    return "SUCCESS"

if __name__ == "__main__":
    # 启动命令: python mock_server_fastapi.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
