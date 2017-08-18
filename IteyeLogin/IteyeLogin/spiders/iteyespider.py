#-*- coding: utf-8 -*
__author__ = 'Howie'
from scrapy.http import Request,FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from xlwt import *
import re
class IteyeSpider(Spider):
        download_delay=3
	name="iteye_spider"
	login_page ="http://www.iteye.com/login"
	start_urls = ["http://kevinflynn.iteye.com/",
                  "http://kevinflynn.iteye.com/blog/2281218"]

	headers={
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
		"Upgrade-Insecure-Requests":"1",
		"Referer":"http://www.iteye.com/login",
	}
	
	def start_requests(self):
		return [Request(self.login_page,callback=self.post_login)]
	
	def post_login(self,response):
		authenticity_token=Selector(response).xpath('//input[@name="authenticity_token"]/@value').extract()[0]
		return [FormRequest.from_response(response,
                                          formdata={
                                              'authenticity_token':authenticity_token,
                                              'name':'kevinflynn',
                                              'password':'',
                                              'button':'登　录',
                                          },headers=self.headers,
                                          callback=self.logged_in)]

	def logged_in(self,response):
	#	return [Request(self.start_urls[0],self.get_page)]
                yield Request(url="http://www.iteye.com/blogs",callback=self.parse_blog_list)

        def parse_blog_list(self,response):
                sel=Selector(response)
                urls=sel.xpath("//div[@class='content']/h3/a/@href").extract()
                for url in urls:
                    yield Request(url=url,callback=self.parse_blog_page)

        def parse_blog_page(self,response):
                sel=Selector(response)
                authenticity_token=sel.xpath("//*[@name='authenticity_token']/@value").extract_first()
                current_url=response.url
                blog_id= current_url[current_url.index("blog")+5:]
		blog_pre_url=current_url[0:current_url.index("blog")]+"blog"
                commit_url=blog_pre_url+"/create_comment/"+str(blog_id)
                commit_content="点赞，点赞，点赞，点赞!!!!"
                formdata={"comment[body]":commit_content,"commit":"提交","_":"","authenticity_token":authenticity_token}
                yield FormRequest(url=commit_url,formdata=formdata,callback=self.parse_commit,dont_filter=True)



	def get_page(self, response):
		sel=Selector(response)
		titles=sel.xpath('//h3/a/text()').extract()
		for title in titles:
			print title
        #        yield Request(url="http://gaojingsong.iteye.com/blog/2390198",callback=self.post_commit)

        def post_commit(self,response):
            sel=Selector(response)
            authenticity_token=sel.xpath("//*[@name='authenticity_token']/@value").extract_first()
            commit_url="http://gaojingsong.iteye.com/blog/create_comment/2390198"

            formdata={"comment[body]":"可以，很不错，很不错，点赞！！！","commit":"提交","_":"","authenticity_token":authenticity_token}
            yield FormRequest(url=commit_url,formdata=formdata,callback=self.parse_commit,dont_filter=False)

        def parse_commit(self,response):
            pass
        #    print response.body






