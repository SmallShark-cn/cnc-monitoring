import asyncio
import websockets

# 你要测试的本地WebSocket端点
WS_URL = "ws://192.168.1.101:8000/ws/vibration/time-domain"

async def test_ws():
    async with websockets.connect(WS_URL) as ws:
        print(f"已连接到 {WS_URL}，等待数据...")
        try:
            while True:
                data = await ws.recv()
                print("收到数据：", data)
        except websockets.ConnectionClosed:
            print("连接已关闭")

if __name__ == "__main__":
    asyncio.run(test_ws())