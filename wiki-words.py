from bs4 import BeautifulSoup
import requests, io, re

file = io.open("words-wiki.txt", "w+")
Words = set()

def getAllWords(response):
	soup = BeautifulSoup(response.text, "html.parser")
	words = soup.text
	myWords = set()
	words = re.sub('[^a-zA-Z\n]', ' ', words)
	for word in words.split(" "):
		myWord = (word.encode('ascii', 'ignore')).decode("utf-8")
		myWord = ''.join(c for c in myWord if c.isalpha())
		if len(myWord) > 2 and len(myWord) < 8:
			myWord = myWord.lower()
			myWords.add(myWord)
	return myWords

def getATags(response, id):
	test_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
	soup = BeautifulSoup(response.text, "html.parser")
	pages = soup.find("div", {"class": id})
	if(pages != None):
		pages = pages.findAll("a", href = True)
	page_url = set()
	if(pages != None):
		for page in pages:
			my_page = page['href']
			res = [ele for ele in test_list if(ele in my_page.lower())]
			if "index.php" not in my_page and "File" not in my_page and ".pdf" not in my_page and not bool(res):
				if my_page[0] == 'h':
					page_url.add(my_page)
				elif my_page[0] == '/':
					page_url.add('https://simple.m.wikipedia.org'+my_page)

	return list(page_url)

web_url = "https://simple.m.wikipedia.org/wiki/Wikipedia:List_of_1000_basic_words"
chk_url = "https://www.wordreference.com/definition/"
response = requests.get(web_url)
page_urls = [web_url]

i = 0
k = 0
while i < len(page_urls):
	try:
		page = page_urls[i]
		print("started: "+page)
		p = ((i+1)/len(page_urls))*100
		response = requests.get(page)
		a_tags = getATags(response, "mw-parser-output")
		for a_tag in a_tags:
			if a_tag not in page_urls:
				page_urls.append(a_tag)
		n = len(Words)
		Words = Words.union(getAllWords(response))
		temp = len(Words)
		if(temp == n):
			k+=1
		if k == 1000:
			break
		i+=1
		print("crawled page("+str(i)+"): "+page+"\nof: "+str(len(page_urls))+"\nwords found: "+str(len(Words))+"\npages no progress: "+str(k)+"\n")
	except:
		print("invalid link: "+page)
		page_urls.remove(page)

print(len(page_urls))
Word_list = list(set(Words))
Word_list.sort()

for word in Word_list:
	file.write(word+"\n")

file.close()