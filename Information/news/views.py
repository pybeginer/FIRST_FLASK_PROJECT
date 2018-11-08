from flask import render_template,request
from Information.models import News
from . import news_bluprt


@news_bluprt.route("/<int:news_id>")
def news_detail(news_id):
    # news_id = request.args.get("news_id")
    news_content = News.query.get(news_id)
    news_items = news_content.to_dict()

    data_sour = {
        "news":news_items
    }
    return render_template("news/detail.html", data=data_sour)
