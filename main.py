# -*- coding: utf-8 -*-
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from routers.ocr_router import ocrRouter

app = FastAPI()
app.include_router(ocrRouter)

# 可跨域访问的域名
# origins = [
#     "http://127.0.0.1",
#     "http://127.0.0.1:38080",
# ]
# 可跨域访问的基本请求设置
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=38080, reload=False, debug=True)
