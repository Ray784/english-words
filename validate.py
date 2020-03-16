import io, enchant
d = enchant.Dict("en_GB")

file_name = input("Enter file name to validate: ")
words_file =  io.open(file_name+".txt", "r")
valid_file = io.open("valid-"+file_name+".txt", "w")

words = words_file.read().split("\n")
valid_words = set()

i = 0
while i < len(words):
	try:
		word = words[i]
		if(word.strip() == ''):
			words.remove(word)
		else:
			p = (i/len(words))*100
			if(d.check(word)):
				print("valid word ("+str(i)+"): "+word+"\ntotal words: "+str(len(words))+"\npercentage complete: "+str(round(p, 2))+"\n")
				i+=1
			else:
				print("Invalid word: "+word+"\nwords: "+str(len(words))+"\npercentage complete: "+str(round(p, 2))+"\n")
				words.remove(word)
	except:
		print("error parsing: "+words[i])

valid_words = list(set(words))
valid_words.sort()

for word in valid_words:
	valid_file.write(word+"\n")
print(len(valid_words))