from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
from random import *
import copy
import requests

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}

class Gift():
	def __init__(self,giftTo,link,image):
		self.giftTo = giftTo
		self.link = link
		self.image = image
	
	

def getAmazonLink(budget):
	return "https://www.amazon.in/s?k=gift&rh=p_36%3A-"+str(budget)+"00&s=review-rank"

def derange(l):
	o=l[:]
	while any(x==y for x,y in zip(o,l)):shuffle(l)


def getLinks(n,budget):
	link = getAmazonLink(budget)
	r = requests.get(link, headers=headers)
	soup = BeautifulSoup(r.text,'lxml')
	links = soup.find_all("a", attrs={'class':'a-link-normal a-text-normal'})
	

	links_list = []
	for link in links:
		links_list.append(link.get('href'))
	
	return links_list[:n]

def getImages(n,budget):
	link = getAmazonLink(budget)
	r = requests.get(link,headers=headers)
	soup = BeautifulSoup(r.text,'lxml')
	image_paths = soup.find_all("img",attrs={'class':'s-image'})
	links = image_paths[:n]

	images_list = []
	for link in links:
		images_list.append(link.get("src"))
	return images_list[:n]


def randomiseUsers(n,budget):
	links_list = getLinks(n,budget)
	images_list = getImages(n,budget)
	original_list = list(range(n))
	new_list = original_list[::]
	derange(new_list)
	list_of_gifts = []
	for i in range(n):
		g = Gift(new_list[i],"https://www.amazon.in"+links_list[i],images_list[i])
		list_of_gifts.append(g)

	
	return list_of_gifts

if __name__ == "__main__":
	l = randomiseUsers(8,400)
	for i in l:
		print(i.giftTo, i.link, i.image)

	
