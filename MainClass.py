try:
    from FleschReadingTest import Environment
    from FleschReadingTest import Agent
    from InteractionRetreival import Interaction_Retrieval
    from plotMinimal import makeGraph
    
except:
    print "Kindly place all the classes in one folder!"



class Main_class:
    def take_input(self):
        
        print "Hello!!"
        
        while True:            
            print "---------------Minimal performance------------------"
            print "1. Display graph for the visualization of global warming trends"
            print "---------------Satisfactory performance------------------"
            print "2. Display the FRES score of a sentence entered by the user"
            print "3. Display the FRES score of a wide range of books from Project Gutenberg website"
            print "---------------Baseline performance------------------"
            print "4. Visualize interactions between characters from the book 'The Woman in White' by Wilkie Collins"
            print "5. Display relations between the two entities: PERSON and LOCATION"
            print "---------------Good performance------------------"
            print "6. Using LOCATIONs as the Google search key, display an image for the same. Also generate music for the sentence."
            print "7. Terminate the program"
            
            try:
                choice = int(raw_input("Kindly enter your choice\n"))
            except ValueError:
                print "Invalid input entered! Kindly input an integer value!"
                continue
            
            try:
                
                if choice == 1:
                    obj = makeGraph()
                    obj.create_graph()
                    
                elif choice == 2:
                    input_sent = raw_input("Enter the sentence for which you want to calculate the FRES score\n")
                    print "......................Computation in progress..............................."
                    flesch_agent = Agent()
                    output = flesch_agent.fres_score(input_sent)
                    print "The FRES score for the entered sentence is ", output[0]
                    print "The grade for the entered sentence is ", output[1]
                    
                elif choice == 3:
                    flesch_env = Environment()                
                    flesch_env.read_input()
    
                elif choice == 4:
                    interact_retrieve = Interaction_Retrieval()
                    interact_retrieve.scrape_web()
                    interact_retrieve.process_content()
                    
                elif choice == 5:
                    interact_retrieve = Interaction_Retrieval()
                    interact_retrieve.scrape_web()
                    interact_retrieve.location_people()                
                elif choice == 6:
                    interact_retrieve = Interaction_Retrieval()
                    interact_retrieve.scrape_web()
                    interact_retrieve.location_people()
                    interact_retrieve.pass_locations()               
                    
                elif choice == 7:
                    print "Bye Bye!! Have a good day!!"  
                    break        
                else:
                    print "You entered an invalid option. Please try again!!"
                    continue
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
        
obj = Main_class()
obj.take_input()