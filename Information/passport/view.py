
from flask import request,make_response,jsonify
from . import passport_blueprint
from Information.utils.captcha.captcha import captcha
from Information import redis_store
from Information.libs.response_code import RET
import re


@passport_blueprint.route("/image_code")
def image_code():
    code_id = request.args.get("code_id")

    name,image_msg,image = captcha.generate_captcha()

    redis_store.set("image_code_" + code_id, image_msg, 300)

    response = make_response(image)

    response.headers["Content-Type"] = "image/jpg"

    return response


@passport_blueprint.route("/sms_code", method=["POST", "GET"])
def sms_send():
    phone_number = request.json.get("mobile")
    image_msg = request.json.get("image_code")
    image_id = request.json.get("image_code_id")

    if not all([phone_number, image_msg, image_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="请输入参数")

    if not re.match("1[3456789]\d{9}", phone_number):
        return jsonify(errno=RET.PARAMERR, errmsg="请输入正确的手机号")

    stored_image = redis_store.get("image_code_" + image_id)
    if not stored_image:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已经过期")

    if image_msg != stored_image:
        return jsonify(errno=RET.PARAMERR, errmsg="验证码输入错误")




