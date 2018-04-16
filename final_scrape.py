
import requests
from bs4 import BeautifulSoup
import json
import string
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))



base_url = "https://www-prod.media.mit.edu/research/"

html = requests.get('https://www-prod.media.mit.edu/research/?filter=groups').text
soup = BeautifulSoup(html, 'html.parser')

page_soup = BeautifulSoup(html, 'html.parser')

row_content = page_soup.find_all("div",class_= "module-layout")


CACHE_FNAME = "SI507final_media_cache.json" 

try:
    fc = open(CACHE_FNAME,'r')
    b_str = fc.read()
    CACHE_DICTION = json.loads(b_str)
except:
    CACHE_DICTION = {}



r_dict = {}
page_text = requests.get('https://www-prod.media.mit.edu/research/?filter=groups').text
CACHE_DICTION['https://www-prod.media.mit.edu/research/'] = page_text
dumped_json_cache = json.dumps(CACHE_DICTION)
fw = open(CACHE_FNAME,"w")
fw.write(dumped_json_cache)
fw.close()
r_dict = CACHE_DICTION['https://www-prod.media.mit.edu/research/']

item = []
title=[]
# print(type(row_content))
all_groups = page_soup.find_all('div',class_='variant-group')
group_brief = page_soup.find_all('div',class_='module-title')
director = []
director_lst=[]
for row in row_content:
	print(len(row))
	director.append(row.find_all('footer'))

# print(director)
print(len(director))
for i in director:
	director_lst = i
# director = row_content.find('footer').find('div').find('a').text
# print(director)

title = page_soup.find_all('a',class_='module-content-guard')
# for i in title:
	# print(i.find('footer'))
	# print(type(i))
	# print(page_soup.find('footer').find('div').find('a').text)
	




# for row in row_content:
	# print(row)
	# print(row.find_all('div',class_='variant-group'))
	
		# item.append(row.find_all('div',class_='variant-group'))
		# print(item)
		# title = i.find_all('a',class_='module-content-guard')['href']
		# print(title)
		# print(item)
		# title=row.find('a',class_='module-content-guard')
			# print(item.find('data-href'))
		# title.append(row.find_all('a',class_='module-content-guard')['href'])
	
# for i in item:
	# print(i.find('a',class_='module-content-guard'))

	# print(title)
	# director = row.find('footer').find('div').find('a').text
	# # print(director)
	# # print(title.split('/')[2])
	# mission = row.find('div',class_='module-title')
	# # print(mission.text)
	# # print(title.text)
	# # print(row)
for i in item:
	# title = i.find('a',class_='module-content-guard')
	# print(title)
	pass

	





def get_medialab_data(filter):

	unique_id = base_url+ "?filter="+filter 

	param = {}
	pass 

