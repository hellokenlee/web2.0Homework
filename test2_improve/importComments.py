# -*- coding: utf-8 -*-
import pymongo
#添加缺省评论函数
all_comment=[
	{"name":"rodney zhang","time":"2013-9-11","content":"理论上StackOverflow在国内成功复制的机会很大，首先中国的程序员数量庞大，更爱好在网络搜索答案，乐于贡献的人也不少；其次国内还没有（个人观察）类似的专业技术问答网站；同时， 在网络上搜索已经越来越不可缺少，程序员对搜索的依赖越来越大，特别是在中国（语言因素），更加需要这样一个平台。"},
	{"name":"ltremMaxwell Lou","time":"2013-9-13","content":"Stackoverflow的确做的是很好，每个tag还有简介，这种体验感觉更加好，因为像这种专业的网站的tag很专业，有个介绍会感觉好一些。"},
	{"name":"lisa zhang","time":"2013-10-1","content":"csdn其实可以做到更多的，可是上面的评论都是在打嘴仗，可笑呀。"},
	{"name":"parsifal yu","time":"2013-10-12","content":"zhang 先生说的很对，stackoverflow 这个平台很好很强大。可说是能促进人的思考。"},
	{"name":"123","time":"2013-11-11","content":"国内复制么? 我现在直接在用Stack Overflow 我承认我很爱面子 每次点上的三角形告诉我Reputation不足时, 我就在心里暗暗发誓我一定要拿到15个Reputation!"}
]

def importData():
    comments.remove()
    for comment in all_comment:
		comments.insert(comment)

def valid():
    for info in comments.find():
        print info

conn=pymongo.Connection("localhost",27017)
db=conn["test2"]
comments=db.comments
importData()
valid()
