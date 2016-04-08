from bs4 import BeautifulSoup
import urllib2
import sys
import urllib
import csv
import os
import shutil


eco_link = "http://economictimes.indiatimes.com/news/latest-news/most-read"
toi_link = "http://timesofindia.indiatimes.com"

def get_img(soup,link,directory,name):
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
	image_name = directory+name+"_.jpg"#ext[-3:]
	urllib.urlretrieve(link,image_name)

def get_img_eco(soup,link,directory,name):
	img_parent = soup.find("figure")
	#img_parent.img["src"]
	try :
		image = img_parent.find("img")
		ext = image["src"]
	except :
		return

	link = link+ext
	image_name = directory+name+"_.jpg"
	urllib.urlretrieve(link,image_name)

def detail_scrape(link,f,directory,name,site):
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
			get_img(soup,link,directory,name)
		elif site=="eco":
			get_img_eco(soup,link,directory,name)
			
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
	#sys.exit()


# def eco_times_detail_scrape(link,f,directory,name):
# 	if link[0]!='h':
# 		link = toi_link+link
# 	print link

# 	lin = urllib2.urlopen(link).read()
# 	soup = BeautifulSoup(lin)

# 	detail_news = 


def toi_scrape(news_type):
	lin = urllib2.urlopen(toi_link).read()
	soup = BeautifulSoup(lin)

	top_news = soup.find("ul",attrs={"data-vr-zone":news_type})
	li = top_news.find_all("li")

	directory = "F:\News\\"+news_type+"\\"
	if os.path.exists(directory)==True:
		shutil.rmtree(directory)
	os.mkdir(directory)

	for i in li:
		news = i.text.encode('utf-8')
		link = i.a["href"]

		ext = news.split()
		ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
		file_name = directory+ext[0]+"_.txt"
		
		if news[1:4]=="Adv" or link.find("articleshow")<0:
			continue

		f=open(file_name,'w')
		f.write(news)
		f.write("#")

		print news
		print link
		detail_scrape(link,f,directory,ext[0],"toi")

def eco_times_scrape():
	lin = urllib2.urlopen(eco_link).read()
	soup = BeautifulSoup(lin)

	list_parent = soup.find("ul",attrs = {"class":"data"})
	li = list_parent.find_all("li")

	directory = "F:\News\\business\\"
	if os.path.exists(directory)==True:
		shutil.rmtree(directory)
	os.mkdir(directory)

	for i in li:
		link = i.a["href"]
		news = i.text.encode("utf-8")

		ext = news.split()
		ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
		file_name = directory+ext[0]+"_.txt"

		if news[1:4]=="Adv" or link.find("articleshow")<0:
			continue

		f=open(file_name,'w')
		f.write(news)
		f.write("#")
		print news
		print link
		detail_scrape(link,f,directory,ext[0],"eco")



	# while i<10:
	# 	i+=1
	# 	print li
	# 	li=li.next_sibling

news_list = ["top_stories","across_toi","latest"]
for news in news_list:
	toi_scrape(news)
eco_times_scrape()
# headline_scrape("top_stories")
# headline_scrape("latest")
# headline_scrape("across_toi")
#top_news = soup.find("ul",attrs={"data-vr-zone":"top_stories"})
#print result
# li = top_news.find_all("li")

# for i in li:
# 	news = i.text.encode('utf-8')
# 	link = i.a["href"]

# 	ext = news.split()
# 	ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
# 	directory = "F:\News\\top_news\\"+ext[0]+"_.txt"
	
# 	if news[1:4]=="Adv" or link.find("articleshow")<0:
# 		continue
# 	f=open(directory,'w')
# 	f.write(news)
# 	#string = news+'^'+link
# 	#top_news.write(string)
# 	#writer.writerow(string)
# 	print news
# 	print link
# 	detail_scrape(link,f)


# latest = soup.find("ul",attrs={"data-vr-zone":"latest"})
# #print result
# li = latest.find_all("li")

# for i in li:	
# 	news = i.text.encode('utf-8')
# 	link = i.a["href"]
	
# 	ext = news.split()
# 	ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
# 	directory = "F:\News\\latest\\"+ext[0]+"_.txt"

# 	if news[1:4]=="Adv" or link.find("articleshow")<0:
# 		continue

# 	f=open(directory,'w')
# 	f.write(news)
# 	#string = news+'^'+link
# 	#top_news.write(string)
# 	#writer.writerow(string)
# 	print news[1:4]
# 	print link
# 	detail_scrape(link,f)

# across_toi = soup.find("ul",attrs={"data-vr-zone":"across_toi"})
# #print result
# li = across_toi.find_all("li")

# for i in li:
# 	news = i.text.encode('utf-8')
# 	link = i.a["href"]
	
# 	ext = news.split()
# 	ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
# 	directory = "F:\News\\across_toi\\"+ext[0]+"_.txt"

# 	if news[1:4]=="Adv" or link.find("articleshow")<0:
# 		continue

# 	f=open(directory,'w')
# 	f.write(news)
# 	f.write("\n")
# 	#string = news+'^'+link
# 	#top_news.write(string)
# 	#writer.writerow(string)
# 	print news
# 	print link
# 	detail_scrape(link,f)