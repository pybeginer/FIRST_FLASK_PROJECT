from datetime import datetime

from flask import current_app
from flask import session

from Information import db
from flask import request,make_response,jsonify
from . import passport_blueprint
from Information.utils.captcha.captcha import captcha
from Information import redis_store
from Information.libs.response_code import RET
import re
import random
from Information.libs.yuntongxun.sms import CCP
from Information import constants
from Information.models import User


@passport_blueprint.route("/image_code")
def image_code():
    code_id = request.args.get("code_id")

    name,image_msg,image = captcha.generate_captcha()

    print("图片验证码为:" + image_msg)

    redis_store.set("image_code_" + code_id, image_msg, constants.IMAGE_CODE_REDIS_EXPIRES)

    response = make_response(image)

    response.headers["Content-Type"] = "image/jpg"

    return response


@passport_blueprint.route("/sms_code", methods=["POST", "GET"])
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
    # 设置为不区分图片验证码的大小写
    if image_msg.upper() != stored_image.upper():
        return jsonify(errno=RET.PARAMERR, errmsg="验证码输入错误")

    sms_data = random.randint(100000, 999999)
    # 注意需要phone_number的数据类型需要转换-----------------------------------------------
    redis_store.set("sms_id_" + phone_number, sms_data, constants.SMS_CODE_REDIS_EXPIRES)

    print("短信验证码为:%d" % sms_data)

    # sms_ccp = CCP()
    #
    # sms_send_result = sms_ccp.send_template_sms(phone_number, [sms_data, 5], 1)
    #
    # if sms_send_result:
    #     return jsonify(errno=RET.THIRDERR, errmsg="验证码发送失败")

    return jsonify(errno=RET.OK, errmsg="验证码发送成功")


@passport_blueprint.route("/register", methods=["POST", "GET"])
def user_register():
    mob_number = request.json.get("mobile")
    sms_content = request.json.get("smscode")
    user_password = request.json.get("password")
    if not all([mob_number, sms_content, user_password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    smscontent_server = redis_store.get("sms_id_" + mob_number)
    if not smscontent_server:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码已过期")
    print(type(sms_content), type(smscontent_server))
    if smscontent_server != sms_content:
        return jsonify(errno=RET.PARAMERR, errmsg="短信验证码错误")

    user_info = User()
    user_info.nick_name = mob_number
    user_info.mobile = mob_number
    user_info.password = user_password

    user_info.last_login = datetime.now()
    db.session.add(user_info)
    db.session.commit()
    print("注册成功")
    return jsonify(errno=RET.OK, errmsg="注册成功")


@passport_blueprint.route("/login", methods=["POST"])
def user_login():
    login_phone = request.json.get("mobile")
    login_password = request.json.get("password")

    # if not all([login_password, login_phone]):
    #     return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        user = User.query.filter(User.mobile == login_phone).first()
    except Exception as err:
        return current_app.logger.error(err)

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="请注册")

    if not user.check_password(login_password):
        return jsonify(errno=RET.PARAMERR, errmsg="密码错误")

    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile

    user.last_login = datetime.now()
    db.session.commit()
    return jsonify(errno=RET.OK, errmsg="登陆成功")


@passport_blueprint.route("/logout")
def user_logout():
    session.pop("user_id")
    session.pop("nick_name")
    session.pop("mobile")
    return jsonify(errno=RET.OK, errmsg="退出成功")

