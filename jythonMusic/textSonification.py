from music import *
from random import *
import pickle
from image import *
import sys
 
# Define text to sonify.

image_doc = pickle.load(open("imagesAndData\image_doc.pickle", 'rb'))

display_options = ""
for key in image_doc.keys():
   display_options = str(key) + ": " + str(image_doc[key])+"\n"

display_options = display_options + "Kindly input a choice"
text = ""
choice = int(raw_input(display_options))
try:
   text = image_doc[int(choice)] 
except:
   print "Invalid input"
   
print "text",text
if text!= " ":
      
   ##### define the data structure
   textMusicScore  = Score("Moby-Dick melody", 130)
   textMusicPart   = Part("Moby-Dick melody", GLOCK, 0)
   textMusicPhrase = Phrase()
    
   # create durations list (factors correspond to probability)
   durations = [HN] + [QN]*4 + [EN]*4 + [SN]*2
    
   ##### create musical data
   for character in text:  # loop enough times
    
      value = ord(character)         # convert character to ASCII number
    
      # map printable ASCII values to a pitch value
      pitch = mapScale(value, 32, 126, C3, C6, PENTATONIC_SCALE, C2)
    
      # map printable ASCII values to a duration value
      index = mapValue(value, 32, 126, 0, len(durations)-1)
      duration = durations[index]
    
      print "value", value, "becomes pitch", pitch,
      print "and duration", duration
    
      dynamic = randint(60, 120)    # get a random dynamic
    
      note = Note(pitch, duration, dynamic)   # create note
      textMusicPhrase.addNote(note)  # and add it to phrase
    
   # now, all characters have been converted to notes   
    
   # add ending note (same as last one - only longer)
   note = Note(pitch, WN)
   textMusicPhrase.addNote(note)   
   print "The program may take some time to execute due to the large size of the image!"
   try:
      image = Image("Pictures/"+repr(choice-1)+".jpg")
   except:
      image = Image("Pictures/"+repr(choice-1)+".png")
   
   ##### combine musical material
   textMusicPart.addPhrase(textMusicPhrase)
   textMusicScore.addPart(textMusicPart)
   
   ##### view score and write it to a MIDI file
   View.show(textMusicScore)
   Play.midi(textMusicScore)
   Write.midi(textMusicScore, "textMusic.mid")