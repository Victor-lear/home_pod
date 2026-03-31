from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "connect_success"}
@app.get("/open_air")
async def root():
    try:
        import gpio
        gpio.click()
        return {"message": "connect_success"}
    except Exception as e:
        # 拼字修正：return，並回傳錯誤訊息方便除錯
        return {"message": "error", "detail": str(e)}
@app.get("/open_light")
async def root():
    try:
        import gpio
        gpio.socketsub()
        return {"message": "connect_success"}
    except Exception as e:
        # 拼字修正：return，並回傳錯誤訊息方便除錯
        return {"message": "error", "detail": str(e)}