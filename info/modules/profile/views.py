from flask import g, render_template, redirect

from info.modules.profile import profile_blu
from info.utils.common import user_login_data


@profile_blu.route('/info')
@user_login_data
def info():
    user = g.user
    if not user:
        return redirect('/')
    data = {"user":user.to_dict()}
    return render_template('news/user.html', data=data)