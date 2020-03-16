from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, io, time, re, enchant

def isValid(browser, page):
	if page != browser.current_url:
		return False
	return True

def isEnValid(word):
	d = enchant.Dict("en_GB")
	return d.check(word)

def getSynonyms(browser):
	words_set = set()
	html_list = browser.find_element_by_class_name("css-1lc0dpe")
	items = html_list.find_elements_by_tag_name("li")
	total_count = 0
	sp_count = 0
	for item in items:
		text = item.text.lower()
		text = re.sub('[^a-zA-Z\n]', ' ', text)
		if len(text) > 2 and len(text) < 8 and (' ' not in text):
			if isEnValid(text):
				words_set.add(text)
		elif ' ' in text:
			sp_count += 1 
		else:
			total_count += 1

	total_count += len(words_set)
	return [words_set, total_count, sp_count]	

web_url = "https://www.thesaurus.com/browse/"

file_name = input("Enter file name: ")
words = io.open(file_name+'.txt', 'r').read().split("\n")

other_words = set()
browser = webdriver.Chrome()

i = 0
total = len(words)

while i < len(words):
	total = len(words)
	if words[i].strip() != '':
		try:
			word = words[i].strip()
			page = web_url + word
			browser.get(page)
			print("parsing word: "+word+" ...waiting for page to load...")
			time.sleep(3)
			if isValid(browser, page):
				li_list = browser.find_element_by_class_name("css-172saqb").find_elements_by_tag_name("li")
				tc = 0
				sc = 0
				for li in li_list:
					button = li.find_element_by_tag_name("a")
					button.click()
					out = getSynonyms(browser)
					tc += out[1]
					sc += out[2]
					other_words = other_words.union(out[0])
				if(tc >= sc):
					p = round((((i+1) / total)*100), 2)
					print("words done: "+str(i+1)+" of "+str(total)+"\npercentage complete: "+str(p)+"\n")
					i += 1
				else:
					if not isEnValid(word):
						words.remove(word)
					else:
						i+=1
				time.sleep(3)
			else:
				i+=1
		except:
			print("connection error ")
	else:
		words.remove(words[i])

words = list(set(words).union(other_words))
words.sort()
print(len(words))

browser.close()

io.open('synon-words-wiki.txt', 'w').write('\n'.join(words))