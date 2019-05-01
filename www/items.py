# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class UserItem(Item):
    id = Field()
    name = Field()
    avatar = Field()
    cover = Field()
    gender = Field()
    description = Field()
    fans_count = Field()
    follows_count = Field()
    weibos_count = Field()
    verified = Field()
    verified_reason = Field()

    verified_type = Field()

    follows = Field()
    fans = Field()
    crawled_at = Field()


class UserRelationItem(Item):

    id = Field()
    follows = Field()

    fans = Field()
class FansItem(Item):
    id = Field()

    fans_uid = Field()
    screen_name = Field()
    followers_count = Field()
    follow_count = Field()
    gender = Field()
    content = Field()
    regist_time = Field()
    desc1 = Field()
class FollowItem(Item):
    id = Field()

    follow_uid = Field()
    screen_name = Field()
    followers_count = Field()
    follow_count = Field()
    gender = Field()
    content = Field()
    regist_time = Field()
    desc1 = Field()


class WeiboItem(Item):


    id = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()

    picture = Field()
    pictures = Field()
    source = Field()
    text = Field()
    raw_text = Field()
    thumbnail = Field()
    user = Field()
    created_at = Field()
    crawled_at = Field()

class DiedaiItem(Item):
    sourceid = Field()
    currentid = Field()
    text = Field()
    time = Field()
    Id = Field()
    Name = Field()
    Url = Field()
    source = Field()
    gender = Field()
    level_count = Field()

