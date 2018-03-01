try:
   from music import *
   from image import *
except:
   print "Missing libraries!!"

##### define  musical parameters
scale = MIXOLYDIAN_SCALE
 
minPitch = 0        # MIDI pitch (0-127)
maxPitch = 127
 
minDuration = 0.8   # duration (1.0 is QN)
maxDuration = 6.0
 
minVolume = 0       # MIDI velocity (0-127)
maxVolume = 127
 
##### define function to sonify data file
# Returns list of notes from sonifying the temperature values of each month
def get_notes(name = 'data.csv'):
   theme = Phrase()
   theme.setTempo(120)
   with open(name, 'r') as inputFile:
      #skipping the header in the file
      next(inputFile)
      count = 0
      pitches = []
      duration = 0
      for line in inputFile:
         
         if count != 0 and count%2 == 0:
            #add chord consisting of 2 pitches and duration, each cord is a sonified temperature info of 2 months
            theme.addChord(pitches, duration/12.0)
            
            #reset pitches and duration after every 2 values
            pitches = []
            duration = 0
         
         line = line.replace('"','')
         row = line.split(",")
         # map avg temperature to pitch, more the temperature higer pitched the sound will be
         pitch = mapScale(float(row[7]), 6, 21, minPitch, maxPitch, scale)
       
         # map max temperature value to duration, more the temperature longer the chord will play
         duration += mapValue(float(row[8]), 9, 28, minDuration, maxDuration)
         
         pitches.append(pitch)
         count+=1
         
   return theme

# Sonify temperature data file and play the theme
Play.midi(get_notes())