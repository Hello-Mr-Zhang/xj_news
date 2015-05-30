from flask import render_template

from info.modules.news import news_blu

@news_blu.route("/<int:news_id>")
def news_detail(news_id):
    data = {
        # TODO 需要传入数据
    }

    return render_template("news/detail.html", data=data)