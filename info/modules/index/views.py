from flask import render_template, current_app, session, request, jsonify

from info.models import User, News
from info.utils.response_code import RET
from . import index_blu
from info import redis_store, constants


@index_blu.route('/')
def index():
    # print("im in")
    # session["name"] = "xses"
    # 测试打印日志
    # logging.debug("debug")
    # logging.warning("warning")
    # logging.error("error")
    # logging.fatal("fatal")
    # current_app.logger.error("error")
    # 向redis中保存数据
    # redis_store.set("name", "xses")
    # return "index"
    user_id = session.get('user_id', None)
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    # 右侧新闻排行逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)
    news_dict_li = []
    # 遍历对象列表，将对象的字典添加到字典列表中
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())
    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li
        # TODO 需要查询category返回给前端  category_li
    }
    return render_template("news/index.html", data=data)


@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')


@index_blu.route('/news_list')
def news_list():
    # 1.获取参数
    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")
    # 2.校验参数
    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数不正确")
    # 查询条件
    filters = []
    if cid != 1:
        filters.append(News.category_id == cid)
    # 3.查询数据
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    # 取到当前页的数据
    news_model_list = paginate.items
    total_page = paginate.pages
    current_page = paginate.page
    # paginate.page
    # paginate.pages
    # paginate.items
    # 将模型对象列表转成字典内容
    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())
    data = {
        "total_page": total_page,
        "current_page": current_page,
        "news_dict_li": news_dict_li
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=data)
