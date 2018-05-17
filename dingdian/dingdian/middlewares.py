# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random

class MyUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self,agents):
        self.agents =agents

    @classmethod
    def from_crawler(cls, crawler):
        #代理__init()__初始化方法
        return cls(
            agents=crawler.settings.get('USER_AGENTS')
        )

    def process_request(self, request, spider):
        '''
            此方法在request被scrapy引擎调度给Downloader之前被调用
        :param request: 是Request对象，即被处理的Request
        :param spider:是Spdier对象，即此Request对应的Spider
        :return:当返回值时None时，scrapy将继续处理该request，接着执行其他的Downloader
        Middleware的process_request()方法，一直到Downloader把Request执行后得到Response才结束。
        这个过程其实就是修改Request的过程，不同的Downloader Middleware按照设置的优先级顺序依次对
        Request进行修改，最后送至Downloader执行；

        当返回为Response对象时，更低优先级的Downloader Middleware的process_request()和
        process_exception()方法就不会被继续调用，每个Downloader Middleware的process_response()
        方法转而被依次调用。调用完毕之后，直接将Response对象发送给Spider来处理；

        当返回为Request对象时，更低优先级的Downloader Middleware的process_request()方法会停止执行。
        这个Request会重新放到调度队列里，其实它就是一个全新的Request，等待被调度。如果被Scheduler调度了，
        那么所有的Downloader Middleware的process_request()方法会被重新按照顺序执行；

        如果IgnoreRequest异常抛出，则所有的Downloader Middleware的process_exception()方法会依次执行。
        如果没有一个方法处理这个异常，那么Request的errorback()方法就会回调。如果该异常还没有被处理，那么它便会被忽略。
        '''

        agent = random.choice(self.agents)
        request.headers['User-Agent'] = agent
        #print(request.headers)

    #def process_response(self, request, response, spider):
        '''
        Downloader执行Request下载之后，会得到对应的Response。Scrapy引擎便会将Response发送给Spider进行解析。在发送之前，
        我们都可以用process_response()方法来对Response进行处理
        :param request:是Request对象，即此Response对应的Request。
        :param response:是Response对象，即此被处理的Response。
        :param spider:是Spider对象，即此Response对应的Spider。
        :return:当返回为Request对象时，更低优先级的Downloader Middleware的process_response()方法不会继续调用。
        该Request对象会重新放到调度队列里等待被调度，它相当于一个全新的Request。然后，该Request会被process_request()方法顺次处理。

        当返回为Response对象时，更低优先级的Downloader Middleware的process_response()方法会继续调用，继续对该Response对象进行处理。

        如果IgnoreRequest异常抛出，则Request的errorback()方法会回调。如果该异常还没有被处理，那么它便会被忽略
        '''
        #pass
        #response.status = 201
        #print(response.status)
        #return response
