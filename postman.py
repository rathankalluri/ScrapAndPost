import requests
import json
import base64
import scraper as sc
import time

start_time = time.time()

user = 'username' #wordpress admin username
pythonapp = 'password' #wordpress password
url = 'http://your-wordpress-site.com/wp-json/wp/v2'

token = base64.standard_b64encode(user + ':' + pythonapp)
headers = {'Authorization': 'Basic ' + token}

#PRINT TO TEST

#print headers
#img_url, alt = sc.get_img_data()
#print img_url, alt
#keywords,content = sc.seo_data() #SEO Details - get more
#print keywords
#print content
#wp_title, slug = sc.title_slug_gen()
#print slug, wp_title
#exit() #REMOVE THIS

#PRINT TO TEST END

keywords,content = sc.seo_data()
wp_title, slug = sc.title_slug_gen()
content = open('cleaned.html', 'rb')
img_url, alt = sc.get_img_data()

#POST media to wp and get ID

media = {'file': open(img_url,'rb'),'caption': alt}
image = requests.post(url + '/media', headers=headers, files=media)
featured_media = json.loads(image.content)['id']

time.sleep(5)

#exit() #REMOVE THIS

#Create post with values
post = {'title': wp_title,
        'slug': slug,
        'status': 'publish',
        'content': content.read(),
        'author': '1',
        'excerpt': wp_title,
        'format': 'standard',
		'featured_media':featured_media
        }
		
r = requests.post(url + '/posts', headers=headers, json=post)

print "SECONDS LASPED"
print time.time() - start_time #
