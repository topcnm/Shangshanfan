# coding=utf-8
from flask_script import Manager
from webapp.extension import db
from webapp.model import Tag


InitManager = Manager()

tags = [
    {
        'title': '美丽成都',
        'remark': '成都，简称蓉，别称蓉城、锦城，是四川省省会，西南地区唯一一个副省级市，\
                    特大城市，国家重要的高新技术产业基地、商贸物流中心和综合交通枢纽，\
                    西部地区重要的中心城市'
    },
    {
        'title': '小城铜梁',
        'remark': '铜梁区位于长江上游地区、 重庆西部、重庆大都市区、城市发展新区，\
                    是中国人民志愿军特等功臣邱少云的故乡和铜梁龙灯的发祥地。\
                    铜梁区西南靠大足区，东北连合川区，南接永川区，西北邻潼南区，东南毗邻璧山区。',
    },
    {
        'title': '江南诸暨',
        'remark': '诸暨位于浙江省中北部，北邻杭州，东接绍兴，南临义乌。\
                    诸暨历史悠久、人文荟萃，是越国故地、西施故里，\
                    诸暨为古越民族聚居地之一、越王勾践图谋复国之所'
    },
    {
        'title': '旅行日记',
        'remark': '去外地行走。不同于旅游。旅行和旅游的区别就在于：\
                    旅行是在观察身边的景色和事物，行万里路，读万卷书，相对于是指个人，是行走。\
                    旅游是指游玩，通常是团体出行，在时间上是很短暂的。',
    }
]


@InitManager.command
def init_tag():
    for tag in tags:
        db.session.add(Tag(title=tag['title'], remark=tag['remark']))
    db.session.commit()
