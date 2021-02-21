from os import close
from tkinter import *
from tkinter import messagebox # to use it in iexit() function.
import json
from difflib import get_close_matches
import pyttsx3

# to initiate python text-to-speech class, we'll create a object of this class.
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# we can set volume of the voice and volume ranges from 0.0 to 1.0 
# we can set rate of speech(word speak in 1 minute) by default it is 200 wpm.
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

def speakWord(): 
    engine.say(entry_field.get())
    engine.runAndWait()

def speakMeaning(): 
    engine.say(textField.get(1.0, END))
    engine.runAndWait()

def iexit(): # this iexit() function is used as a command inside exitButton. to exit the window.
    result = messagebox.askyesno('Confirm', 'Do you want to exit?') # yes button will return True and No button will return False. and these value will be stored in result variable.
    if result == True:
        root.destroy() # to close the window.
    else:
        pass # it will do nothing.

def clearText(): # this function is used in clearButton as a command to clear all the text.
    # whatever text present in entry_field and textField will be deleted.
    # again making the state normal(enabled) because we are clearing the text inside textField
    textField.config(state = NORMAL)
    entry_field.delete(0, END) # form 0th position to end position.
    textField.delete(1.0, END) # why 1.0 ? => may be this is second text field that's why 1.0.
    textField.config(state = DISABLED)
    
def searchMeaning(): # this function is used in searchButton as a command to search the meaning of the given word.
    # we'll use data.json file searching the meaning. data.json contains data in form of dictionary, in which word are in form of key and their meaning are in form of value of that key.
    data = json.load(open('data.json'))
    inputWord = entry_field.get()
    inputWord = inputWord.lower()
    
    if inputWord in data: # if the given word is present in data(data variable contain data.json file), do the below
        # textField.insert(END, data[inputWord]) # insert the meaning of given word. we are accessing value for the given key from dict.
        
        # to print the result in seperate line and without curly braces (of dict.)
        meaning = data[inputWord]
        
        # again making the state normal(enabled) because we are inserting the text inside textField
        textField.config(state = NORMAL)
        # just before adding the meaning, we'll delete if any text is present in textField.
        textField.delete(1.0, END)
        # Now we'll add meaning on the textField.
        for item in meaning: # meaning is a list here containing multiple item and we have to access each item in a new line.
            textField.insert(END, u'\u2022 ' + item + '\n\n') # 2022 is code to create a bullet symbol. u is for string. \n\n is for new line after each complete sentence.
        
        # we'll disable the state of textField so that no one can edit the textField, else user can change the text present inside textField
        textField.config(state = DISABLED)
    
    # what if user enterd a word which is not correct, we'll provide a close match for that word. by using close match module which is present in difflib package.
    # ''' How get_close_matches() works.? 
    #         it takes 4 arguments , 2 compulsary and 2 optional
    #         get_close_matches(
    #         1st argument -> 'the wrong word for which we want close matches', 
    #         2nd argument ->'a list from which it'll search for close matches', 
    #         3rd argument -> we will give n value. eg- n = 3 , then it'll give max 3 answers.,
    #         4th argument -> cutoff = 0.6 # by default cutoff value is 0.6. cutoff value lies between 0.0 to 1.0 , value closer to 1.0 will give more accurate result.)
    # '''
    elif len(get_close_matches(inputWord, data.keys(), n = 1, cutoff = 0.8)) > 0: # if the close matches list contains atleast 1 word then lenth will be greater than 0
        close_match = get_close_matches(inputWord, data.keys(), cutoff = 0.8)[0] # accessing the first word from close_match, because 1st word is more accurate than the rest.
        # we'll display the close match word in a message box
        correct = messagebox.askyesno('Confirm', 'Did you mean ' + close_match + ' instead.?')
        if correct == True:
            correct_meaning = data[close_match]
            entry_field.delete(0, END) # deleting the entry_field to replace the wwrong word.
            entry_field.insert(END, close_match) # inserting the correct word i.e close_match
            textField.delete(1.0, END) # deleting the text in textField to update it with correct meaning for given word.
            
            # again making the state normal(enabled) because we are inserting the text inside textField
            textField.config(state = NORMAL)
            for item in correct_meaning: # inserting multiple meaning line by line.
                textField.insert(END, u'\u2022 ' + item + '\n\n')
                
            textField.config(state = DISABLED) # disable the textField.
        else:
            textField.delete(1.0, END)
            messagebox.showinfo('Information', 'Please type a correct word.')
            entry_field.delete(0, END) # deleting the entry_field so that user can type again .
    else:
        textField.delete(1.0, END)
        messagebox.showerror('Error', 'This word does not exist in our database.')
        entry_field.delete(0, END) # deleting the entry_field so that user can type again .
        
            
            

''' GUI Part Starts Here '''
# we'll init. object of TK() class
root = Tk()

# now we'll set the size of window using geometry('width * height') class.
root.geometry('1000x650+450+180')
# to fix the size of windows (to switch off the maximize button)
# we are passing false value for width and height so that there will be no change in width and height
root.resizable(0, 0)
# setting title to the titlebar
root.title('Talking Dictionary ~ Created With ❤ By Aman')
# this mainloop will keep our window on infinite loop, and we can see window till we closed it.

# to set the background image, we'll use PhotoImage() class.
background_image = PhotoImage(file = 'bg.png')
# to use this image, we have to place it on a label so now we'll create a Label() class
background_label = Label(root, image = background_image) # label will be on root window
# now we have to place this label
background_label.place(x = 0, y = 0)

# placing a Enter Word Text 
EnterWordLabel = Label(root, text = "Enter Word", font = ('Kristen ITC', 25, 'bold'), fg = 'red3', bg = 'whitesmoke')
EnterWordLabel.place(x = 600, y = 50)
# now we'll create entry_field for taking user input Word.
entry_field = Entry(root, font = ('FangSong', 15), bd = 5, relief = GROOVE, justify = CENTER) # border = bd, relief is a design for border
# by default cursor in the entry_field will blink in the left hand side.
# that's why we use justify = CENTER , so that it'll blink at the center.

# by default cursor is not pointed on the entry_field.we have to click on the field for pointing the cursor. to change this thing, we'll do the below
entry_field.focus_set()

# Now we'll upload pictures for icons.
searchImage = PhotoImage(file = 'search.png')
# now we'll use Button() class by creating an object of this class.
searchButton = Button(root, image = searchImage, bd = 0, bg = 'whitesmoke', activebackground = 'whitesmoke', cursor = 'hand2', command = searchMeaning)
searchButton.place(x = 620, y = 150)

enterWord_micImage = PhotoImage(file = 'mic.png')
enterWord_micButton = Button(root, image = enterWord_micImage, bd = 0, bg = 'whitesmoke', activebackground = 'whitesmoke', cursor = 'hand2', command = speakWord)
enterWord_micButton.place(x = 720, y = 154)
entry_field.place(x = 591, y = 110)

# placing a Meaning Text 
MeaningLabel = Label(root, text = "Meaning", font = ('Kristen ITC', 25, 'bold'), fg = 'red3', bg = 'whitesmoke')
MeaningLabel.place(x = 629, y = 250)

# Now we'll create the TextField.
textField = Text(root, font = ('FangSong',16,'bold'), height = 10, width = 38, bd = 3, relief = GROOVE, wrap = 'word')
# by default at the end of the line, each letter will start going in the next line instead of each word. to fix this, we'll do this. wrap = 'word'
textField.place(x = 463, y = 300)

# Now setting up the buttons.

audio_micImage = PhotoImage(file = 'audio.png')
audio_micButton = Button(root, image = audio_micImage, bd = 0, bg = 'whitesmoke', activebackground = 'whitesmoke', cursor = 'hand2', command = speakMeaning)
audio_micButton.place(x = 530, y = 563)

clearImage = PhotoImage(file = 'clear.png')
clearButton = Button(root, image = clearImage, bd = 0, bg = 'whitesmoke', activebackground = 'whitesmoke', cursor = 'hand2', height = 50, width = 50, command = clearText)
clearButton.place(x = 660, y = 562)

exitImage = PhotoImage(file = 'exit_2.png')
exitButton = Button(root, image = exitImage, bd = 0, bg = 'whitesmoke', activebackground = 'whitesmoke', cursor = 'hand2', height = 50, width = 50, command = iexit)
# iexit is a function defined above.
exitButton.place(x = 800, y = 562)

''' Binding Keyboard Key With Button.'''
# attaching enetr key with searchButton.
def enter_function(event):
    searchButton.invoke()
# whenever we'll press enterkey this enter_function will be called. and this function will invoke the askButton.
# To bind the ask button with Enter key. so that on pressing Enter key the button will work.
root.bind('<Return>', enter_function)  # Enter is represented like Return.


# attaching backspace key with clearButton.
def backspace_function(event):
    clearButton.invoke()
root.bind('<BackSpace>', backspace_function) 

# attaching esc key with exitButton.
def exit_function(event):
    exitButton.invoke()
root.bind('<Alt-F4>', exit_function) 
# attaching Alt-F4 key with exitButton.
def exit_function(event):
    exitButton.invoke()
root.bind('<Escape>', exit_function) 

''' Binding Keyboard Key With Button End Here...'''

''' GUI Part Ends Here '''

root.mainloop()
