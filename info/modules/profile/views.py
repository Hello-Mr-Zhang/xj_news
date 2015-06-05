from flask import g, render_template, redirect, request, jsonify

from info.modules.profile import profile_blu
from info.utils.common import user_login_data
from info.utils.response_code import RET


@profile_blu.route('/base_info', methods=['get', 'post'])
@user_login_data
def base_info():
    user = g.user
    if request.method == "GET":
        return render_template('news/user_base_info.html', data={"user": user.to_dict()})
    # 修改用户数据
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if gender not in ['WOMAN', 'MAN']:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender

    return jsonify(errno=RET.OK, errmsg="OK")


@profile_blu.route('/info')
@user_login_data
def info():
    user = g.user
    if not user:
        return redirect('/')
    data = {"user": user.to_dict()}
    return render_template('news/user.html', data=data)
