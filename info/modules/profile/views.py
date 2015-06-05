from flask import g, render_template, redirect, request

from info.modules.profile import profile_blu
from info.utils.common import user_login_data


@profile_blu.route('/base_info')
@user_login_data
def base_info():
    user = g.user
    if request.method == "GET":
        return render_template('news/user_base_info.html', data={"user":user.to_dict()})
    # 修改用户数据



@profile_blu.route('/info')
@user_login_data
def info():
    user = g.user
    if not user:
        return redirect('/')
    data = {"user":user.to_dict()}
    return render_template('news/user.html', data=data)