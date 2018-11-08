from flask import request, jsonify
from flask import session

from Information.libs.response_code import RET
from Information.models import User,News,Category
from . import blueprint_objt
from flask import render_template,current_app


@blueprint_objt.route("/")
def homepage():
    user_id = session.get("user_id")
    user = None
    if user_id:
        user = User.query.get(user_id)
    rank_news = News.query.order_by(News.clicks.desc()).limit(10)
    rank_news_list = []
    for news in rank_news:
        rank_news_list.append(news.to_dict())
    cates = Category.query.all()
    cates_list = []
    for cate in cates:
        cates_list.append(cate.to_dict())

    data = {
        "usr_info":user.to_dict() if user else None,
        "ranknews":rank_news_list,
        "cates":cates_list,
    }

    return render_template("news/index.html", data = data)


@blueprint_objt.route("/news_list")
def news_list():
    news_cid = request.args.get("cid", 1)
    news_page = request.args.get("page", 1)
    news_per_page = request.args.get("per_page", 10)
    try:
        news_cid = int(news_cid)
        news_page = int(news_page)
        news_per_page = int(news_per_page)
    except Exception as err:
        news_cid = 1
        news_page = 1
        news_per_page = 10
    filter_list = []
    if news_cid != 1:
        filter_list.append(News.category_id == news_cid)

    paginate_news = News.query.filter(*filter_list).order_by(News.create_time.desc()).paginate(news_page, news_per_page, False)

    items = paginate_news.items
    current_page = paginate_news.page
    total_pages = paginate_news.pages
    news_list = []
    for item in items:
        news_list.append(item.to_dict())
    sour_data = {
        "current_page":current_page,
        "total_page":total_pages,
        "news_dict_li":news_list
    }
    return jsonify(errno=RET.OK, errmsg="ok", data=sour_data)


@blueprint_objt.route("/favicon.ico")
def add_favi():
    return current_app.send_static_file("news/favicon.ico")


