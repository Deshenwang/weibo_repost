# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from www.items import *
import json,time
import  pymongo
from www.settings import LOCAL_MONGO_HOST,LOCAL_MONGO_PORT,DB_NAME


class WwSpider(scrapy.Spider):
    name = 'ww'
    allowed_domains = ['m.weibo.cn']

    # # start_urls = ['http://m.weibo.cn/']
    # user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    #
    # follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    #
    # fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'
    # fans_profile_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&lfid=107603{uid}&type=uid&value={uid}&containerid=230283{uid}'
    #
    # weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    #
    # start_users = ['5647863244','2282991915']
    # # '1742566624', '2282991915', '1288739185', '3952070245', '5878659096'
    #
    # def start_requests(self):
    #     for uid in self.start_users:
    #         yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
    #
    # def parse_user(self, response):
    #     """
    #     解析用户信息
    #     :param response: Response对象
    #     """
    #     self.logger.debug(response)
    #     result = json.loads(response.text)
    #     if result.get('data').get('userInfo'):
    #         user_info = result.get('data').get('userInfo')
    #         user_item = UserItem()
    #         field_map = {
    #             'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
    #             'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
    #             'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
    #             'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
    #         }
    #         for field, attr in field_map.items():
    #             user_item[field] = user_info.get(attr)
    #         yield user_item
    #         # 关注
    #         uid = user_info.get('id')
    #         yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follows,
    #                       meta={'page': 1, 'uid': uid})
    #         # 粉丝
    #         yield Request(self.fan_url.format(uid=uid, page=1), callback=self.parse_fans,
    #                       meta={'page': 1, 'uid': uid})
    #         # 微博
    #         # yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
    #         #               meta={'page': 1, 'uid': uid})
    #
    # def parse_follows(self, response):
    #     """
    #     解析用户关注
    #     :param response: Response对象
    #     """
    #     result = json.loads(response.text)
    #     if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
    #             result.get('data').get('cards')[-1].get(
    #                 'card_group'):
    #         # 解析用户
    #         follows = result.get('data').get('cards')[-1].get('card_group')
    #         # for follow in follows:
    #         #     if follow.get('user'):
    #         #         uid = follow.get('user').get('id')
    #         #         yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
    #
    #         for follow in follows:
    #
    #                 uid = response.meta.get('uid')
    #                 follow_uid = follow.get('user').get('id')
    #                 desc1 = follow.get('desc1')
    #                 screen_name = follow.get('user').get('screen_name')
    #                 followers_count = follow.get('user').get('followers_count')
    #                 follow_count =  follow.get('user').get('follow_count')
    #                 gender = follow.get('user').get('gender')
    #                 meta = {'uid': uid,
    #                         'follow_uid': follow_uid,
    #                         'screen_name':screen_name,
    #                         'followers_count': followers_count,
    #                         'follow_count':follow_count,
    #                         'gender':gender,
    #                         'desc1':desc1,
    #                         }
    #                 yield Request(self.fans_profile_url.format(uid=follow_uid), meta=meta,callback=self.parse_follow_profile)
    #         # 下一页关注
    #         page = response.meta.get('page') + 1
    #         yield Request(self.follow_url.format(uid=uid, page=page),
    #                       callback=self.parse_follows, meta={'page': page, 'uid': uid})
    # def parse_follow_profile(self,response):
    #     result = json.loads(response.text)
    #
    #     if result.get('ok'):
    #         if result.get('data').get('cards')[1].get('card_group'):
    #             follow = result.get('data').get('cards')[1].get('card_group')
    #             item_content = follow[1].get('item_content')
    #             item_company = follow[2].get('item_content')#时间
    #         else:
    #             item_company = None
    #             item_content = None
    #         follow_item = FollowItem()
    #         follow_item['id'] = response.meta.get('uid') #目标用户
    #         follow_item['follow_uid'] = response.meta.get('follow_uid')#被关注人
    #         follow_item['screen_name'] = response.meta.get('screen_name')
    #         follow_item['followers_count'] = response.meta.get('followers_count')
    #         follow_item['follow_count'] = response.meta.get('follow_count')
    #         follow_item['gender'] = response.meta.get('gender')
    #         follow_item['content'] = item_content
    #         follow_item['regist_time'] = item_company
    #         follow_item['desc1'] = response.meta.get('desc1')
    #         yield follow_item
    #
    # def parse_fans(self, response):
    #     """
    #     解析用户粉丝
    #     :param response: Response对象
    #     """
    #     result = json.loads(response.text)
    #     if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
    #             result.get('data').get('cards')[-1].get(
    #                 'card_group'):
    #         # 解析用户
    #         fans = result.get('data').get('cards')[-1].get('card_group')
    #         # for fan in fans:
    #         #     if fan.get('user'):
    #         #         uid = fan.get('user').get('id')
    #         #         yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
    #
    #
    #         for fan in fans:
    #             if fan.get('user'):
    #                 uid = response.meta.get('uid')
    #                 desc1 = fan.get('desc1')
    #                 fans_uid = fan.get('user').get('id')
    #                 screen_name = fan.get('user').get('screen_name')
    #                 followers_count = fan.get('user').get('followers_count')
    #                 follow_count =  fan.get('user').get('follow_count')
    #                 gender = fan.get('user').get('gender')
    #                 meta = {'uid': uid,
    #                         'fans_uid': fans_uid,
    #                         'screen_name':screen_name,
    #                         'followers_count': followers_count,
    #                         'follow_count':follow_count,
    #                         'gender':gender,
    #                         'desc1':desc1,
    #                         }
    #                 yield Request(self.fans_profile_url.format(uid=fans_uid), meta=meta,callback=self.parse_fans_profile)
    #
    #         # 粉丝列表
    #         # user_relation_item = UserRelationItem()
    #         # fans = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in
    #         #         fans]
    #         # user_relation_item['id'] = uid
    #         # user_relation_item['fans'] = fans
    #         # user_relation_item['follows'] = []
    #         # yield user_relation_item
    #         # 下一页粉丝
    #         page = response.meta.get('page') + 1
    #         yield Request(self.fan_url.format(uid=uid, page=page),
    #                       callback=self.parse_fans, meta={'page': page, 'uid': uid})
    #         #
    #         # def parse_weibos(self, response):
    #         #     """
    #         #     解析微博列表
    #         #     :param response: Response对象
    #         #     """
    #         #     result = json.loads(response.text)
    #         #     if result.get('ok') and result.get('data').get('cards'):
    #         #         weibos = result.get('data').get('cards')
    #         #         for weibo in weibos:
    #         #             mblog = weibo.get('mblog')
    #         #             if mblog:
    #         #                 weibo_item = WeiboItem()
    #         #                 field_map = {
    #         #                     'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
    #         #                     'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
    #         #                     'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
    #         #                     'thumbnail': 'thumbnail_pic',
    #         #                 }
    #         #                 for field, attr in field_map.items():
    #         #                     weibo_item[field] = mblog.get(attr)
    #         #                 weibo_item['user'] = response.meta.get('uid')
    #         #                 yield weibo_item
    #         #         # 下一页微博
    #         #         uid = response.meta.get('uid')
    #         #         page = response.meta.get('page') + 1
    #         #         yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
    #         #                       meta={'uid': uid, 'page': page})
    #
    # def parse_fans_profile(self,response):
    #     result = json.loads(response.text)
    #
    #     if result.get('ok'):
    #         if result.get('data').get('cards')[1].get('card_group'):
    #             fans = result.get('data').get('cards')[1].get('card_group')
    #             item_content = fans[1].get('item_content')
    #             item_company = fans[2].get('item_content')#时间
    #         else:
    #             item_content = None
    #             item_company = None
    #         fans_item = FansItem()
    #         fans_item['id'] = response.meta.get('uid') #目标用户
    #         fans_item['fans_uid'] = response.meta.get('fans_uid')#粉
    #         fans_item['screen_name'] = response.meta.get('screen_name')
    #         fans_item['followers_count'] = response.meta.get('followers_count')
    #         fans_item['follow_count'] = response.meta.get('follow_count')
    #         fans_item['gender'] = response.meta.get('gender')
    #         fans_item['desc1'] = response.meta.get('desc1')
    #         fans_item['content'] = item_content
    #         fans_item['regist_time'] = item_company
    #         yield fans_item




    '''
    下面是迭代爬取某个微博的多次转发数

    '''


    name = "weib"
    allowed_domains = ["m.weibo.cn"]
    #在start_requests方法中构建urlhttps://m.weibo.cn/detail/4293673170086168#repost
    def start_requests(self):
        #此处的id为该条微博的id，转发后id会不一样
        # user_id = '4293673170086168'
        #user_id = '4354920570387426'
        user_id = '4347534971443204'#杜蕾斯

        level_count = 1
        url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=4347534971443204&page=1'
        # 通过上方的url，爬取到该条微博转发的页数
        # 如果能成功连接就进行请求
        yield scrapy.Request(url, meta={'id': user_id,'level_count':level_count}, callback=self.parse, dont_filter=True)
        #由于接下来的url需要微博id，所以用meta携带id
    def parse(self, response):
        curPage = response.body
        content = json.loads(curPage)   #对爬取到的页面，进行转json的处理
        data = content.get("data")
        if data:
            count = data.get("max")
            print(count)# 本层次微博的转发数
            id = response.meta.get('id')        #将id从meta中取出
            level_count = response.meta.get('level_count')        #将id从meta中取出
            for i in range(1,count + 1):
                weibo_Repost_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={id}'.format(id=id) +'&page=' +str(i)
            #构建每页评论的url
                yield  scrapy.Request(weibo_Repost_url, callback=self.get_weibo_repost,meta={'id':id,'level_count':level_count})
    def get_weibo_repost(self, response):
        # 爬取所需要的数据
        curPage = response.body
        # \n是正常时回车，\r是win下的回车，这是防止有些微博里有换行而存入时不规整设计的
        content = json.loads(curPage)
        datas = content.get('data')
        data = datas.get('data')
        for i in range(0, len(data)):
            weiboItem = DiedaiItem()
            weiboItemdata = data[i]
            #获取转发时附带的文本，
            text = weiboItemdata.get('text')
            level_count = response.meta.get('level_count')
            a = level_count - 1
            if a is not text.count("//<a"):
                pass
            else:
                weiboItem['text'] = weiboItemdata.get('text')  # 转发时的文字内容
                weiboItem['level_count'] = level_count
            # weiboItem['time'] = self.time_form(weiboItemdata.get('created_at').encode('utf-8'))   # 转发博文的发布时间
                weiboItem['sourceid'] = response.meta.get('id')
                uid = weiboItemdata.get('id')
                weiboItem['currentid'] = uid  # 转发后的微博的ID
                weiboItem['time'] = weiboItemdata.get('created_at')
                weiboItem['source'] = weiboItemdata.get('source')
                weiboUser = weiboItemdata.get('user')
                weiboItem['Id'] =  weiboUser.get('id')                # 转发人的id
                weiboItem['Name'] = weiboUser.get('screen_name')      # 转发人的昵称
                weiboItem['Url'] = weiboUser.get('profile_url')  # 转发人的url
                weiboItem['gender'] = weiboUser.get('gender')  # 转发人的url

                # print u'正在处理第 %d 条微博：  %s  %s' % (i, weiboItem['reTime'], str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
                yield weiboItem
                #查看此微博的层次sourceid
                level_count = level_count + 1
                url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={uid}&page=1'
                yield scrapy.Request(url.format(uid=uid), meta={'id': uid,'level_count':level_count}, callback=self.parse)
    # def time_form(self, time_str):
    #     if '刚刚' in time_str:
    #         real_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    #         return real_time
    #     elif '分钟' in time_str:
    #         time_str = time_str.split('分钟')
    #         seconds = int(time_str[0]) * 60
    #         real_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - seconds))
    #         return real_time
    #     elif '小时' in time_str:
    #         time_str = time_str.split('小时')
    #         seconds = int(time_str[0]) * 60 * 60
    #         real_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - seconds))
    #         return real_time
    #     elif '今天' in time_str:
    #         time_str = time_str.split('今天')
    #         today = time_str[1]
    #         real_time = time.strftime('%Y-%m-%d', time.localtime(time.time())) + today
    #         return real_time
    #     elif '昨天' in time_str:
    #         time_str = time_str.split('昨天')
    #         yesterday = time_str[1]
    #         real_time = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60)) + yesterday
    #         return real_time
    #     elif len(time_str) == 5:
    #         real_time = time.strftime('%Y-', time.localtime(time.time())) + time_str
    #         return real_time
    #     else:
    #         real_time = time_str
    #         return real_time
    #









2




