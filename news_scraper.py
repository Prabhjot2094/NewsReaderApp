from bs4 import BeautifulSoup
import urllib2
import sys
import urllib
import csv
import os
import shutil


eco_link = "http://economictimes.indiatimes.com/news/latest-news/most-read"
toi_link = "http://timesofindia.indiatimes.com"

def get_img(soup,link,directory,name,j):
	print "In get_img"
	img_parent = soup.find("section",attrs={"class":"highlight clearfix"})
	if img_parent == None:
		img_parent = soup.find("section",attrs={"class":"highlight clearfix vdo"})
		if img_parent != None:
			image = img_parent.find("img")#,attrs={"class":"highlight clearfix vdo")
	else:
		image = img_parent.find("img")

	try :
		ext = image["src"]
	except :
		print "returning from get_img"
		return
	link = link+ext
	image_name = directory+name+str(j)+"_.jpg"#ext[-3:]
	urllib.urlretrieve(link,image_name)

def get_img_eco(soup,link,directory,name,j):
	img_parent = soup.find("figure")
	#img_parent.img["src"]
	try :
		image = img_parent.find("img")
		ext = image["src"]
	except :
		return

	link = link+ext
	image_name = directory+name+str(j)+"_.jpg"
	urllib.urlretrieve(link,image_name)

def detail_scrape(link,f,directory,name,site,j):
	#return
	print "In detai_scrape"
	if link[0]!='h':
		if site=="toi":
			link = toi_link+link
		elif site=="eco":
			link = eco_link+link
	print link 
	#sys.exit()
	try:
		lin = urllib2.urlopen(link).read()
		soup = BeautifulSoup(lin)	
		print "Souped"

		if site=="toi":
			get_img(soup,link,directory,name,j)
		elif site=="eco":
			get_img_eco(soup,link,directory,name,j)
			
		heading = soup.find("h1")
		heading = heading.text.encode("utf-8")
		f.write(heading)
		f.write('#')

		detail_news = soup.find("div",attrs={"class":"Normal"})
		detail_news = detail_news.text.encode('utf-8')
		f.write(detail_news)

		f.close()
		print detail_news
	except:
		print "returning from detail scrape"
		return


def toi_scrape(news_type):
	lin = urllib2.urlopen(toi_link).read()
	soup = BeautifulSoup(lin)

	top_news = soup.find("ul",attrs={"data-vr-zone":news_type})
	li = top_news.find_all("li")

	directory = "F:/News/"+news_type+"/"
	if os.path.exists(directory)==True:
		shutil.rmtree(directory)
	os.mkdir(directory)

	j=0
	for i in li:
		
		j+=1

		news = i.text.encode('utf-8')
		link = i.a["href"]

		ext = news.split()
		ext[0] = ext[0].translate(None,":/\?*\"<>|'")

		ext[0]=''.join([i if ord(i) < 128 else ' ' for i in ext[0]])

		file_name = directory+ext[0]+str(j)+"_.txt"
		
		if news[1:4]=="Adv" or link.find("articleshow")<0:
			continue

		f=open(file_name,'w')
		f.write(news)
		f.write("#")

		print news
		print link
		detail_scrape(link,f,directory,ext[0],"toi",j)

def eco_times_scrape():
	lin = urllib2.urlopen(eco_link).read()
	soup = BeautifulSoup(lin)

	list_parent = soup.find("ul",attrs = {"class":"data"})
	li = list_parent.find_all("li")

	directory = "F:/News/business/"
	if os.path.exists(directory)==True:
		shutil.rmtree(directory)
	os.mkdir(directory)

	j=0
	for i in li:
		
		j+=1

		link = i.a["href"]
		news = i.text.encode("utf-8")

		ext = news.split()
		ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
		file_name = directory+ext[0]+str(j)+"_.txt"

		if news[1:4]=="Adv" or link.find("articleshow")<0:
			continue

		f=open(file_name,'w')
		f.write(news)
		f.write("#")
		print news
		print link
		detail_scrape(link,f,directory,ext[0],"eco",j)


	news_list = ["top_stories","across_toi","latest"]
for news in news_list:
	toi_scrape(news)
eco_times_scrape()
