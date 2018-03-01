try:
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import sent_tokenize
    from nltk.corpus import cmudict
    from bs4 import BeautifulSoup
    import urllib2
    import re
    import matplotlib.pyplot as plt
    import numpy as np
except:
    print "One or more libraries are missing! Kindly try again!!"

class Environment:
    records_for_graph_name = []
    records_for_graph_score = []   
    
    
    def read_input(self):
        print "------------------------------------------------------------------------------------------"
        while True:      
            print "1: See the score of a book" 
            print "2: View a graphical representation between the book name and the FRES score"
            print "3: Exit"
            
            try:
                choice = int(raw_input("Kindly input a choice\n"))
            except ValueError:
                print "You have entered a non-integer value! Pease enter an integer value and try again!"
                continue
            except:
                print "You have entered an invalid value! Pease enter a valid value and try again!"
                continue              
            
            if choice == 1:               
                title_letter = raw_input("Enter the letter by which you want to browse the titles of the books\n")
                title_letter = title_letter.lower().strip()
                print "........................Fetching the book names........................."
                scrape = self.web_scraping("http://www.gutenberg.org/browse/titles/"+title_letter)    
                if scrape == -1:
                    continue
                book_name = scrape[0]
                fres_score = scrape[1]
                self.records_for_graph_name.append(book_name)
                self.records_for_graph_score.append(fres_score)                
            
            elif choice == 2:
                self.create_graph()
            elif choice == 3:
                break                
            else:
                print "Invalid input! Please try again!"
                continue
            
           
        
    def create_graph(self):
            fig,ax = plt.subplots(1,1,figsize=(12,3))
            
            # create some x data and some integers for the y axis
            y = self.records_for_graph_score
            x = np.arange(len(self.records_for_graph_score))
            
            # tell matplotlib which yticks to plot 
            ax.set_xticks(x)
            
            # labelling the yticks according to the list
            labels = [item.get_text() for item in ax.get_xticklabels()]
            for i in range(0, len(self.records_for_graph_name)):
                labels[i] = self.records_for_graph_name[i]              
                
                
            plt.gcf().subplots_adjust(bottom=0.15)
            ax.set_xticklabels(labels, minor = False, rotation=45)   
            plt.xlabel('Book Name')
            plt.ylabel('FRES Score')  
            plt.title('Book Name V/S FRES Score graph')
            
            # plot the data
            ax.plot(x,y)        
            plt.show()    
        
    
    def web_scraping(self, url):
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find_all('div', attrs={'class': 'pgdbbytitle'})  
            
            name_link = []
            
            for link in table:
                for m in link.find_all('a'):
                    temp_link = m.get('href')
                    url_final = temp_link.encode('utf-8')
                    #print "url",url_final
                    url_final = "http://www.gutenberg.org"+url_final
                    if "ebooks" in url_final:
                        data = m.text
                        cleaned_data = self.cleanText(data)
                        cleaned_data = cleaned_data.replace("\n", " ")                    
                        name_link.append([{'link':url_final}, {'name':cleaned_data}])                   
            
            i = 1
            for book in name_link:
                print str(i)+ "." +book[1]['name'].title()
                i = i + 1
                # done to limit the number of books
                if i == 21:
                    break
            
            obj_agent = Agent()
            url_scrape = ""    
            choice = int(raw_input("Kindly choose a book for calculating the FRES score\n"))           
            if choice in range(0,i):
                choice_url = name_link[choice-1][0]['link']
                try:
                    page1 = urllib2.urlopen(choice_url)
                    soup1 = BeautifulSoup(page1, 'html.parser')
                    
                    # Removing the script content
                    for script in soup1(["script", "style"]):
                        script.extract()  # rip it out
                
                    cols = soup1.find_all('table', attrs={'class': 'files'})                    
                    
                    for link in cols:
                        for m in link.find_all('a'):
                            temp_link = m.get('href')  
                            if m.text in "Plain Text UTF-8":
                                url_scrape = temp_link
                            
                
                    
                    url_scrape = "http:"+url_scrape
                    
                    page2 = urllib2.urlopen(url_scrape)
                    soup2 = BeautifulSoup(page2, 'html.parser')
                    
                    # Removing the script content
                    for script in soup2(["script", "style"]):
                        script.extract()  # rip it out                    
                
                    cleaned_data = soup2.text.encode('ascii', 'ignore')
                    
                    
                    index = str(soup2).find("Author:")
                    index = index + 8
                    index_new_line = str(soup2).find('\n', index)
                   
                    author = "Anonymous"
                    
                    if index != -1 and index_new_line != -1:
                        author = str(soup2)[index: index_new_line+1]                   
                
                    author = author.strip()
                    fres = obj_agent.fres_score(cleaned_data)
                    
                    print "Book Title: ", name_link[choice-1][1]['name'].title()
                    print "Author: ", author.title()
                    print "FRES score: ", str(fres[0])
                    print "School level: ", str(fres[1])
                    
                    return (name_link[choice-1][1]['name'].title(), str(fres[0]))
                
                except urllib2.HTTPError:
                    print("You may have selected an audio book!")
                    return -1
                
                except:
                    print("You may have selected an audio book!")
                    return -1
                
            else:
                print "Invalid option selected!"
            
        except urllib2.HTTPError:
            print("Sorry! HTTP error occured!!")
            return
        
        except UnicodeEncodeError:
            print("Unicode Encode Error")
            return
        except:
            print("Error occured!!")        


    # Function to clean the text
    def cleanText(self, text):
        paras = (line.strip() for line in text.splitlines())
        chunks = (words.strip() for line in paras for words in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        try:
            return re.sub("[,;@#?:/\-+!&()$]+\ *", " ", text.encode('ascii', 'ignore')).lower()
        except:
            print("There is some issue with the RegEx library")


class Agent:
    def fres_score(self, sentance):
        number_of_syllables = 0
        tokenizer = RegexpTokenizer('\w+')
        x = tokenizer.tokenize(sentance)
        number_of_words = len(x)
        y = sent_tokenize(sentance)
        number_of_sentances = len(y)
        
        d = cmudict.dict()
        for word in x:
            
            try:
                number_of_syllables = number_of_syllables + [len(list(z for z in a if z[-1].isdigit())) for a in d[word.lower()]][0]
            except KeyError:
                number_of_syllables = number_of_syllables + self.syllables(word)
        
        fres_score_calc = 206.835-(1.015*(number_of_words/float(number_of_sentances)))-(84.6*(number_of_syllables/float(number_of_words)))
        flesch_grade = (0.39*(number_of_words/float(number_of_sentances))) + (11.8*(number_of_syllables/float(number_of_words)))-15.59
        
        fres_score_calc = round(fres_score_calc, 2)
        flesch_grade = round(flesch_grade, 2)
        
        return (fres_score_calc, flesch_grade)
        

    def syllables(self, word):
        # referred from stack overflow 'Count the number of syllables in a word'
        count = 0
        vowels = 'aeiouy'
        word = word.lower().strip(".:;?!")
        if word[0] in vowels:
            count +=1
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count+=1
        if count == 0:
            count +=1
        return count    
    
        
#obj_agent = Agent()
#obj_agent.fres_score("hi")
#obj_env = Environment()
#obj_env.read_input()
#obj_env.create_graph()

