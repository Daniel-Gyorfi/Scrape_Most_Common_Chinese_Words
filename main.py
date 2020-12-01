import requests
import re
import io
import bs4
from chinese import ChineseAnalyzer
from collections import Counter 
import chardet

def getEncoding(webtext): 
    encodings = ["utf-8", "gb18030"]
    for e in encodings:
        #print(type(test))
        try:
            if e == "utf-8":
                test = webtext.encode(e)
                if re.search(u'[\u4e00-\u9fff]', test.decode(e)):
                    return e
            else:
                test = webtext.encode(e)
                if re.search(u'[\u4e00-\u9fff]', test.decode(e)):
                    return e
        except Exception as e:
            print(e)
    return "no compatible encoding"
        
def scrapeText(url):
    # turns url text contents into text file
    #page = str(urllib.request.urlopen(url).read())
    #soup = bs4.BeautifulSoup(page)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    pText = soup.get_text()
    fname = input("Filename: ") + ".txt"
    enco = getEncoding(pText)
    if (enco == "no compatible encoding"):
        raise Exception(enco)
    with open(fname, "w", encoding= enco) as f:
        f.write(pText)
    print("download complete")

def showZipf(filetext):
    # shows most common Chinese words/characters
    # opens file
    with open(filetext, "r", encoding="utf-8") as f:
        # create object from Chinese lib
        chinlyzer = ChineseAnalyzer()
        content = f.read()
        parse = chinlyzer.parse(content)
        common = []
    #for loop sorts chinese characters into new counter
        for k in parse.freq().elements():
    #checks if character is in a unicode range for Chinese characters
            if re.search(u'[\u4e00-\u9fff]', k):
                common.append(k)
        common = Counter(common)
        print(common.most_common(20))
        
# two prompts-- scrape web andor analyze file
# repeat prompt until either yes or no is input
# might check inputs from a collection of pos/neg answers
print("Would you like to scrape a new webpage?")
answer = ""
while answer != "no" and answer != "yes":
    answer = input("Y/N: ").lower()          
    if (answer == "yes"):
        try :
            scrapeText(input("URL: "))
        except Exception as e:
            print(e)
    elif (answer == "no"):
        print("ok then")
print("Analyze a file?")
answer = ""
while answer != "no" and answer != "yes":
    answer = input("Y/N: ").lower()          
    if (answer == "yes"):
        try :
            print("Zipf analysis")
            showZipf(input("Filename: ") + ".txt")
        except Exception as e:
            print(e)
    elif (answer == "no"):
        print("ok then")
