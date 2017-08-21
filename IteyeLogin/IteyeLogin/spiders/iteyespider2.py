#-*- coding: utf-8 -*
__author__ = 'Howie'
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from xlwt import *
import re
class IteyeSpider(Spider):
        download_delay=3
        name="iteye_spider2"

	login_page ="http://www.iteye.com/login"

	headers={
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
                "Upgrade-Insecure-Requests":"1",
        }

	def start_requests(self):
                return [Request(self.login_page,callback=self.post_login)]
	
	def post_login(self,response):
		authenticity_token=Selector(response).xpath('//input[@name="authenticity_token"]/@value').extract()[0]
		print authenticity_token
		return [FormRequest.from_response(response,
                                          formdata={
                                              'authenticity_token':authenticity_token,
                                              'name':'youngzil',
                                              'password':'nicai@123',
                                              'button':'登　录',
                                          },headers=self.headers,
                                          callback=self.logged_in,dont_filter=True)]

	def logged_in(self,response):
		return [Request(url="http://zhoumeng87.iteye.com/blog/2390493",headers=self.headers,callback=self.post_commit)]

	def post_commit(self,response):
	    sel=Selector(response)
            authenticity_token=sel.xpath("//*[@name='authenticity_token']/@value").extract_first()
            print authenticity_token
	    commit_url="http://zhoumeng87.iteye.com/blog/create_comment/2390493"
	    formdata={"comment[body]":"可以，点赞，很不错，很不错，点赞！！！","commit":"提交","_":"","authenticity_token":authenticity_token}
            yield FormRequest(url=commit_url,formdata=formdata,callback=self.parse_commit,dont_filter=True)
	

	def parse_commit(self,response):
            pass
