import matplotlib.pyplot as plt
import numpy as np

class makeGraph:
    def create_graph(self):
        
        temperature = []
        year = []
        
        with open("data.csv", 'r') as inputFile:
            #skipping the header in the file
            next(inputFile)
            for line in inputFile:
        
                line = line.replace('"','')
                row = line.split(",")
                year.append(str(row[6]))
                temperature.append(float(row[7]))
        
        fig,ax = plt.subplots(1,1,figsize=(12,10))
        
        # create some x data and some integers for the y axis
        y = temperature
        x = np.arange(len(year))
        
        # tell matplotlib which yticks to plot 
        ax.set_xticks(x)
        
        # labelling the yticks according to the list
        labels = [item.get_text() for item in ax.get_xticklabels()]
        for i in range(0, len(year)):
            labels[i] = year[i]              
            
            
        plt.gcf().subplots_adjust(bottom=0.15)
        ax.set_xticklabels(labels, minor = False)   
        plt.xlabel('Year')
        plt.ylabel('Temperature')  
        plt.title('Temperature V/S Year graph')
        
        # plot the data
        ax.plot(x,y)        
        plt.show()    
