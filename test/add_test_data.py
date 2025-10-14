import app.database as db
from sqlalchemy.orm import Session
from sqlalchemy import select
import datetime

def main():
    # 添加了三个测试文章tag
    with Session(db.engine) as session:
        stmt = select(db.ArticleTags)
        result = session.scalars(stmt)
        tags = result.fetchall()
        if len(tags) == 0:
            article_types = [
                db.ArticleTags(article_type_name="测试文章1"),
                db.ArticleTags(article_type_name="测试文章2"),
                db.ArticleTags(article_type_name="测试文章3"),
            ]
            session.add_all(article_types)
            session.commit()
        stmt = select(db.ArticleTags)
        result = session.scalars(stmt)
        tags = result.fetchall()
        print(tags)

    # 添加了三个测试文章
    with Session(db.engine) as session:
        stmt = select(db.Articles)
        result = session.scalars(stmt)
        articles = result.fetchall()
        if len(articles) == 0:
            articles = [
                db.Articles(article_name="第一篇文章",
                            update_time=datetime.datetime.now(),
                            article_cover="There is no cover!",
                            article_abstract="第一篇文章",
                            article_content="## 第一篇第一节",
                            article_tag=tags[0].article_tag_id),
                db.Articles(article_name="第二篇文章",
                            update_time=datetime.datetime.now(),
                            article_cover="There is no cover!",
                            article_abstract="第二篇文章",
                            article_content="## 第二篇第一节",
                            article_tag=tags[1].article_type_id),
                db.Articles(article_name="第三篇文章",
                            update_time=datetime.datetime.now(),
                            article_cover="There is no cover!",
                            article_abstract="第三篇文章",
                            article_content="## 第三篇第一节",
                            article_tag=tags[2].article_type_id),
            ]
            session.add_all(articles)
            session.commit()
        stmt = select(db.Articles)
        result = session.scalars(stmt)
        articles = result.fetchall()
        print(articles)

if __name__ == '__main__':
    main()
