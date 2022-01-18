# -*- coding: utf-8 -*-
import base64
import datetime
import difflib
import os

from fastapi import APIRouter
from paddleocr import PaddleOCR

from models.ocr_req import OcrImageModel

ocrRouter = APIRouter(prefix="/ocr", tags=['ocr'])
# # Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
# ocr = PaddleOCR(use_angle_cls=True, lang='ch')
# project_path = os.path.abspath(__file__).split("routers")[0]
# ocr = PaddleOCR(det_model_dir=os.path.join(project_path, "inference", "ch_ppocr_det_infer"),
#                 rec_model_dir=os.path.join(project_path, "inference", "ch_ppocr_rec_infer"),
#                 cls_model_dir=os.path.join(project_path, "inference", "ch_ppocr_cls_infer"),
#                 use_angle_cls=True, lang='ch', use_gpu=False, use_space_char=False)
ocr = PaddleOCR(use_angle_cls=True, lang='ch')


@ocrRouter.post("/image/coordinates")
async def get_coordinates_by_text(req: OcrImageModel):
    try:
        text_coordinates = get_coordinates(req.imageBase64, req.imageType, req.text)
        if text_coordinates and text_coordinates[0]:
            return {"code": 0, "msg": "成功",
                    "data": {"match_text": text_coordinates[0], "x": text_coordinates[1], "y": text_coordinates[2]}}
        else:
            return {"code": 1, "msg": "识别错误!"}
    except Exception as e:
        return {"code": 2, "msg": "识别异常!" + str(e)}


def get_coordinates(img_base64: str, img_type: str, text: str) -> []:
    """
    识别图片中相似度最高的文本坐标，坐标为文本所在BOX的中心坐标
    :param img_type:  图片后缀
    :param img_base64: 图片BASE64字符串
    :param text:  文本
    :return:[]
    """
    if not img_base64 or not img_type or not text:
        return []
    x, y, max_match_rate, match_text = 0, 0, 0, ""
    img_file = os.path.join(os.path.abspath(__file__).split("routers")[0], "tmp",
                            datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "." + img_type.lower())
    img_data = base64.b64decode(img_base64)
    with open(img_file, "wb") as f:
        f.write(img_data)
    contents = ocr.ocr(img_file, cls=True)
    for content in contents:
        temp_match_rate = difflib.SequenceMatcher(None, content[1][0], text).quick_ratio()
        if temp_match_rate > max_match_rate:
            max_match_rate = temp_match_rate
            x, y, match_text = 0, 0, content[1][0]
            for coordinate in content[0]:
                x += coordinate[0]
                y += coordinate[1]
    os.remove(img_file)
    return [match_text, x / 4, y / 4]
