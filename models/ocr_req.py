# -*- coding: utf-8 -*-
from fastapi import Query
from pydantic import BaseModel


class OcrImageModel(BaseModel):
    imageBase64: str = Query(..., description="图片BASE64字符串")
    imageType: str = Query(..., description="图片后缀类型")
    text: str = Query(..., description="文本")

