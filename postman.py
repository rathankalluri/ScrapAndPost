import requests
import json
import base64
import time
import scraper as sc
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='postman.log',
                    filemode='a')



user = 'username' #wordpress admin username
pythonapp = 'password' #wordpress password
url = 'http://your-wordpress-site.com/wp-json/wp/v2'

token = base64.standard_b64encode(user + ':' + pythonapp)
headers = {'Authorization': 'Basic ' + token}

#Read each file and upload that 
with open('filelist.txt') as f:
	content = f.readlines()

content = [x.strip() for x in content]

import scraper as sc
for l in content:
	fname = sc.get_file(l)
	logging.info('-----------LOG INIT for %s ------------',fname) 

	start_time = time.time()

	#PRINT TO TEST

	#print headers
	#img_url, alt = sc.get_img_data()
	#print img_url, alt
	#keywords,content = sc.seo_data() #SEO Details - get more
	#print keywords
	#print content
	#wp_title, slug, category = sc.title_slug_gen()
	#print slug, wp_title, category
	#exit() #REMOVE THIS

	#PRINT TO TEST END

	keywords,description = sc.seo_data()
	logging.info('Got Keywords and SEO Content')

	wp_title, slug, category_name = sc.title_slug_gen()
	logging.info('Got Title: %s , Slug: %s , Category: %s', wp_title, slug, category_name)

	content = open('cleaned.html', 'rb')
	logging.info('Content scrapped')

	img_url, alt = sc.get_img_data()
	logging.info('Image created')

	#Create a category or Check if it exists

	cat_json = requests.get(url + '/categories', headers=headers)
	contents = cat_json.json()
	for i in contents:
		if i['name'] == category_name:
			 category_id = i['id']
			 logging.info('Category ID exists with ID : %d', category_id)
			 break
		else:
			cat = {'name': category_name}
			c = requests.post(url + '/categories', headers=headers, json=cat)
			cat = c.json()
			category_id = cat['id']
			logging.info('Category created with ID : %d', category_id)
			break

	#POST media to wp and get ID

	media = {'file': open(img_url,'rb'),'caption': alt}
	image = requests.post(url + '/media', headers=headers, files=media)
	featured_media = json.loads(image.content)['id']
	image_url = json.loads(image.content)['source_url']

	time.sleep(5)

	logging.info('Media Posted')
	#exit() #REMOVE THIS

	#Create post with values
	post = {'title': wp_title,
		'slug': slug,
		'status': 'publish',
		'content': content.read(),
		'categories': category_id,
		'author': '1',
		'excerpt': wp_title,
		'format': 'standard',
		'featured_media':featured_media
		}

	r = requests.post(url + '/posts', headers=headers, json=post)
	r = r.json()
	post_id = r['id']
	logging.info('Post Created with ID : %d', post_id)

	#SEO Tag updation
	# can use your own SEO related stuff.. have written a wp-json api code at wordpress to receive this code
	tags = {'post_id':post_id,
			'seo_title':wp_title,
			'seo_desc':description,
			'meta_title':'%%sitename%% | '+category_name+' | %%title%%',
			'img_url':image_url,
			'keywords':keywords}

	t = requests.post(url + '/yoast', headers=headers, json=tags)
	seo = t.json()
	logging.info(seo)

	logging.info('Post Created and lasped for : %s', time.time() - start_time)
	logging.info('-----------LOG END for %s -------------',fname) 
	print "Posting of file %s Completed".format(fname)
