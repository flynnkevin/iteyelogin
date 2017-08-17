#-*- coding: utf-8 -*
__author__ = 'Howie'
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from xlwt import *

class IteyeSpider(Spider):
	name="iteyespider"
	login_page ="http://www.iteye.com/login"
	start_urls = ["http://kevinflynn.iteye.com/",
                  "http://kevinflynn.iteye.com/blog/2281218"]
	
	def start_requests(self):
		return [Request(self.login_page,callback=self.post_login)]
	
	def post_login(self,response):
		authenticity_token=Selector(response).xpath('//input[@name="authenticity_token"]/@value').extract()[0]
		return [FormRequest.from_response(response,
                                          formdata={
                                              'authenticity_token':authenticity_token,
                                              'name':'kevinflynn',
                                              'password':'maoshan2011215858',
                                              'button':'登　录',
                                          },
                                          callback=self.logged_in)]

	def logged_in(self,response):
		return [Request(self.start_urls[0],self.get_page)]

	def get_page(self, response):
		print response.body
		sel=Selector(response)
		titles=sel.xpath('//h3/a/text()').extract()
		for title in titles:
			print title
                yield Request(url="http://gaojingsong.iteye.com/blog/2390198",callback=self.post_commit)

        def post_commit(self,response):
            sel=Selector(response)
            authenticity_token=sel.xpath("//*[@name='authenticity_token']/@value").extract_first()
            commit_url="http://gaojingsong.iteye.com/blog/create_comment/2390198"

            formdata={"comment[body]":"可以，很不错，很不错，点赞！！！","commit":"提交","_":"","authenticity_token":authenticity_token}
            yield FormRequest(url=commit_url,formdata=formdata,callback=self.parse_commit,dont_filter=False)

        def parse_commit(self,response):
            print response.body






