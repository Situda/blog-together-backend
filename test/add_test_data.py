import app.database as db
from sqlalchemy.orm import Session
from sqlalchemy import select
import datetime

import app.models.article


def main():
    # 添加了三个测试文章category
    with Session(db.engine) as session:
        stmt = select(app.models.article.ArticleCategories)
        result = session.scalars(stmt)
        categories = result.fetchall()
        if len(categories) == 0:
            article_categories = [
                app.models.article.ArticleCategories(article_category_name="测试文章1"),
                app.models.article.ArticleCategories(article_category_name="测试文章2"),
                app.models.article.ArticleCategories(article_category_name="测试文章3"),
            ]
            session.add_all(article_categories)
            session.commit()
        stmt = select(app.models.article.ArticleCategories)
        result = session.scalars(stmt)
        categories = result.fetchall()
        print(categories)

    # 添加了三个测试文章
    with Session(db.engine) as session:
        stmt = select(app.models.article.Articles)
        result = session.scalars(stmt)
        articles = result.fetchall()
        if len(articles) == 0:
            articles = [
                app.models.article.Articles(article_title="第一篇文章",
                                            update_time=datetime.datetime.now(),
                                            article_cover="There is no cover!",
                                            article_abstract="第一篇文章",
                                            article_content="## 第一篇第一节",
                                            article_category=categories[0].article_category_id),
                app.models.article.Articles(article_title="第二篇文章",
                                             update_time=datetime.datetime.now(),
                                             article_cover="There is no cover!",
                                             article_abstract="第二篇文章",
                                             article_content="## 第二篇第一节",
                                             article_category=categories[1].article_category_id),
                app.models.article.Articles(article_title="第三篇文章",
                                             update_time=datetime.datetime.now(),
                                             article_cover="There is no cover!",
                                             article_abstract="第三篇文章",
                                             article_content="## 第三篇第一节",
                                             article_category=categories[2].article_category_id),
            ]
            session.add_all(articles)
            session.commit()
        stmt = select(app.models.article.Articles)
        result = session.scalars(stmt)
        articles = result.fetchall()
        print(articles)

if __name__ == '__main__':
    main()
