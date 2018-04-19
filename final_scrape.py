
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
import string
import nltk 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))


CACHE_FNAME = "SI507final_media_cache.json" 

try:
    fc = open(CACHE_FNAME,'r')
    b_str = fc.read()
    CACHE_DICTION = json.loads(b_str)
except:
    CACHE_DICTION = {}

base_url = "https://www-prod.media.mit.edu"
groups_url= base_url + "/research"
# "https://www-prod.media.mit.edu/research/?filter=groups"

# return a dictonary of each lab and associated values 
def get_medialab_data():
	
	# "https://www-prod.media.mit.edu/research/?filter=groups"
	# param = {}

	if groups_url in CACHE_DICTION:
		print('Fetching cached data')
		r_dict = CACHE_DICTION[groups_url]
	else:
		print("Getting data from the Media Lab")
		page_text = requests.get(groups_url).text
		CACHE_DICTION[groups_url] = page_text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close()
		r_dict=CACHE_DICTION[groups_url]

	page_soup = BeautifulSoup(r_dict, 'html.parser')

# row_content = page_soup.find_all("div",class_= "module-layout")

	group_dict = {}
	# {labname:{director="",lab_brief='',PI_email='',peoplenum=0,recentup=0}}
	# Getting all the media lab research groups, their group briefs, number of people, number of reserach hashtags and directors 
	all_groups = page_soup.find_all('div',class_='variant-group')
	# group_name = []
	# lab_brief=[]
	# directors = []
	# print(len(all_groups))
	for i in all_groups:

		# name_row = all_groups[i]
		group_dict[i['data-href'].split('/')[2]]={}		# consturcting dictionary using group name as key
		# group_name.append(i['data-href'].split('/')[2])  # Group name 
		for j in i.find_all('footer',class_="module-meta"):
			if j.find('a')['href'].startswith('/people'):		
				# print(j.find('a').text)
				group_dict[i['data-href'].split('/')[2]]['director'] = j.find('a').text
				# directors.append(j.find('a').text)
			else:
				group_dict[i['data-href'].split('/')[2]]['director'] ="NA"
				# directors.append("NA")
		group_brief = i.find('div',class_='module-title')
		group_dict[i['data-href'].split('/')[2]]['brief'] = group_brief.text

		lab_name= i['data-href'].split('/')[2]
		people_url = base_url+"/groups/"+lab_name+"/people/"
		if people_url in CACHE_DICTION:
			print('Fetching cached people data from ' + lab_name + " lab")
			p_dict = CACHE_DICTION[people_url]
		else:
			print("Getting people data from " + lab_name+ " lab")
			people_text = requests.get(people_url).text
			CACHE_DICTION[people_url] = people_text
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME,"w")
			fw.write(dumped_json_cache)
			fw.close()
			p_dict=CACHE_DICTION[people_url]

	
		people_soup = BeautifulSoup(p_dict,'html.parser')
		people_row = people_soup.find_all('div', class_='container-item')
		# print(len(people_row))
		group_dict[i['data-href'].split('/')[2]]['peoplenum'] = len(people_row)
		# print(people_row)
		# for p in people_row:
			# print(p.find('div',class_='module-title'))
	

		overview_url = base_url+"/groups/"+lab_name+"/overview/"
		if overview_url in CACHE_DICTION:
			print('Fetching cached hashtag data from ' + lab_name + " lab")
			h_dict = CACHE_DICTION[overview_url]
		else:
			print("Getting hashtag data from " + lab_name+ " lab")
			hash_text = requests.get(overview_url).text
			CACHE_DICTION[overview_url] = hash_text
			dumped_json_cache = json.dumps(CACHE_DICTION)
			fw = open(CACHE_FNAME,"w")
			fw.write(dumped_json_cache)
			fw.close()
			h_dict=CACHE_DICTION[overview_url]

		hash_soup = BeautifulSoup(h_dict,'html.parser')
		hash_row = hash_soup.find('div',class_="primary-block-meta")
		hash_lst = []

		for h in hash_row.find_all('a'):
			hash_lst.append(h.text)

		group_dict[i['data-href'].split('/')[2]]['hashnum'] = len(hash_row.find_all('a'))
		group_dict[i['data-href'].split('/')[2]]['hashtags'] = hash_lst

		#Gettign the most updated news and events 
		# update_url = base_url+"/groups/"+lab_name+"/updates/"
		# if update_url in CACHE_DICTION:
		# 	print('Fetching cached updates data from ' + lab_name + " lab")
		# 	u_dict = CACHE_DICTION[update_url]
		# else:
		# 	print("Getting updates data from " + lab_name+ " lab")
		# 	up_text = requests.get(update_url).text
		# 	CACHE_DICTION[update_url] = up_text
		# 	dumped_json_cache = json.dumps(CACHE_DICTION)
		# 	fw = open(CACHE_FNAME,"w")
		# 	fw.write(dumped_json_cache)
		# 	fw.close()
		# 	u_dict=CACHE_DICTION[update_url]

		# update_soup = BeautifulSoup(u_dict,'html.parser')
		# if lab_name == 'design-fiction':
		# 	print('too ficted')
		# else:
		# 	update_row = update_soup.find('div',class_="item-container")
		# 	newest = update_row.find('div',class_='module')
		# 	for n in newest.find('footer',class_='module-meta'):
		# 		for d in n:
		# 			if d != type(''):
		# 				print(d)
		# 				print(type(d))	
				# print(n)
			
			# print(newest)
		# hash_lst = []

	return group_dict

# get_medialab_data()
# labs = get_medialab_data()
# print(labs)
# print(labs.keys())
# print(labs['space-enabled']['brief'])

	

def get_project_data(lab_name):
	project_url = base_url+"/groups/" + lab_name+"/projects/"
	if project_url in CACHE_DICTION:
		print('Fetching cached project data from ' + lab_name + " lab")
		r_dict = CACHE_DICTION[project_url]
	else:
		print("Getting project data from " + lab_name+ " lab")
		project_text = requests.get(project_url).text
		CACHE_DICTION[project_url] = project_text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close()
		r_dict=CACHE_DICTION[project_url]

	project_soup =  BeautifulSoup(r_dict,'html.parser')
	all_pro = project_soup.find_all('div', class_='container-item')

	project_info = {}
	# print(all_pro)
	for i in all_pro:
		for j in i.find('a',class_="module-content-guard").find(('h2')): # project name 
			# print(j)
			project_info[j] = {}
			project_name = j
		# print(i.find('div',class_="module-excerpt").find('p').text)
		project_info[j]['brief'] = i.find('div',class_="module-excerpt").find('p').text

		# find detailed info for each project 	
		# each_project_url = base_url+"/projects/" +project_name+"/overview"

		# if each_project_url in CACHE_DICTION:
		# 	print('Fetching cached project data from ' + project_name + " project")
		# 	e_dict = CACHE_DICTION[each_project_url]
		# else:
		# 	print("Getting project data from " + project_name+ " project")
		# 	each_text = requests.get(each_project_url).text
		# 	CACHE_DICTION[each_project_url] = each_text
		# 	dumped_json_cache = json.dumps(CACHE_DICTION)
		# 	fw = open(CACHE_FNAME,"w")
		# 	fw.write(dumped_json_cache)
		# 	fw.close()
		# 	e_dict=CACHE_DICTION[each_project_url]

		# each_soup = BeautifulSoup(r_dict,'html.parser')

	return project_info
		
# get_project_data('collective-learning')


def get_hashtag():
	groups_url= base_url + "/research"
	hash_lst = []

	if groups_url in CACHE_DICTION:
		print('Fetching cached data')
		r_dict = CACHE_DICTION[groups_url]
	else:
		print("Getting hashtag data from the Media Lab")
		page_text = requests.get(groups_url).text
		CACHE_DICTION[groups_url] = page_text
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close()
		r_dict=CACHE_DICTION[groups_url]

	page_soup = BeautifulSoup(r_dict, 'html.parser')

	hashtags = page_soup.find_all('li',class_="autocomplete-result")

	for i in hashtags:
		hash_lst.append(i.find('p').text.strip())


	return hash_lst



all_hash = get_hashtag()
print(len(all_hash))



#-------------- Write out the json -------------------------
# media json that for group table 
# r_json_nice = json.dumps(labs,indent = 2)
# f = open("media.json",'w')
# f.write(r_json_nice)
# f.close()

# hashtag json for hashtag table 
h_json_nice = json.dumps(all_hash,indent=2)
f = open("hashtag.json",'w')
f.write(h_json_nice)
f.close()











