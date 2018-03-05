import requests
import json
import base64
import scraper as sc
import time

start_time = time.time()

user = 'charles'
pythonapp = '31CM7WvDRBRscelaiy'
url = 'http://rathankalluri.com/charles/wp-json/wp/v2'

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
print(json.loads(r.content))

print "SECONDS LASPED"
print time.time() - start_time

"""
imgsrc = json.loads(up.content)['source_url']
postid = json.loads(r.content)['id']
updatedpost = {'content': 'Changed things.<img src=' 
        + imgsrc
        + '>'}
		
update = requests.post(url + '/posts/' + postid, headers=headers, json=updatedpost)
print('The updated post is published on ' + json.loads(updatedpost.content)['link'])
"""




"""content = open('formatted2.html', 'rb')
#postname = basename('formatted.html')
file, ext = os.path.splitext('formatted.html')
upload_file = urllib.urlopen('http://www.daily-bible-verse.net/images/1Corinthians13-3.jpg').read()

i = requests.post("http://rathankalluri.com/charles/wp-json/wp/v2/media",auth=('charles', '31CM7WvDRBRscelaiy'),
data={files=upload_file})

print(r.status_code, r.reason, r)


r = requests.post("http://rathankalluri.com/charles/wp-json/wp/v2/posts", data={
'title':file,
'content': content.read(),
'status':'draft',
'featured_media': featured_media
}, auth=('charles', '31CM7WvDRBRscelaiy'))

print(r.status_code, r.reason)"""