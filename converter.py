from sre_constants import SUCCESS
from turtle import width
from PIL import Image

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


# ascii characters used to build the output text
ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", "a", ",", "!"]


'''
The following class creates the GUI for converting an image file into ASCII art. User simple just need 
to select the image file for converting. As the process starts, messages will pop out in text box to the user
to show the the progress or any errors.
'''

class GUI:
    def __init__(self, frame):

        #Create main GUI frame using tkinter
        self.frame=frame
        frame.title("Image to ASCII Art")
        frame.geometry('800x568')

        self.label_instrut= tk.Label(frame, text="\nHOW TO USE:\n Simply click the Open file button to select desired image to start the process.")
        self.label_instrut.pack()

        self.open_button = ttk.Button(frame,text='Open an image File',command=self.select_image)
        self.open_button.pack()
        self.textbox = tk.Text(frame, width=50, height=5, bg='black', fg='white')
        self.textbox.pack()
        self.label_break= tk.Label(frame, text="\n_______________________________________________________________________________"
                                                    "____________________________________________________________________________\n")
        self.label_break.pack()
        self.ascii_display = tk.Label(frame,text='', fg= "white", font=("Courier", 3))
        self.ascii_display.pack(ipadx=50, ipady= 10, fill='both')


    '''
    On button click, user go to corresponding image file location and select the file to start.
    '''
    def select_image(self):
        # accepted filetype, default are JPEG
        filetypes = (
        ('JPEG Image', '*.jpg'),
        ('PNG Image', '*.png'),
        ('All files', '*.*')
        )

        #getting the path of the image file
        filepath = fd.askopenfilename(
            initialdir='/',
            filetypes=filetypes)

        #Informing user the current process
        self.display_msg("      Starting Converting......\n")
        self.start(filepath)

    
    '''
    Update text to the tkinter text widget to inform user what is happening.
    '''
    def display_msg(self, msg):
        self.textbox.insert('end', msg)
        self.textbox.see('end')
    

    '''
    Show the final ascii result in the end of frame
    '''
    def show_ascii(self, string):
        self.ascii_display.config(text =string, background="black")
    
    '''
    Start the converting process
    '''
    def start(self, path):
        ascii_string=Converter(path, self.textbox).start()

        if ascii_string:
            self.show_ascii(ascii_string)
            self.display_msg("      Successful converting image to Ascii Art!\n")
        else: 
            self.display_msg("      Invalid image file, please try again!\n")

'''
The following class is actually handle the real work by converting the image file into
an sequence of ascii string.
'''
class Converter:

    def __init__(self, path, textbox):
        self.filepath = path
        # default resize width is 200 px
        self.width=200
        self.display=textbox

    '''
    resize image according to a new width and height with default ratio
    '''
    def image_resize(self,image):
        ratio = 43/42
        new_height = int(self.width * ratio)
        resize_image = image.resize((self.width, new_height))
        return(resize_image)

    '''
    convert each pixel to grayscale
    '''
    def grayscale(self,image):
        gray_image = image.convert("L")
        return(gray_image)
        
   
    '''
    convert pixels to a string of ascii characters
    '''
    def pixels_to_ascii(self, image):
        pixels = image.getdata()
        #loop through each pixel and find the corresponsing ascii charater
        ascii_ch = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
        return(ascii_ch)    

    
    def display_msg(self, msg):
        self.display.insert('end', msg)
        self.display.see('end')


    '''
    Start converting image file to an ascii string 
    '''
    def start(self):
        #handle not image file exception
        try:
            image =Image.open(self.filepath)
        except:
            self.display_msg("      Not a valid pathname to an image, please try again!\n")
            return

        new_image_data = self.pixels_to_ascii(self.grayscale(self.image_resize(image)))
        
        # format the string ascii charaters
        pixel_num = len(new_image_data)  
        ascii_image = "\n".join([new_image_data[index:(index+self.width)] for index in range(0, pixel_num, self.width)])
        
        return ascii_image


root= tk.Tk()
interface=GUI(root)
root.mainloop()
