from bs4 import BeautifulSoup
import urllib2
import sys
import urllib
import csv

toi_link = "http://timesofindia.indiatimes.com"
lin = urllib2.urlopen(toi_link).read()
soup = BeautifulSoup(lin)

def detail_scrape(link,f):
	#return
	if link[0]!='h':
		link = toi_link+link
	print link 
	#sys.exit()
	lin = urllib2.urlopen(link).read()
	soup = BeautifulSoup(lin)	
	#print soup.prettify().encode('utf-8')
	detail_news = soup.find("div",attrs={"class":"Normal"})
	detail_news = detail_news.text.encode('utf-8')
	f.write(detail_news)
	f.close()
	print detail_news
	#sys.exit()

def headline_scrape(news_type):
	top_news = soup.find("ul",attrs={"data-vr-zone":news_type})
	#print result
	li = top_news.find_all("li")

	for i in li:
		news = i.text.encode('utf-8')
		link = i.a["href"]

		ext = news.split()
		ext[0] = ext[0].translate(None,":/\?*\"<>|'")		
		directory = "F:\News\\"+news_type+"\\"+ext[0]+"_.doc"
		
		if news[1:4]=="Adv" or link.find("articleshow")<0:
			continue

		f=open(directory,'w')
		f.write(news)
		f.write("\n")

		print news
		print link
		detail_scrape(link,f)

headline_scrape("top_stories")
headline_scrape("latest")
headline_scrape("across_toi")
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