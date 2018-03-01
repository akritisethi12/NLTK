try:    
    from bs4 import BeautifulSoup
    import urllib2
    from nltk.tokenize import RegexpTokenizer
    from nltk.tokenize import sent_tokenize
    import nltk
    import re
    import matplotlib.pyplot as plt
    from collections import Counter
    import numpy as np
    import matplotlib.patches as mpatches
    import pickle
    import os
    import requests
    import cookielib
    import json
except:
    print "Some libraries are missing!!"

class Interaction_Retrieval:
    content = ""
    interactions = []
    location_list = []
    def scrape_web(self):
        try:
            url = "http://www.gutenberg.org/cache/epub/583/pg583.txt"
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            
            # Removing the script content
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
        
            cols = soup.text.encode('ascii', 'ignore')
            
        
            index_start = str(cols).find("*** START OF THIS PROJECT GUTENBERG EBOOK THE WOMAN IN WHITE ***")
            index_start = index_start + len("*** START OF THIS PROJECT GUTENBERG EBOOK THE WOMAN IN WHITE ***")
            
            index_end = str(cols).find("*** END OF THIS PROJECT GUTENBERG EBOOK THE WOMAN IN WHITE ***")          
            
            cols = cols[index_start:index_end]
            self.content = cols.strip()            
        
        except urllib2.HTTPError:
            print("You may have selected an audio book!")
            return
        
        except KeyError:
            print "Key error occured"
            return
        except:
            print "Error occured!!"
            return
            
    def process_content(self):
        print "Finding PERSON-PERSON interactions! This may take some time!"
        try:
            
            sentences = nltk.sent_tokenize(self.content)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [nltk.pos_tag(sent) for sent in sentences]        
            
            regex_interactions = nltk.RegexpParser('CHUNK: {<PERSON> <V.*> <PERSON>}')
            for sent in sentences:
                tree = regex_interactions.parse(nltk.ne_chunk(sent))
                temp_string = ""
                for subtree in tree.subtrees():
                    if subtree.label() == 'CHUNK':                     
                        for item in subtree.leaves():
                            temp_string = temp_string + item[0]+" "
                        self.interactions.append(temp_string)
                        
            
            
            print "The interactions between the characters of the book 'The Woman in White' are: "
            for item in self.interactions:
                print item
        
            self.plot_graph()
        except urllib2.HTTPError:
            print("You may have selected an audio book!")
            return
        
        except KeyError:
            print "Key error occured"
            return
        except AttributeError:
            print "Attribute error occured!!"
            return        
        except NameError:
            print "Name error occured!!"
            return        
        except:
            print "Error occured!!"
            return        
            
    
    def location_people(self):
        print "Finding the relations between PERSON and LOCATION in the book 'The Woman in White' by Wilkie Collins. This may take some time!"
        try:
            
            sentences = nltk.sent_tokenize(self.content)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [nltk.pos_tag(sent) for sent in sentences]  
            
            chunk_sent = [nltk.ne_chunk(sentence) for sentence in sentences]
            
            location_person_list = []
            location_person_list_final = []
            
            print "The following are the PERSON LOCATION interactions in the book 'The Woman in White' by Wilkie Collins"
            
            IN = re.compile(r'.*')
            for doc in chunk_sent:            
                for rel in nltk.sem.extract_rels('PERSON', 'GPE', doc, pattern = IN):
                    doc = ' '.join([w for w, t in doc.leaves()]),nltk.sem.rtuple(rel)
                    location_person_list.append((doc, nltk.sem.rtuple(rel)))
                    #print doc
                         
            
            #print "location person list", location_person_list
            
            location_person_list = location_person_list[len(location_person_list)-10:]
            
            i = 0
            person_list = []
            
            dict_pickle = {}
            index_image = 1
    
            for item in location_person_list:
                dict_pickle[index_image] = item[0][0]
                index_image = index_image + 1
                
                index_person = item[1].find("[PER:")
                index_person = index_person + len("[PER:") + 2        
                index_end_person = item[1].find("/", index_person)                        
                person_list.append(item[1][index_person: index_end_person])
                
                index = item[1].find("[GPE:")
                index = index + len("[GPE:") + 2
                
                index_end = item[1].find("/", index)
                
                item = list(item)
                item[1] = item[1][index: index_end]
                item = tuple(item) 
                
                self.location_list.append(item[1])
                location_person_list[i] = item
                i = i + 1
            
            
            for key in dict_pickle.keys():
                print(str(key) + ": " + str(dict_pickle[key]))       
                
            # writing the contents to a pickel file
            path = os.getcwd()+"\\jythonMusic\\imagesAndData\\"
            if not os.path.exists(path):
                os.makedirs(path)        
            data = open(os.path.join(path, 'image_doc.pickle'), 'wb')
            pickle.dump(dict_pickle, data, protocol=pickle.HIGHEST_PROTOCOL)  
            data.close()
            
            self.create_graph_location(person_list, self.location_list) 
        
        except urllib2.HTTPError:
            print("You may have selected an audio book!")
            return
        
        except KeyError:
            print "Key error occured"
            return
        except AttributeError:
            print "Attribute error occured!!"
            return        
        except NameError:
            print "Name error occured!!"
            return        
        except:
            print "Error occured!!"
            return   
        
    def pass_locations(self):
        x = 0
        for loc in self.location_list:
            self.scrape_google(loc,x)
            x = x + 1   
    
    def get_soup(self, url,header):
        try:
            return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
        except urllib2.HTTPError:
            print("Error in connection!")
            return        
        except KeyError:
            print "Key error occured"
            return
        except AttributeError:
            print "Attribute error occured!!"
            return        
        except NameError:
            print "Name error occured!!"
            return        
        except:
            print "Error occured!!"
            return   
    
    # This code is referred from stackoverflow
    def scrape_google(self, query, file_name):  
        print "Scraping google to find images for the location ",query
        image_type="ActiOn"
        query= query.split()
        query='+'.join(query)
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        #print url
        #add the directory for your image here
        DIR="jythonMusic\Pictures"
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = self.get_soup(url,header)
        
        ActualImages=[]# contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
            break
        
        #print  "there are total" , len(ActualImages),"images"
        
        if not os.path.exists(DIR):
                    os.mkdir(DIR)
        #DIR = os.path.join(DIR, query.split()[0])
        
        if not os.path.exists(DIR):
                    os.mkdir(DIR)
        ###print images
        for i , (img , Type) in enumerate( ActualImages):
            try:
                req = urllib2.Request(img, headers={'User-Agent' : header})
                raw_img = urllib2.urlopen(req).read()
        
                cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
                print cntr
                if len(Type)==0:
                    f = open(os.path.join(DIR , str(file_name)+".jpg"), 'wb')
                else :
                    f = open(os.path.join(DIR , str(file_name)+"."+Type), 'wb')
                print "Image downloaded"
                f.write(raw_img)
                f.close()
            except Exception as e:
                print "could not load : "+img
                print e    
    
        print "Kindly run the program file textSonification.py, located in the jythonMusic folder, from the JEM editor for the third part of the good performance section"
    
    def plot_graph(self):
        names_plot_x = []
        names_plot_y = []
        
        #self.interactions = ['Pari Banou interrupted Prince Ahmed', 'Beder Akriti Sit thanked Abdallah', 'Pari Banou interrupted Prince Ahmed', 'Schaibar was Pari', 'Danhasch left Maimoune', 'Pari Banou interrupted Prince Ahmed']
        for item in self.interactions:
            item = item.strip()       
        
        try:
            for item in self.interactions:
                name1 = ""
                name2 = ""
                splitted_item = item.split()
                for i in range(0,len(splitted_item)):
                    if splitted_item[i][0].islower():
                        name1_temp = splitted_item[0:i]
                        for name in name1_temp:
                            name1 = name1 + " " +name
                        break
                
                name2_temp = splitted_item[i+1:]
                
                for name in name2_temp:
                    name2 = name2+ " " + name
                  
                names_plot_x.append(name1)
                names_plot_y.append(name2)
            
            
            master_list = []
            for i in range(0, len(names_plot_x)):
                master_list.append(names_plot_x[i].strip()+" "+names_plot_y[i].strip())
                
            
            count = Counter(master_list)        
            
            final_dict = []
            
            temp_list = []
            for i in range(0, len(names_plot_x)):
                temp = (names_plot_x[i].strip()+" " +names_plot_y[i].strip()).strip()
                temp_count = count[temp]
                
                if temp not in temp_list: 
                    final_dict.append({'name1': names_plot_x[i].strip(), 'name2': names_plot_y[i].strip(), 'frequency': temp_count})
                
                temp_list.append(temp)
            
            names_plot_x_unique = list(set(names_plot_x))
            names_plot_y_unique = list(set(names_plot_y))
            a = (len(names_plot_x_unique), len(names_plot_y_unique))
            plot_graph = np.zeros(a)
            
            print "Frequency of occurences of the corresponding name-name pairs is:"
            for item in final_dict:
                print "Name1: ",item['name1']
                print "Name2: ",item['name2']
                print "Number of occurences: ",item['frequency']            
            
            print "---------------------------------------------------------------------------------------------"
            print "Plotting the graph for showing the interactions between PERSON and PERSON."
            
            for item in final_dict:
                index_x = names_plot_x_unique.index(" "+item['name1'])
                index_y = names_plot_y_unique.index(" "+item['name2'])
                
                plot_graph[index_x][index_y] = item['frequency']
                
            fig,ax = plt.subplots(1,1,figsize=(12,10))
            heatmap = ax.pcolor(plot_graph)
            
            ax.set_yticks(np.arange(plot_graph.shape[0])+0.5, minor=False)
            ax.set_xticks(np.arange(plot_graph.shape[1])+0.5, minor=False)
            
            ax.set_xticklabels(names_plot_x_unique, minor=False, rotation=45)
            ax.set_yticklabels(names_plot_y_unique, minor=False)
            
            plt.xlabel('Names of people')
            plt.ylabel('Names of people')  
            plt.title('Heatmap of interactions between people')        
            
            y_patch = mpatches.Patch(color='purple', label='No interactions')
            g_patch = mpatches.Patch(color='teal', label='1 interaction')
            b_patch = mpatches.Patch(color='yellow', label='2 interactions')
            plt.legend(handles=[y_patch,g_patch,b_patch])
            
            mng = plt.get_current_fig_manager()
            #mng.resize(*mng.window.maxsize())
            
            plt.show()      
        except urllib2.HTTPError:
            print("You may have selected an audio book!")
            return
        
        except KeyError:
            print "Key error occured"
            return
        except AttributeError:
            print "Attribute error occured!!"
            return        
        except NameError:
            print "Name error occured!!"
            return        
        except:
            print "Error occured!!"
            return           
    
    def create_graph_location(self, names_plot_x, names_plot_y):
        #names_plot_x = ['Anne', 'Anne', 'Anne', 'Lady', 'Anne', 'Miss', 'Laura', 'Laura', 'Perpetual', 'Laura']
        #names_plot_y = ['London', 'Hampshire', 'London', 'London', 'London', 'Knowlesbury', 'Marian', 'Marian', 'Rosicrucian', 'London']
        #print "names_plot_x", names_plot_x
        #print "names_plot_y", names_plot_y
        
        try:
            
            master_list = []
            for i in range(0, len(names_plot_x)):
                master_list.append(names_plot_x[i].strip()+" "+names_plot_y[i].strip())
                
            
            count = Counter(master_list)        
            
            final_dict = []
            
            temp_list = []
            for i in range(0, len(names_plot_x)):
                temp = (names_plot_x[i].strip()+" " +names_plot_y[i].strip()).strip()
                temp_count = count[temp]
                
                if temp not in temp_list: 
                    final_dict.append({'name': names_plot_x[i].strip(), 'location': names_plot_y[i].strip(), 'frequency': temp_count})
                
                temp_list.append(temp)
            
            print "Frequency of occurences of the corresponding name-location pairs (for 10 records) is:"
            for item in final_dict:
                print "Name: ",item['name']
                print "Location: ",item['location']
                print "Number of occurences: ",item['frequency']
            
            #print final_dict
            
            names_plot_x_unique = list(set(names_plot_x))
            names_plot_y_unique = list(set(names_plot_y))
            a = (len(names_plot_x_unique), len(names_plot_y_unique))
            plot_graph = np.zeros(a)
            #print plot_graph
            
            for item in final_dict:
                index_x = names_plot_x_unique.index(item['name'])
                index_y = names_plot_y_unique.index(item['location'])
                
                plot_graph[index_x][index_y] = item['frequency']
                
            #print plot_graph
            
            fig,ax = plt.subplots(1,1,figsize=(12,10))
            heatmap = ax.pcolor(plot_graph)
            
            ax.set_yticks(np.arange(plot_graph.shape[0])+0.5, minor=False)
            ax.set_xticks(np.arange(plot_graph.shape[1])+0.5, minor=False)
            
            ax.set_xticklabels(names_plot_x_unique, minor=False, rotation=45)
            ax.set_yticklabels(names_plot_y_unique, minor=False)
            
            plt.xlabel('Names of people')
            plt.ylabel('Location')  
            plt.title('Heatmap of relations between people and locations')        
            
            y_patch = mpatches.Patch(color='purple', label='No interactions')
            g_patch = mpatches.Patch(color='darkslateblue', label='1 interaction')
            a_patch = mpatches.Patch(color='mediumseagreen', label='2 interactions')
            b_patch = mpatches.Patch(color='yellow', label='3 interactions')
            plt.legend(handles=[y_patch,g_patch,a_patch,b_patch])
            
            mng = plt.get_current_fig_manager()
            #mng.resize(*mng.window.maxsize())
            
            plt.show()      
            
        except urllib2.HTTPError:
            print("You may have selected an audio book!")
            return
        
        except KeyError:
            print "Key error occured"
            return
        except AttributeError:
            print "Attribute error occured!!"
            return        
        except NameError:
            print "Name error occured!!"
            return        
        except:
            print "Error occured!!"
            return       
    
#obj_retrieve = Interaction_Retrieval()
#obj_retrieve.scrape_web()
#obj_retrieve.create_graph_location()