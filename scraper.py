from BeautifulSoup import BeautifulSoup
import json
import requests

#METHODS/FUNCTIONS
def get_file(fname):
	global filename
	filename = fname
	html = open(filename, 'rb')
	
	global soup
	soup = BeautifulSoup(html)
	initiator(soup)		
	remove_without_content()
	return filename

def _remove_attrs(divs):
    for tag in divs.findAll(True):
		if tag.name not in ['img', 'a']:
			tag.attrs = None
    return divs

def get_img_data():
	imgs = soup.findAll('img')
	for image in imgs:
		#return image['src'],image['alt']
		img_file = create_img(image['src'])
		return img_file, image['alt']

def create_img(url):
	resp = requests.get(url)
	fname = url.rsplit('/',1)[1]
	if resp.status_code == 200:
		with open(fname,"wb") as f:
			f.write(resp.content)
			return fname

def title_slug_gen():
	title = soup.find('title').text
	category = re.findall('\|(.*?)\|', title)
	wp_title = title.rsplit('| ',1)[1]
	link = soup.find(attrs={"rel":"canonical"})
	slug = link['href'][:-5].rsplit('/',1)[1]
	return wp_title, slug, category[0].strip() 

def seo_data():
	keywords = soup.find(attrs={"name":"keywords"})
	description = soup.find(attrs={"name":"description"})
	return keywords['content'].encode('utf-8'), description['content'].encode('utf-8')

def remove_without_content():
	format_code = open('formatted2.html', 'rb')
	to_clean = BeautifulSoup(format_code)
	clean = to_clean.findAll()
	for ele in clean:
		if len(ele.text) == 0:
			ele.extract()
	INVALID = ['table','script','br']
	
	for tag in to_clean.findAll():
		if tag.name in INVALID:
			tag.replaceWith(tag.text.strip())
		else:
			tag.text.strip()
	#creating a temp file as per my requirement, you can modify as you wish or can use as is
	#Need to make this code chunk better --->
	newfile = open('cleaned.html','w') #
	for d in to_clean:
		newfile.write("%s\n" % d)
	
	newfile = open('cleaned.html','rb')
	html = newfile.read()
	html  = " ".join(line.strip() for line in html.split("\n"))

	file = open('cleaned.html','w')
	for d in html:
		file.write("%s" % d)
	file.close()
	#<--- Need to make this code chunk better 
	
#CLEAN CONTENT
def initiator(soup):
	for divs in soup.findAll('div',attrs={"id":"ContentColumn"}):
		scripts = divs.findAll('script')
		#Remove Scripts
		for sc in scripts:
			sc.extract()
		html = divs.findAll('html')
		#Remove Ads
		for data in html:
			data.extract()
		style = divs.findAll('style')
		#Remove Style tags
		for st in style:
			st.extract()

		clean_divs = _remove_attrs(divs)

		thefile = open('formatted2.html', 'w') #creating a temp file as per my requirement, you can modify as you wish or can use as is
		for d in clean_divs:
			thefile.write("%s\n" % d)
#Program Ends
