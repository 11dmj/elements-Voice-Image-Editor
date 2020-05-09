import tkinter as tk
from tkinter import *
import queue
import speech_recognition as sr
from pocketsphinx import LiveSpeech
import threading
import time
from nltk import word_tokenize
import pyttsx3
import sys
from tkinter import messagebox
import PIL
from PIL import Image,ImageTk, ImageEnhance, ImageDraw, ImageFont, ImageFilter
from pygame import mixer
#from IPython.utils import frame
from tkinter import filedialog as fd
import urllib
import pyaudio
import os
from sys import platform
import random
import keyboard
import pynput
from pynput.keyboard import Key,Listener
from tkinter import colorchooser
from tkfontchooser import askfont
import math
from tkinter.commondialog import Dialog
#all global variables are initialized with none to make them global variables 
root=None
hello_label=None
operation_label=None
listening=None ##it's the flag to perform listen operation in while loop
q=queue.Queue()  ##queue for basic thread operation is intialized to a vasriable
chat_value= None ##this variable is for text to speech chat
main_frame=None
current_img= None
qualityenter=None
file_path_string=None
filenameget=None
extentionget=None
qualityget=None
text_colour=None
internet_access=None
first_time = True
import_win=None
get_colour_Box=None
w_board=None
h_board=None
board_colour=None
paper_set_canvas=None
text_newcl_button=None
original_img=None
current_img=None
canvasfilter=None
##This is the code to setup and initialize pyttsx3 for text tp speech
engine=pyttsx3.init('sapi5')  ##sapi5 (by microsoft) is like gtts: google text to speech, by google 
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)   ##here the voices list contain either 0 or 1 , voices[0] is male voice

def connection2():
    global first_time
    global internet_access
    global main_frame
    canvasstatus = Canvas(main_frame, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0" )
    canvasstatus.place(x="905", y="734", relwidth="0.3", relheight="0.45")
    #check status
    host='http://google.com'
    try:
        urllib.request.urlopen(host)
        print("connected")
        #if first_time == True:
        connectionLabel=Label(canvasstatus,bg="#0d0d0d",fg="white",text="Connection Established")
        connectionLabel.pack()
        closingLabel=Label(canvasstatus,bg="#0d0d0d",fg="white",text="voice enabled")
        closingLabel.pack()
        canvasstatus.after(10000, canvasstatus.destroy)
            #first_time = False
        #internet_access = True
    except:
        print("not_connected")
        #if first_time == True:
        connectionLabel=Label(canvasstatus,bg="#0d0d0d",fg="white",text="NoConnection Err: 404")
        connectionLabel.pack()
        closingLabel=Label(canvasstatus,bg="#0d0d0d",fg="white",text="quit to close/ continue without voice")
        closingLabel.pack()
        quitButton=Button(canvasstatus,bg="#0d0d0d",fg="white",text="Quit",command=root.destroy)
        quitButton.pack()
        canvasstatus.after(10000, canvasstatus.destroy)
            #first_time = False
        #internet_access = False


#Hover button Class 
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        # self[foreground]="white"
        # self.[activeforeground]="blue"
        tk.Button.__init__(self,master=master,**kw)
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['foreground'] = self['activeforeground']

    def on_leave(self, e):
        self['foreground'] = self.defaultForeground

# option not used
class MyOptionMenu(OptionMenu):
    def __init__(self, master, status, *options):
        self.var = StringVar(master)
        self.var.set(status)
        OptionMenu.__init__(self, master, self.var, *options)
        self.config(font=('calibri',(10)),bg='#1a1a1a',width=16, activebackground="#2a2a2a", bd ="0", fg = "white")
        self['menu'].config(font=('calibri',(10)),bg='#1a1a1a', bd = "0", fg = "white")



# Colour Picker tkinter class
# __all__ = ["Chooser", "askcolor"]

class Chooser(Dialog):
    #"Ask for a color"

    command = "tk_chooseColor"

    def _fixoptions(self):
        try:
            # make sure initialcolor is a tk color string
            color = self.options["initialcolor"]
            if isinstance(color, tuple):
                # assume an RGB triplet
                self.options["initialcolor"] = "#%02x%02x%02x" % color
        except KeyError:
            pass

    def _fixresult(self, widget, result):
        # result can be somethings: an empty tuple, an empty string or
        # a Tcl_Obj, so this somewhat weird check handles that
        if not result or not str(result):
            return None, None # canceled

        # to simplify application code, the color chooser returns
        # an RGB tuple together with the Tk color string
        r, g, b = widget.winfo_rgb(result)
        # return (r/256, g/256, b/256), str(result)
        return str(result)

def exit_func():
        global listening
        if listening==1:
            pass
        else:
            sys.exit(1)
            root.destroy()



##this is the main function which is called and the listen thread starts from here.
def Gui():
    global chat_value  ##wherever we need global variable, we must first set them to none as mentioned above and then code
                        ##for eg."global chat_value"  in functions wherever necessary 
    global root
    global hello_label
    global operation_label
    global main_frame
    ###############################################   GUI   ######################################################################
    root=tk.Tk()
    
    root.geometry("1200x800+150+10")
    root.wm_attributes("-topmost",1)
    root.title("Elements Voiced Image Editing")
    root.iconbitmap(r"elements2.0Images1\icons\logofull2_1TB_icon.ico")
    root.overrideredirect(0)
    topbar= Frame(main_frame,bg="#0d0d0d")
    topbar.pack(side=TOP,fill=X)
    close_button= Button(topbar,text="X",bg="blue",fg="black",command=lambda: root.destroy())
    close_button.pack(side=RIGHT)
    main_frame= Frame(root,bg="#0d0d0d")
    main_frame.pack(fill=BOTH, expand=1)
    chat_value="Welcome to Elements"
    chat(chat_value)
    hello_label=Label(main_frame,bg="#0d0d0d",bd="1",highlightthickness="1",fg="white",text="Welcome to Elements")
    hello_label.pack(side=BOTTOM,fill=X)
    operation_label=Label(main_frame,text=None,fg="Red")
    operation_label.pack(side=BOTTOM,fill=X)

    connection2()
    # splash_thread=threading.Thread(target=splash)
    # splash_thread.start()
    # splash_thread.join()
    #Undo and Redo
    Undo=[]
    Redo=[]

    canvas1 = Canvas(main_frame, bg="black", bd="0", borderwidth = "0", highlightthickness = "0" )
    canvas1.place(x="30", y="30", relwidth="0.85", relheight="0.75")
    labelshow = Label(canvas1, bg="black", bd="0", borderwidth = "0", highlightthickness = "0",image= None)
    labelshow.pack(fill= BOTH)

    def askcolor(color = None, **options):
    #"Ask for a color"
        global text_newcl_button
        global text_colour
        if color:
            options = options.copy()
            options["initialcolor"] = color
        #global text_colour
        text_colour = Chooser(**options).show()
        text_newcl_button.config(bg = text_colour)

    def import_options():
        global import_win
        import_win = Toplevel(root)
        import_win.overrideredirect(1)
        import_win.wm_attributes("-topmost",1)
        import_win.title("Import image")
        import_win.iconbitmap(r"elements2.0Images1\icons\logofull2_1TB_icon.ico")
        import_win.geometry("900x500+400+200")
        # import_win.maxsize(900,500)
        import_win.resizable(FALSE,FALSE)                                                                                          ## Disable resizing
        import_win.config(bg="#1c1c1c")
        import_win.grab_set()                                                                                                   ## prevent duplication of same window and block main window
        
        ## Import Image / fresh start in new banner
        imp_label=Label(import_win,fg="white",bg="#1c1c1c",text="IMPORT/CREATE BOARD",font=("Courier", 35))
        imp_label.place(x="30",y="30")

        ############################################## Left canvas
        # import canvas left
        imp_canvas = Canvas(import_win, bg="#1f1f1f", bd="0", borderwidth = "0", highlightthickness = "0")
        imp_canvas.place(x="30", y="90", relwidth="0.23", relheight="0.72")

        # info label import
        imp_det_label=Label(imp_canvas,fg="white",bg="#1f1f1f",text="Import image and \ncontinue editing \nor\nUse Canvas for fresh Start \n \nMake collages and Create", justify=LEFT)
        imp_det_label.place(x="30",y="30")

        # import button import win
        import_win_button = HoverButton(imp_canvas,  bg = "#FF6B26", bd="0", text = "Import", compound= "left",fg ="white",width ="13", height ="2",command=lambda: import_clicked())
        import_win_button.place(x="30", y="240")    

        #fresh start button import win
        import_win_canvas_button = HoverButton(imp_canvas,  bg = "#FF6B26", bd="0", text = "Create Board", compound= "left",fg ="white",width ="13", height ="2",command=lambda: new_board())
        import_win_canvas_button.place(x="30", y="290")

        ############################################ Right board Canvas
        #canvas board right
        board_canvas = Canvas(import_win, bg="#1f1f1f", bd="0", borderwidth = "0", highlightthickness = "0")
        board_canvas.place(x="260", y="90", relwidth="0.685", relheight="0.72")

        # info label board
        imp_det_board_label=Label(board_canvas,fg="gray",bg="#1f1f1f",text="Board Settings/customise Board")
        imp_det_board_label.place(x="20",y="10")

        # info label board info paper
        imp_det_board_paper_label=Label(board_canvas,fg="gray",bg="#1f1f1f",text="Paper Size Ratio Comparison\nSelect Paper", justify=LEFT)
        imp_det_board_paper_label.place(x="20",y="30")

        # Select Paper drop down menu
        ## setting size for preview
        A10 = 74.00, 105.00
        A9 = 105.00, 147.00
        A8 = 147.00, 210.00
        A7 = 210.00, 298.00
        A6 = 298*0.7, 420*0.7
        A5 = 420*0.5, 595*0.5
        A4 = 595*0.38, 842*0.38
        A3 = 842*0.28, 1191*0.28
        A2 = 1191*0.183, 1684*0.183
        A1 = 1684*0.14, 2384*0.14
        Square = 1000.00, 1000.00
        Small_Square = 500.00, 500.00
        A0 = 2384.000, 3370.000
        A02 = 3370.000, 4768.000
        A04 = 4768.000, 6741.000
        Custom = None, None
        ###(origin_x,orgin_y,width,height)

        # setting up paper preview
        # refreshes the paper size in preview
        
        def refresh_size():
            global get_colour_Box
            global w_board
            global h_board
            global board_colour
            board_colour = get_colour_Box.get("1.0","end-1c")
            paper_set_canvas.create_rectangle(0, 0, 1000,1000,fill="black")
            paper = var.get()
            ws,hs=paper.split()
            lenw = len(ws)
            lenh = len(hs)
            print (ws)
            print (hs)
            if ws == "('None'," or hs == "'None')":
                print ("custom active")
                custom_w = get_board_size_w.get("1.0","end-1c")
                custom_h = get_board_size_h.get("1.0","end-1c")
                w_board = custom_w
                h_board = custom_h
            else:
                w_board = float(ws[1:lenw-1])
                h_board = float(hs[0:lenh-1])
            orientation = orient.get()
            ## check orientation
            if orientation == "landscape":
                temp=w_board
                w_board=h_board
                h_board=temp
            print (w_board, "x", h_board)
            imp_det_board_paper_label.config(fg="white",bg="#1f1f1f",text="Paper Size Ratio Comparison\nSelect Paper : " +str(w_board) +" x" +str(h_board) , justify=LEFT)
            paper_set_canvas.create_rectangle(0, 0, w_board,h_board, fill= board_colour)

        # radio buttons for selecting paper 
        var = StringVar()
        A1_R=Radiobutton(board_canvas, text = "A1", variable = var, value = A1,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED,command= lambda : refresh_size())
        A1_R.pack(side=TOP)
        A2_R=Radiobutton(board_canvas, text = "A2", variable = var, value = A2,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A2_R.pack(side=TOP)
        A3_R=Radiobutton(board_canvas, text = "A3", variable = var, value = A3,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A3_R.pack(side=TOP)
        A4_R=Radiobutton(board_canvas, text = "A4", variable = var, value = A4,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A4_R.pack(side=TOP)
        A5_R=Radiobutton(board_canvas, text = "A5", variable = var, value = A5,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A5_R.pack(side=TOP)
        A6_R=Radiobutton(board_canvas, text = "A6", variable = var, value = A6,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A6_R.pack(side=TOP)
        A7_R=Radiobutton(board_canvas, text = "A7", variable = var, value = A7,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A7_R.pack(side=TOP)
        A8_R=Radiobutton(board_canvas, text = "A8", variable = var, value = A8,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A8_R.pack(side=TOP)
        A9_R=Radiobutton(board_canvas, text = "A9", variable = var, value = A9,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A9_R.pack(side=TOP)
        A10_R=Radiobutton(board_canvas, text = "A10", variable = var, value = A10,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        A10_R.pack(side=TOP)
        square_R=Radiobutton(board_canvas, text = "Square", variable = var, value = Square,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        square_R.pack(side=TOP)
        small_sq_R=Radiobutton(board_canvas, text = "Sm. Sq.", variable = var, value = Small_Square,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        small_sq_R.pack(side=TOP)
        custom_R=Radiobutton(board_canvas, text = "Custom", variable = var, value = Custom,bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED, command= lambda : refresh_size())
        custom_R.pack(side=TOP)

        # radio button For selecting orientation // label
        imp_det_board_orient=Label(board_canvas,fg="gray",bg="#1f1f1f",text="Change Orientation", justify=LEFT, font=("",14))
        imp_det_board_orient.place(x="20",y="90")
        orient = StringVar()
        landscape_R=Radiobutton(board_canvas, text = "Landscape", variable = orient, value = "landscape",bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED,command= lambda : refresh_size())
        landscape_R.place(x="20",y="120")
        portrate_R=Radiobutton(board_canvas, text = "portrate", variable = orient, value = "portrate",bg="#1f1f1f",fg="white",cursor="hand1",activebackground="#1f1f1f", activeforeground="white",selectcolor="#1f1f1a",state= DISABLED,command= lambda : refresh_size())
        portrate_R.place(x="100",y="120")

        # change background colour
        global get_colour_Box
        imp_det_board_page_colour=Label(board_canvas,fg="gray",bg="#1f1f1f",text="Change background", justify=LEFT, font=("",14))
        imp_det_board_page_colour.place(x="20",y="150")
        get_colour_Box=Text(board_canvas,height=2, width=10, bg="#1a1a1a" , bd="0", fg="gray")
        get_colour_Box.place(x="20", y="180", relwidth=".3", relheight="0.065")

        # custom board Size
        imp_board_size_label=Label(board_canvas,fg="gray",bg="#1f1f1f",text="Custom Board Size", justify=LEFT, font=("",14))
        imp_board_size_label.place(x="20",y="210")
        get_board_size_w=Text(board_canvas,height=2, width=10, bg="#1a1a1a" , bd="0", fg="gray")
        get_board_size_w.place(x="20", y="240", relwidth=".1365", relheight="0.065")
        get_board_size_h=Text(board_canvas,height=2, width=10, bg="#1a1a1a" , bd="0", fg="gray")
        get_board_size_h.place(x="120", y="240", relwidth=".1365", relheight="0.065")

        # fresh start button import win
        apply_win_canvas_button = HoverButton(board_canvas, bg = "white", bd="0", text = "Start Board", activeforeground="white",compound= "left",fg ="gray",width ="13", height ="2",state=DISABLED,command=lambda: apply_board())
        apply_win_canvas_button.place(x="20", y="290")

        # new board function, simply a plane space where back ground can be defined, later images can be imported into
        def new_board():
            global paper_set_canvas
            imp_det_board_label.config(fg="white")
            imp_det_board_paper_label.config(fg="white")
            # paper on canvas board
            paper_set_canvas = Canvas(board_canvas, bg="#1f1f1f", bd="0", borderwidth = "0", highlightthickness = "0", cursor= "plus")
            paper_set_canvas.place(x="350", y="10", relwidth="0.42", relheight="0.94")
            paper_set_canvas.config(bg="black")
            A1_R.config(state=ACTIVE)
            A2_R.config(state=ACTIVE)
            A3_R.config(state=ACTIVE)
            A4_R.config(state=ACTIVE)
            A5_R.config(state=ACTIVE)
            A6_R.config(state=ACTIVE)
            A7_R.config(state=ACTIVE)
            A8_R.config(state=ACTIVE)
            A9_R.config(state=ACTIVE)
            A10_R.config(state=ACTIVE)
            square_R.config(state=ACTIVE)
            small_sq_R.config(state=ACTIVE)
            custom_R.config(state=ACTIVE)
            landscape_R.config(state=ACTIVE)
            portrate_R.config(state=ACTIVE)
            imp_det_board_orient.config(fg="white")
            imp_det_board_page_colour.config(fg="white")
            get_colour_Box.config(fg="white")
            imp_board_size_label.config(fg="white")
            get_board_size_h.config(fg="white")
            get_board_size_w.config(fg="white")
            apply_win_canvas_button.config(activebackground = "#FF6B26",bg="white",fg= "#FF6B26",activeforeground="white", bd="0", text = "Apply Board",state= ACTIVE, command=lambda: apply_board())

        ## Apply
        def apply_board():
            global current_img
            global original_img
            # get board size
            w=  int (w_board)
            h=  int (h_board)
            shape = [(0,0), (w,h)] 
            
            # creating new Image object 
            board = Image.new("RGB", (w, h)) 
            
            # create rectangle image 
            board1 = ImageDraw.Draw(board)   
            board1.rectangle(shape, fill = board_colour) 

            width, height = board.size
            image_resized = resize_image(width, height,label_width,label_height,board)
            board_show = ImageTk.PhotoImage(image=image_resized)
            labelshow.image= board_show
            labelshow.config(image= board_show)
            current_img = board
            original_img = board

            # destroy unrequired
            import_label.destroy()
            import_win.destroy()

    # call for import option at begining
    import_options()

    #To resize image
    label_width = labelshow.winfo_screenwidth()
    label_height = labelshow.winfo_screenheight() - 264


    #image resize funtion
    def resize_image(width, height, label_width, label_height, image):
        factor_one = 1.0* (label_width / width)  
        factor_two =  1.0*(label_height / height)
        factor = min([factor_one, factor_two])
            # if the image resolution is smaller as the label resolution the function returns the original image
            # otherwise the function resize the image
        if factor_one > 1 and factor_two > 1 and factor_one <2 and factor_two <2:
            return image
        elif factor_one>2 and factor_two>2:
            width_resized = int( width*factor)
            height_resized = int(height*factor)
            return image.resize((width_resized, height_resized),Image.ANTIALIAS)
        else:
            width_resized = int( width*factor)
            height_resized = int(height*factor)
            return image.resize((width_resized, height_resized),Image.ANTIALIAS)

    def logobtn_clicked():
    
        logo_win = Toplevel(root)
        logo_win.overrideredirect(1)
        img1_logo = Image.open(r"elements2.0Images1\assets\otherImages\splashscreen.png")
        img1_logo = img1_logo.resize((900,400), Image.ANTIALIAS)
        photo_logo = ImageTk.PhotoImage(img1_logo)
        l1= Label(logo_win, bg="grey", image=photo_logo)
        l1.pack()
        close_button=HoverButton(logo_win,text="x",fg="#0d0d0d",activeforeground="black",command=lambda:close_logo_toplevel())
        close_button.pack(side=TOP,padx="890")
        l1.photo=photo_logo
        def close_logo_toplevel():
            logo_win.detroy()
        # logo_win.title("Credits")
        # logo_win.iconbitmap(r"elements2.0Images\logofull2_1TB_icon.ico")
        logo_win.geometry("900x400+400+200")
        # logo_win.maxsize(900,400)
        logo_win.after(5000,logo_win.destroy)

    #logo button
    img_logo = Image.open(r"elements2.0Images1\icons\elementslogo.png")
    img_logo = img_logo.resize((35,35), Image.ANTIALIAS)
    img_logo1 = ImageTk.PhotoImage(img_logo)
    button_img_logo = HoverButton(main_frame,  bg = "#0d0d0d", bd="0", image=img_logo1, command= logobtn_clicked)
    button_img_logo.place(x="10", y="670", relwidth=".05", relheight=".05")

        #import Image funtion
    def import_clicked():
        #import image first label has to be destroyed 
        import_label.destroy()     ## destroy import label

        name = fd.askopenfilename()
        image = Image.open(name)
        global current_img 
        current_img=image
        #img_frm = image.resize((1018,598), Image.ANTIALIAS)
        #current_img=img_frm
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        #current_img=image_resized
        img_frame = ImageTk.PhotoImage(image_resized)
        labelshow.image=img_frame
        labelshow.configure(image=img_frame)
        Undo.append(current_img)

        # import button         
    img_import = Image.open(r"elements2.0Images1\assets\operationsImages\save.png")
    img_import = img_import.resize((30,30), Image.ANTIALIAS)
    img_import1 = ImageTk.PhotoImage(img_import)
    button_import = HoverButton(main_frame,  bg = "#0d0d0d", bd="0", image=img_import1, command =import_clicked)
    button_import.place(x="40", y="705", relwidth=".05", relheight=".05")

    #Textbox to get input from the user!!
    textBox=Text(main_frame,height=2, width=10, bg="#1a1a1a" , bd="0", fg="white")
    textBox.place(x="125", y="705", relwidth=".3", relheight="0.065")

    #Get user input
    def retrieve_input():
        ########## original
        inputValue = textBox.get("1.0","end-1c")
        print(inputValue)
        return inputValue

    #side toolbar canvas
    canvastoolbar = Canvas(main_frame, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0" )
    canvastoolbar.place(x="1065", y="30", relwidth="0.123", relheight="0.755")

    #settings Canvas/ button
    def settings_clicked():
        # setting canvas
        canvassetting = Canvas(main_frame, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0" )
        canvassetting.place(x="950", y="30", relwidth="0.123", relheight="0.15")
        canvassetting.after(2000, canvassetting.destroy)
        #import button
        img_import = Image.open(r"elements2.0Images1\assets\operationsImages\save.png")
        img_import = img_import.resize((30,30), Image.ANTIALIAS)
        img_import1 = ImageTk.PhotoImage(img_import)
        img_import1.image=img_import1
        button_import = HoverButton(canvassetting,  bg = "#0d0d0d",text="Import",fg="gray",compound="left", bd="0", image=img_import1, command =import_clicked)
        button_import.place(x="30", y="0")

        #save button
        img_save = Image.open(r"elements2.0Images1\assets\operationsImages\save.png")
        img_save = img_save.resize((30,30), Image.ANTIALIAS)
        img_save1 = ImageTk.PhotoImage(img_save)
        img_save1.image=img_save1
        button_save = HoverButton(canvassetting,  bg = "#0d0d0d",text="Save as",fg="gray",compound="left", bd="0", image=img_save1, command =lambda: save_clicked())
        button_save.place(x="30", y="40")
 
        #logo button
        img_logo = Image.open(r"elements2.0Images1\icons\elementslogo.png")
        img_logo = img_logo.resize((35,35), Image.ANTIALIAS)
        img_logo1 = ImageTk.PhotoImage(img_logo)
        img_logo1.image=img_logo1
        button_logo = HoverButton(canvassetting,  bg = "#0d0d0d", bd="0",text="Logo    " ,fg="gray",compound="left",image=img_logo1, command= logobtn_clicked)
        button_logo.place(x="30", y="80")   

    #settings button
    img_settings = Image.open(r"elements2.0Images1\assets\operationsImages\settings.png")
    img_settings = img_settings.resize((30,32), Image.ANTIALIAS)
    img_settings1 = ImageTk.PhotoImage(img_settings)
    button_settings = HoverButton(canvastoolbar,bg="#0d0d0d", fg = "silver", bd="0", image=img_settings1,activeforeground='white', text = "Settings", compound= "left",command=settings_clicked)
    button_settings.place(x="15", y="0")

    #brightness Function
    def brightness_clicked():
        global current_img
        br=float(retrieve_input())
        img=ImageEnhance.Brightness(current_img)
        image=img.enhance(br)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        current_img=image
        bright_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= bright_img
        labelshow.configure(image= bright_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #brightness button
    img_brightness = Image.open(r"elements2.0Images1\assets\operationsImages\brightness.png")
    img_brightness = img_brightness.resize((30,32), Image.ANTIALIAS)
    img_brightness1 = ImageTk.PhotoImage(img_brightness)
    button_brightness = HoverButton(canvastoolbar, fg = "silver",activeforeground='white',  bg = "#0d0d0d", bd="0", image=img_brightness1, text = "Brightness", compound= "left",command=brightness_clicked)
    button_brightness.place(x="15", y="50")

    #rotatae button Function
    def rot_clicked():
        angle=retrieve_input() 
        global current_img    
        image= current_img.rotate(float(angle),expand=1)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        rotate_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= rotate_img
        labelshow.config(image= rotate_img)
        current_img=image
        Undo.append(current_img)
        #return current_img        

    #rotate button
    img_rotate = Image.open(r"elements2.0Images1\assets\operationsImages\rotate.png")
    img_rotate = img_rotate.resize((30,32), Image.ANTIALIAS)
    img_rotate1 = ImageTk.PhotoImage(img_rotate)
    button_rotate = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_rotate1, text = "Rotate", compound= "left", fg = "silver",activeforeground='white', command=rot_clicked)
    button_rotate.place(x="15", y="100")

    #crop Function
    def crop_clicked():
        global current_img
        width, height = current_img.size 
        #print ("Current size of image is", width, height) 
        print (" You need to Specify the Parameters of crop in pixels") 
        #listen left crop parameter
        print("Speak left crop" ) 
        #left = int(listen())
        left = int(retrieve_input())
        #left = int(input())
        print (left)
        #listen upper crop parameter
        print("Speak upper crop" )
        #upper =  int (listen())
        upper = int(retrieve_input())
        #upper = int(input())
        print (upper)
        #listen right crop parameter
        print("Speak right crop" )
        #right = int (listen())
        right = int(retrieve_input())
        #right = int(input())
        right = width - left
        print (right)
        #listen lower crop parameter
        print("Speak lower crop" )
        #lower = int (listen())
        lower = int(retrieve_input())
        #lower = int(input())
        lower = height - upper
        print (lower)
        #print("New size of image is", width, height)

        area = (left, upper, right, lower) 
        image = current_img.crop(area)  

        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        crop_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= crop_img
        labelshow.configure(image= crop_img)

        current_img=image   
        Undo.append(current_img)
        #return current_img     

    #crop button
    img_crop = Image.open(r"elements2.0Images1\assets\operationsImages\crop.png")
    img_crop = img_crop.resize((30,32), Image.ANTIALIAS)
    img_crop1 = ImageTk.PhotoImage(img_crop)
    button_crop = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_crop1, text = "Crop", compound= "left", fg = "silver",activeforeground='white',command=lambda: crop_clicked() )
    button_crop.place(x="15", y="150")

    #sharpness Function
    def sharpness_clicked(canvasfilter):
        sp = retrieve_input()
        print (sp)
        global current_img
        imbr = ImageEnhance.Sharpness(current_img)
        image = imbr.enhance(int (sp))
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        sharpness_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= sharpness_img
        labelshow.configure(image= sharpness_img)
        current_img=image
        Undo.append(current_img)
        canvasfilter.destroy()
        #return current_img
        
    #blur Function
    def blur_clicked():
        global current_img
        image = current_img.filter(ImageFilter.BLUR)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        blur_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= blur_img
        labelshow.configure(image= blur_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #enhance Function
    def enhance_clicked():
        global current_img
        image = current_img.filter(ImageFilter.EDGE_ENHANCE)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        enh_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= enh_img
        labelshow.configure(image= enh_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #smooth Function
    def smooth_clicked():
        global current_img
        image = current_img.filter(ImageFilter.SMOOTH)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        smth_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= smth_img
        labelshow.configure(image= smth_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #smooth more Function
    def smooth_more_clicked():
        global current_img
        image = current_img.filter(ImageFilter.SMOOTH_MORE)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        smth_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= smth_img
        labelshow.configure(image= smth_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #detail Function
    def detail_clicked():
        global current_img
        image = current_img.filter(ImageFilter.DETAIL)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        dtl_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= dtl_img
        labelshow.configure(image= dtl_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #emboss Function
    def embross_clicked():
        global current_img
        image = current_img.filter(ImageFilter.EMBOSS)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        emb_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= emb_img
        labelshow.configure(image= emb_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #contour Function
    def contour_clicked():
        global current_img
        image = current_img.filter(ImageFilter.CONTOUR)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        cntr_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= cntr_img
        labelshow.configure(image= cntr_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #saturation function
    def black_and_White_clicked():
        global current_img
        imbr = ImageEnhance.Color(current_img)
        image = imbr.enhance(0)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        bw_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= bw_img
        labelshow.configure(image= bw_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #filter specific buttons/  canvas
    def filter_clicked():
        #filter canvas
        canvasfilter = Canvas(main_frame, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0" )
        canvasfilter.place(x="950", y="230", relwidth="0.123", relheight="0.45")
        canvasfilter.after(3000, canvasfilter.destroy)
        #sharpness button
        img_sharp = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_sharp = img_sharp.resize((30,30), Image.ANTIALIAS)
        img_sharp1 = ImageTk.PhotoImage(img_sharp)
        img_sharp1.image=img_sharp1
        button_sharp = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_sharp1, text = "Sharpness", compound= "left", fg = "silver",activeforeground='white',command=lambda:sharpness_clicked(canvasfilter))
        button_sharp.place(x="30", y="0")

        #blur button
        img_blur = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_blur = img_blur.resize((30,30), Image.ANTIALIAS)
        img_blur1 = ImageTk.PhotoImage(img_blur)
        img_blur1.image=img_blur1
        button_blur = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_blur1, text = "Blur", compound= "left", fg = "silver",activeforeground='white',command=lambda:blur_clicked())
        button_blur.place(x="30", y="40")

        #enhance button
        img_enhance = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_enhance = img_enhance.resize((30,30), Image.ANTIALIAS)
        img_enhance1 = ImageTk.PhotoImage(img_enhance)
        img_enhance1.image=img_enhance1
        button_enhance = HoverButton(canvasfilter, bg = "#0d0d0d", bd="0", image=img_enhance1, text = "Enhance   ", compound= "left", fg = "silver",activeforeground='white',command=lambda:enhance_clicked())
        button_enhance.place(x="30", y="80")

        #smooth button
        img_smooth = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_smooth = img_smooth.resize((30,30), Image.ANTIALIAS)
        img_smooth1 = ImageTk.PhotoImage(img_smooth)
        img_smooth1.image=img_smooth1
        button_smooth = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_smooth1, text = "Smooth   ", compound= "left", fg = "silver",activeforeground='white',command=lambda:smooth_clicked())
        button_smooth.place(x="30", y="120")

        #smoothify button
        img_smooth_more = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_smooth_more = img_smooth_more.resize((30,30), Image.ANTIALIAS)
        img_smooth_more1 = ImageTk.PhotoImage(img_smooth_more)
        img_smooth_more1.image=img_smooth_more1
        button_smooth_more = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_smooth_more1, text = "Smoothify", compound= "left", fg = "silver",activeforeground='white',command=lambda:smooth_more_clicked())
        button_smooth_more.place(x="30", y="160")

        #detail button
        img_detail = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_detail = img_detail.resize((30,30), Image.ANTIALIAS)
        img_detail1 = ImageTk.PhotoImage(img_detail)
        img_detail1.image=img_detail1
        button_detail = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_detail1, text = "Details     ", compound= "left", fg = "silver",activeforeground='white',command=lambda:detail_clicked())
        button_detail.place(x="30", y="200")

        #emboss button
        img_embross = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_embross = img_embross.resize((30,30), Image.ANTIALIAS)
        img_embross1 = ImageTk.PhotoImage(img_embross)
        img_embross1.image=img_embross1
        button_embross = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_embross1, text = "Embross ", compound= "left", fg = "silver",activeforeground='white',command=lambda:embross_clicked())
        button_embross.place(x="30", y="240")

        #contour button
        img_contour = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_contour = img_contour.resize((30,30), Image.ANTIALIAS)
        img_contour1 = ImageTk.PhotoImage(img_contour)
        img_contour1.image=img_contour1
        button_contour = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_contour1, text = "Countour", compound= "left", fg = "silver",activeforeground='white',command=lambda:contour_clicked())
        button_contour.place(x="30", y="280")

        #black and white button
        img_bw = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
        img_bw = img_bw.resize((30,30), Image.ANTIALIAS)
        img_bw1 = ImageTk.PhotoImage(img_bw)
        img_bw1.image=img_bw1
        button_contour = HoverButton(canvasfilter,  bg = "#0d0d0d", bd="0", image=img_bw1, text = "Black&White", compound= "left", fg = "silver",activeforeground='white',command=lambda:black_and_White_clicked())
        button_contour.place(x="30", y="320")

    #filer button
    img_filter = Image.open(r"elements2.0Images1\assets\operationsImages\filter.png")
    img_filter = img_filter.resize((30,32), Image.ANTIALIAS)
    img_filter1 = ImageTk.PhotoImage(img_filter)
    button_filter = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_filter1, text = "Filter", compound= "left", fg = "silver",activeforeground='white',command=lambda:filter_clicked())
    button_filter.place(x="15", y="200")

    #add Text button
    def addtext_clicked():
        global current_img
        if current_img != None:
            print("on progress")
            canvas_add_text = Canvas(canvas1, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0")
            canvas_add_text.place(x="750", y="290", relwidth="0.25", relheight="0.42")
            
            # get text
            get_text_label = Label(canvas_add_text, text = "enter text :", fg="white", bg = "#0d0d0d")
            get_text_label.place(x="20", y="20")
            get_text=Entry(canvas_add_text, bg="#1a1a1a" , bd="0", fg="white")
            get_text.place(x="140", y="15", relwidth=".5", relheight="0.1")
            
            # get font size
            get_font_size_label = Label(canvas_add_text, text = "enter font size :", fg="white", bg = "#0d0d0d")
            get_font_size_label.place(x="20", y="60")
            get_font_size=Entry(canvas_add_text,bg="#1a1a1a" , bd="0", fg="white")
            get_font_size.place(x="140", y="55", relwidth=".5", relheight="0.1")

            # choose font type and style
            get_font_label = Label(canvas_add_text, text = "Select font :", fg="white", bg = "#0d0d0d")
            get_font_label.place(x="20", y="100")
            select_font_option = MyOptionMenu(canvas_add_text, 'Select Font', 'arial','impact','times new roman')
            select_font_option.place(x="140", y="100")
            selected_font_label = Label(canvas_add_text, text = "Select font :", fg="white", bg = "#0d0d0d")
            selected_font_label.place(x="140", y="100")
            select_font_button= tk.Button(canvas_add_text, bg ="gray",text="new", bd =".5",width= "3", height = "1", command =lambda: askcolor())
            select_font_button.place(x="268", y="175")
            
            # get font colour
            get_text_colour = Label(canvas_add_text, text = "Select font colour :", fg="white", bg = "#0d0d0d")
            get_text_colour.place(x="20", y="140")
            
            def choose_colour(colour):
                global text_colour
                text_colour = colour
                #sprint (text_colour)
            
            red_button = tk.Button(canvas_add_text, bg ="red", bd= ".5",width= "3", height = "1", command =lambda: choose_colour("red"))
            red_button.place(x="140", y="145")
            
            blue_button = tk.Button(canvas_add_text, bg ="blue", bd =".5", width= "3", height = "1",command =lambda:  choose_colour("blue"))
            blue_button.place(x="172", y="145")
            
            yellow_button= tk.Button(canvas_add_text, bg ="yellow", bd =".5",width= "3", height = "1",command =lambda:  choose_colour("yellow"))
            yellow_button.place(x="204", y="145")
            
            green_button= tk.Button(canvas_add_text, bg ="green", bd =".5",width= "3", height = "1", command = lambda: choose_colour("green"))
            green_button.place(x="236", y="145")
            
            violet_button= tk.Button(canvas_add_text, bg ="violet", bd =".5" ,width= "3", height = "1",command =lambda:  choose_colour("violet"))
            violet_button.place(x="268", y="145")
            
            orange_button= tk.Button(canvas_add_text, bg ="orange", bd =".5" ,width= "3", height = "1",command =lambda:  choose_colour("orange"))
            orange_button.place(x="140", y="175")
            
            black_button= tk.Button(canvas_add_text, bg ="black", bd =".5", width= "3", height = "1",command =lambda:  choose_colour("black"))
            black_button.place(x="172", y="175")
            
            white_button= tk.Button(canvas_add_text, bg ="white", bd =".5",width= "3", height = "1", command =lambda:  choose_colour("white"))
            white_button.place(x="204", y="175")

            gray_button= tk.Button(canvas_add_text, bg ="gray", bd =".5",width= "3", height = "1", command =lambda:  choose_colour("white"))
            gray_button.place(x="236", y="175")
            
            ## choose colour Manually
            global text_newcl_button
            text_newcl_button= tk.Button(canvas_add_text, bg ="gray",text="new", bd =".5",width= "3", height = "1", command =lambda: askcolor())
            text_newcl_button.place(x="268", y="175")
                
        def apply():
            global current_img
            global text_colour
            # get text
            text = get_text.get()
            print(text)
            # text size
            text_size = int(get_font_size.get())
            print(text_size)
            # font
            cfont=str(select_font_option.var)
            print (cfont)
            # text colour
            f_c =text_colour
            print(f_c)
            # apply font
            draw = ImageDraw.Draw(current_img)
            font = ImageFont.truetype(cfont+'.ttf', size=text_size)
            draw.text((300, 300), text, fill=f_c, font=font)
            
            ## show image
            image = draw
            width, height = image.size
            image_resized = resize_image(width, height,label_width,label_height,image)
            text_added = ImageTk.PhotoImage(image=image_resized)
            labelshow.image= text_added
            labelshow.configure(image= text_added)
            current_img=image
            Undo.append(current_img)
            
            canvas_add_text.after(1000, canvas_add_text.destroy)
            canvastoolbar.destroy
            
        button_apply_font = HoverButton(canvas_add_text,  bg = "#0d0d0d", bd="0", height = "1", width ="15",text = "Apply Font", compound= "left",fg ="gray",command=lambda:apply())
        button_apply_font.place(x="20", y="300")
    
        
    #add text function
    img_addtext = Image.open(r"elements2.0Images1\assets\operationsImages\addtext.png")
    img_addtext = img_addtext.resize((30,32), Image.ANTIALIAS)
    img_addtext1 = ImageTk.PhotoImage(img_addtext)
    button_addtext = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_addtext1, text = "Add Text", compound= "left", fg = "silver",activeforeground='white', command=lambda: addtext_clicked())
    button_addtext.place(x="15", y="250")

    #contrast button function
    def contrast_clicked():
        global current_img
        br=retrieve_input()
        print (br)
        imbr = ImageEnhance.Contrast(current_img)
        image = imbr.enhance(float (br))
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        cntrst_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= cntrst_img
        labelshow.configure(image= cntrst_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #contrast button
    img_contrast = Image.open(r"elements2.0Images1\assets\operationsImages\contrast.png")
    img_contrast = img_contrast.resize((35,35), Image.ANTIALIAS)
    img_contrast1 = ImageTk.PhotoImage(img_contrast)
    button_contrast = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_contrast1, text = "Contrast", compound= "left", fg = "silver",activeforeground='white',command=lambda: contrast_clicked())
    button_contrast.place(x="13", y="300")

    #flip right-lrft funtion
    def flip_right_clicked():
        global current_img
        image = current_img.transpose(method=Image.FLIP_LEFT_RIGHT)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        flip_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= flip_img
        labelshow.configure(image= flip_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #flip top down function
    def flip_top_clicked():
        global current_img
        image = current_img.transpose(method=Image.FLIP_TOP_BOTTOM)
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        flip_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= flip_img
        labelshow.configure(image= flip_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #flip specific buttons / canvas
    def flip_clicked():
        #flip canvas
        canvasflip = Canvas(main_frame, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0" )
        canvasflip.place(x="950", y="380", relwidth="0.123", relheight="0.1")
        canvasflip.after(2000, canvasflip.destroy)
        #flip rigth - left button
        flipright = Image.open(r"elements2.0Images1\assets\operationsImages\flip.png")
        flipright = flipright.resize((40,40), Image.ANTIALIAS)
        flipright1 = ImageTk.PhotoImage(flipright)
        flipright1.image=flipright1
        button_flipright = HoverButton(canvasflip,  bg = "#0d0d0d", bd="0", image=flipright1, text = "Flip Right", compound= "left", fg = "silver",activeforeground='white', command=lambda: flip_right_clicked())
        button_flipright.place(x="30", y="0")

        #flip top- botton
        fliptop = Image.open(r"elements2.0Images1\assets\operationsImages\flip.png")
        fliptop = fliptop.resize((40,40), Image.ANTIALIAS)
        fliptop1 = ImageTk.PhotoImage(fliptop)
        fliptop1.image=fliptop1
        button_fliptop = HoverButton(canvasflip,  bg = "#0d0d0d", bd="0", image=fliptop1, text = "Flip top   ", compound= "left", fg = "silver",activeforeground='white', command=lambda: flip_top_clicked())
        button_fliptop.place(x="30", y="40")

    #flip button
    img_flip = Image.open(r"elements2.0Images1\assets\operationsImages\flip.png")
    img_flip = img_flip.resize((35,35), Image.ANTIALIAS)
    img_flip1 = ImageTk.PhotoImage(img_flip)
    button_flip = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_flip1, text = "Flip", compound= "left", fg = "silver",activeforeground='white',command=lambda: flip_clicked())
    button_flip.place(x="13", y="350")

    #saturation function
    def saturation_clicked():
        global current_img
        br=retrieve_input()
        print (br)
        imbr = ImageEnhance.Color(current_img)
        image = imbr.enhance(int (br))
        width, height = image.size
        image_resized = resize_image(width, height,label_width,label_height,image)
        cntrst_img = ImageTk.PhotoImage(image=image_resized)
        labelshow.image= cntrst_img
        labelshow.configure(image= cntrst_img)
        current_img=image
        Undo.append(current_img)
        #return current_img

    #Saturation button
    img_saturation = Image.open(r"elements2.0Images1\assets\operationsImages\saturation.png")
    img_saturation = img_saturation.resize((37,37), Image.ANTIALIAS)
    img_saturation1 = ImageTk.PhotoImage(img_saturation)
    button_saturation = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_saturation1, text = "Saturation", compound= "left", fg = "silver",activeforeground='white',command=lambda: saturation_clicked() )
    button_saturation.place(x="13", y="400")


    #Undo function
    def undo_clicked():
        if len(Undo) !=0:
            try:
                image= Undo[-2]
                global current_img
                width, height = image.size
                image_resized = resize_image(width, height,label_width,label_height,image)
                undo_img = ImageTk.PhotoImage(image=image_resized)
                labelshow.image=undo_img
                labelshow.configure(image= undo_img)
                current_img=image
                if Undo[-1] not in Redo:
                    Redo.append(Undo[-1])
                else:
                    pass
                Redo.append(Undo[-2])
                Undo.pop()
            except:
                pass
        else:
            pass

    #undo button

    img_undo = Image.open(r"elements2.0Images1\assets\operationsImages\undo.png")
    img_undo = img_undo.resize((40,40), Image.ANTIALIAS)
    img_undo1 = ImageTk.PhotoImage(img_undo)
    button_undo = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_undo1, text = "Undo", compound= "left", fg = "silver",activeforeground='white',command= undo_clicked)
    button_undo.place(x="13", y="510")

    # redo function
    def redo_clicked():
        if len(Redo)!=0:
            try:
                image=Redo[-1]
                global current_img
                width, height = image.size
                image_resized = resize_image(width, height,label_width,label_height,image)
                redo_img = ImageTk.PhotoImage(image=image_resized)
                labelshow.image=redo_img
                labelshow.configure(image=redo_img)
                current_img=image
                Undo.append(Redo[-1])
                Redo.pop()
            except:
                pass
        else:
            pass

    #redo button
    img_redo = Image.open(r"elements2.0Images1\assets\operationsImages\redo.png")
    img_redo = img_redo.resize((40,40), Image.ANTIALIAS)
    img_redo1 = ImageTk.PhotoImage(img_redo)
    button_redo = HoverButton(canvastoolbar,  bg = "#0d0d0d", bd="0", image=img_redo1, text = "Redo", compound= "left", fg = "silver",activeforeground='white', command=redo_clicked)
    button_redo.place(x="13", y="560")

    ##################################################### voice/ mic active/ listen ###########################################################


    ############################################################ Play Button #################################################################
    #play button function
    def playbtn_clicked():
        play_win = Toplevel(root)
        play_win.title("elements_Music")
        play_win.iconbitmap(r"elements2.0Images1\icons\logofull2_1TB_icon.ico")
        play_win.geometry("600x400+400+200")

        play_logo = Image.open(r"elements2.0Images1\Unwanted\logofull2.png")
        play_logo = play_logo.resize((600,400), Image.ANTIALIAS)
        photo_logo = ImageTk.PhotoImage(play_logo)
        l1= Label(play_win, image=photo_logo)
        l1.pack()
        l1.photo=photo_logo

        play_button = Image.open(r"elements2.0Images1\assets\operationsImages\play-button.png")
        play_button = play_button.resize((40,30), Image.ANTIALIAS)
        play_button1 = ImageTk.PhotoImage(play_button)
        button_play_button = HoverButton(play_win,  bd="0", image=play_button1)
        button_play_button.place(x="350", y="50", relwidth=".07", relheight=".074")
        button_play_button.play_button1 = play_button1

        play_back = Image.open(r"elements2.0Images1\assets\operationsImages\backwards.png")
        play_back = play_back.resize((40,30), Image.ANTIALIAS)
        play_back1 = ImageTk.PhotoImage(play_back)
        button_play_back = HoverButton(play_win, bg="white",  bd="0", image=play_back1)
        button_play_back.place(x="300", y="50", relwidth=".07", relheight=".065")
        button_play_back.play_back1 = play_back1

        #add music to collection button
        add_music = Image.open(r"elements2.0Images1\assets\operationsImages\play-button.png")
        add_music = add_music.resize((40,30), Image.ANTIALIAS)
        add_music1 = ImageTk.PhotoImage(add_music)
        button_add_music = HoverButton(play_win,  bd="0", image=add_music1)
        button_add_music.place(x="400", y="50", relwidth=".07", relheight=".074")
        button_add_music.add_music = add_music1

    # play button
    img_play = Image.open(r"elements2.0Images1\assets\operationsImages\play-button.png")
    img_play = img_play.resize((30,30), Image.ANTIALIAS)
    img_play1 = ImageTk.PhotoImage(img_play)
    button_play = HoverButton(main_frame,  bg = "#0d0d0d", bd="0", image=img_play1, activebackground='#0d0d0d', compound= "left", fg = "silver",activeforeground='white',command= playbtn_clicked)
    button_play.place(x="1062", y="700", relwidth=".065", relheight=".05")

    import_label=Label(canvas1,fg="white",bg="black",text=None)
    import_label.place(x="460",y="270")
    ############################################################# Save Portion ##############################################################
    #save using top level for voice on progerss
    def saved():                                                                                           ## image Saved confirmation stay or leave??
        saved_win = Toplevel(root)
        saved_win.title("Image Saved")
        saved_win.iconbitmap(r"elements2.0Images1\icons\logofull2_1TB_icon.ico")
        saved_win.geometry("400x200+400+200")
        saved_win.maxsize(400,200)
        saved_win.config(bg="#1c1c1c")

        #Confirmation Tick                                      ##new tik.png assets included
        label_tik = Label(saved_win, bg="#1c1c1c", bd="0", borderwidth = "0", highlightthickness = "0",image= None)
        label_tik.place(x="65",y="50")

        tic_img=Image.open(r"elements2.0Images1\assets\operationsImages\tick.png")
        image_resized =tic_img.resize((65,65), Image.ANTIALIAS)
        tic_img1=image_resized
        tic_img2 = ImageTk.PhotoImage(image=tic_img1)
        label_tik.image= tic_img2
        label_tik.config(image= tic_img2)
        label_tik.config(width="65",height="65")

        # confirmation label
        confirm_label=Label(saved_win,fg="white",bg="#1c1c1c",text="Image Saved!", font=("", 12))
        confirm_label.place(x="190",y="60")
        confirm_label=Label(saved_win,fg="white",bg="#1c1c1c",text="Do you want to Continue Editing?", font=("", 10))
        confirm_label.place(x="150",y="90")

        # Continue button
        Cont_button = HoverButton(saved_win,  bg = "#0d0d0d", bd="0", text = "Continue", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command=lambda: saved_win.destroy())
        Cont_button.place(x="80",y="140")

        #quit button
        Quit_button = HoverButton(saved_win,  bg = "#0d0d0d", bd="0", text="Quit", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command=  root.destroy())
        Quit_button.place(x="220",y="140")

    # Save function, Calls Save window
    def save():
        global current_img
        if current_img == None :                  ## if tried to save without importing image
            #print("check") #debug
            import_label.config(text="Import Image First")

        else:                                 ## Else if image imported and editted open save window
            save_win = Toplevel(root)
            save_win.title("Save image")
            save_win.iconbitmap(r"elements2.0Images1\icons\logofull2_1TB_icon.ico")
            save_win.geometry("800x400+400+200")
            save_win.maxsize(800,400)
            save_win.config(bg="#1c1c1c")

            ##preview_text
            prv_label=Label(save_win,fg="white",bg="#1c1c1c",text="PREVIEW",font=("Courier", 35))
            prv_label.place(x="30",y="30")
            #prv_label.config(font=("Courier", 44))

            # Setting preview Image
            # setting image in label for Preview 
            label_preview = Label(save_win, bg="black", bd="0", borderwidth = "0", highlightthickness = "0",image= None)
            label_preview.place(x="380",y="30")

            image=current_img
            width, height = image.size
            image_resized = resize_image(width, height,label_width,label_height,image)
            current_img=image
            preview_img = ImageTk.PhotoImage(image=image_resized)
            label_preview.image= preview_img
            label_preview.config(image= preview_img)
            label_preview.config(width="400",height="300")

            #get file name
            #filename label
            Filename_label=Label(save_win,bg="#1c1c1c",fg="white",text="Enter File Name")
            Filename_label.place(x="30", y="120")
            #retrive file name
            FileName=Text(save_win,height=2, width=25, bg="#3a3a3a" , bd="0", fg="white")
            FileName.place(x="150",y="115")

            #get extention
            #ext label
            ext_label=Label(save_win,fg="white",bg="#1c1c1c",text="Select extention ")
            ext_label.place(x="30",y="180")
            #retrive extention 
            extention=Text(save_win,height=2, width=25, bg="#3a3a3a" , bd="0", fg="white")
            extention.place(x="150",y="175")

            
            #Change save Quality
            def quality():
                global qualityenter
                Change_quality.destroy()
                #quality label
                ext_label=Label(save_win,fg="white",bg="#1c1c1c",text="Quality in % ")
                ext_label.place(x="30",y="240")
                #retrive extention 
                qualityenter=Text(save_win,height=2, width=25, bg="#3a3a3a" , bd="0", fg="white")
                qualityenter.place(x="150",y="235")

            #change quality button
            Change_quality = HoverButton(save_win,  bg = "#0d0d0d", bd="0", text = "Change Quality", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command=lambda: quality())
            Change_quality.place(x="30", y="230")

            # estimated file size
            etfs_label=Label(save_win,fg="white",bg="#1c1c1c",text="Refresh to get filesize")                  ##Refresh to get file size
            etfs_label.place(x="150",y="298")                                                                  ##place

            # getsize Function                                                                                 ##debug !!!     ## err
            def getsize():               
                etfs_label.destroy()
                etfs_label_2=Label(save_win,fg="white",bg="#1c1c1c",text="Estimated File size is :")           ##File size description
                etfs_label_2.place(x="150",y="298")  
                ###size=os.stat(current_img).st_size                                                           ##getting file size   ##debug    ##error
                size=os.path.getsize(current_img)                                                              ##getting file size   ##debug    ##error
                etfs_label_1=Label(save_win,fg="white",bg="#1c1c1c",text=size)                                 ##Refreshed filesize
                etfs_label_1.place(x="260",y="298")  

            etfs_button = HoverButton(save_win,  bg = "#0d0d0d", bd="0", text = "Refresh File Size", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command=lambda: getsize())
            etfs_button.place(x="30", y="290")

            # Show location && Location button                                                                  
            def getlocation():
                global file_path_string                  
                file_path_string = fd.askdirectory()
                save_win.attributes('-topmost', 'true')                                                         ## bring savve window top and visible
                path_label=Label(save_win,fg="white",bg="#1c1c1c",text=file_path_string)
                path_label.place(x="150",y="353")
                print(file_path_string)

            get_loc_button = HoverButton(save_win,  bg = "#0d0d0d", bd="0", text = "Get File Location", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command=lambda: getlocation())
            get_loc_button.place(x="30", y="345")

            # show Height x Width
            h,w=current_img.size
            hxw_label_1=Label(save_win,fg="white",bg="#1c1c1c",text=h)                                          ## Display Height
            hxw_label_1.place(x="380",y="330") 
            hxw_label_2=Label(save_win,fg="white",bg="#1c1c1c",text="x")                                        ## Display x
            hxw_label_2.place(x="407",y="330") 
            hxw_label_2=Label(save_win,fg="white",bg="#1c1c1c",text=w)                                          ## Display width
            hxw_label_2.place(x="420",y="330") 

            
            ## Save Now Function
            def save_now():
                global qualityenter
                global filenameget
                global extentionget
                global qualityget

                filenameget = FileName.get("1.0","end-1c")                                                      ## retrive filename
                #print(filenameget)
                extentionget = extention.get("1.0","end-1c")                                                    ## retrive extention
                #print(extentionget)
                try:
                    qualityget =int(qualityenter.get("1.0","end-1c"))                                           ## retrive quality
                #print(qualityget)
                except:
                    qualityget=100
                ##finally save
                finalfilename = file_path_string + "/" + filenameget + "." + extentionget                       ## Final filename
                print (finalfilename)

                current_img.save( finalfilename, optimize = True, quality = qualityget)                         ## finally save file
                save_win.destroy()                                                                              ## destroy save Window After saving
                saved()                                                                                         ## show image saved

            # Save Mic button
            activate_voice_label=Label(save_win,fg="white",bg="#1c1c1c",text="Activate Voice")                  ## label  activate voice
            activate_voice_label.place(x="380",y="348") 
            img_mic2 = Image.open(r"elements2.0Images1\assets\operationsImages\mic2.png")
            img_mic2 = img_mic2.resize((33,36), Image.ANTIALIAS)
            img_mic12 = ImageTk.PhotoImage(img_mic2)
            button_mic2 = tk.Button(save_win,  bg = "#1c1c1c", bd="0", image=img_mic12 ,activebackground='#1c1c1c' ,command =  lambda: save_voice())
            button_mic2.place(x="473", y="344", relwidth=".075", relheight=".091")

            #save button
            Save_button = HoverButton(save_win,  bg = "#0d0d0d", bd="0", text = "Save", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command=lambda: save_now())
            Save_button.place(x="578", y="340")

            #Quit Button
            Quit_button = HoverButton(save_win,  bg = "#0d0d0d", bd="0", text="Continue Editing", compound= "left", fg = "silver",activeforeground='white',width ="13", height ="2",command= lambda : save_win.destroy())
            Quit_button.place(x="683", y="340")

            ##### Save window Keywords ##### 
            """ this keywords belongs to save window only"""
            ################################
            ##save_kewords_list =["save","continue","filename","extention","quality"]

            #save over voice
            #Save over voice function
            def save_voice():                                                                                   ## activates when mic button clicked in save window
                save_voice_activate = True
                while save_voice_activate==True :
                    activate_voice_label.destroy()
                    button_mic2.destroy()
                    save_completed = False
                    while save_completed == False :
                        ############# Filename
                        filenameget = None                                                                      ## get filename over voice
                        while filenameget == None:
                            try:
                                print("filename?")
                                filenameget= listenit()
                                print(filenameget)
                            except sr.UnknownValueError :
                                print ("try again")
                                FileName.insert(tk.INSERT,"try again")                                     ## show fileName text try again
                            FileName.insert(tk.INSERT,filenameget)                                         ## show fileName in svae window

                        ############# Extention 
                        extentionget =None                                                                      ## get extention over voice
                        while extentionget == None:
                            try:
                                print("extention?")
                                value = listenit()
                                if value == "JPG": 
                                    extentionget = "jpg"
                                elif value == "JPEG":
                                    extentionget = "jpeg"
                                elif value == "PNG":
                                    extentionget = "png"
                                elif value == "tiff" or value == "TIFF":
                                    extentionget = "tiff"
                            except ValueError :
                                print ("try again")
                            print(extentionget)
                            extention.insert(tk.INSERT,extentionget)                                       ## show extention in save window

                        ###### If want to change Quality and reduce size #####
                        qualityget = None
                        while qualityget == None:
                            # quality_identifiers =["half","full","quarter"]
                            print("quality?")
                            try:
                                value = listenit()
                                if value.isdigit == True: 
                                    qualityget = value
                                elif value == "half":
                                    qualityget = 50
                                elif value == "full":
                                    qualityget = 100
                                elif value == "quarter":
                                    qualityget = 25
                            except ValueError :
                                    qualityget = 100
                            print (value)
                            print (qualityget)
                        ## get file path automatic manual
                        print("location?")
                        getlocation()                                                                           ## get location
                        print(file_path_string)
                        save_completed ="yes"
                    save_now()
            save_win.mainloop()
        
    #Save Image function___________ Invalid function not used
    def save_clicked():
        global current_img
        try:
            files=[("JPEG", "*.jpeg"),("PNG", "*.png"),("JPG","*.jpg")]
            saveimg= fd.asksaveasfilename(filetypes= files, defaultextension = files)
            if saveimg:
                current_img.save(saveimg)
            

        except BaseException as e:
            print(e)

    #save button
    img_save = Image.open(r"elements2.0Images1\assets\operationsImages\save.png")
    img_save = img_save.resize((30,30), Image.ANTIALIAS)
    img_save1 = ImageTk.PhotoImage(img_save)
    button_save = HoverButton(main_frame,  bg = "#0d0d0d", bd="0", image=img_save1, command = save())
    button_save.place(x="10", y="740", relwidth=".05", relheight=".05")



    # closing Confirmation
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to Stop Editing?"):
            root.destroy()

    #clossing protocol
        root.protocol("WM_DELETE_WINDOW", on_closing)

    #### Do all gui elements codes here. Editing Functions are seperately coded outside of this function like other functions 
    ##################################################################################################################################
    
    
    time.sleep(5)##when time.sleep called the main thread executing till the sleep function stops for 3 secs and listen thread is called
    # chat_value="Welcome to elements...."  ###this say welcome by calling the chat() function below
    #                                     ###global chat_value is passed as parameter
    
    # chat(chat_value)
    listen_thread=threading.Thread(target=listenit)##listenit thread is started.
    listen_thread.start()
    
    root.mainloop() ###mainloop is executing infinitely



def chat(chat_value):   
    engine.say(chat_value)
    engine.runAndWait()
    engine.stop()

def listenit(): ##This function is called in the thread.
    global chat_value
    global hello_label
    global listening
    listening=1   
    while listening:  ##this means when there is a value in the listening variable      
        time.sleep(2)
        try:
            
            chat_value="recognizer is active......I am Listening...."
            chat(chat_value)
            r=sr.Recognizer()
            print("recognizer is active...Listening")            
            hello_label.config(text="Recognizer is active..I am Listening...")
            
            
            with sr.Microphone() as source: ## we can tune the microphone input by setting sample rate and chunk size
                print("Micophone is active")
                
                r.adjust_for_ambient_noise(source) ##adjust for ambient noise with default duration=1,atleast 0.5
                #r.energy_threshold=1000
                #r.dynamic_energy_ratio=1.5
                #r.dynamic_energy_threshold=True
                audio= r.listen(source)
                print("audio received input")
                hello_label.config(text="audio received input ")
                # chat_value="audio received input...."
                # chat(chat_value)
            value = r.recognize_google(audio)
            print(f"value received input is {value}")
            hello_label.config(text=f"You said {value}")
            chat_value=(f"You said {value}")
            chat(chat_value)
            q.put(value)   ##here we put the listened value to the queue
            print("input to queue")
            hello_label.config(text="input to queue")
            # chat_value="input to queue"
            # chat(chat_value)
            time.sleep(2) ##here listening is stopped for 2 seconds and so execution switch back to main thread, then 2 sec is over returns
                            ##to print("Slept for 2 secs")
            print("slept for 2 sec....")
            do_func_thread=threading.Thread(target=do_func(),args=(q,))
            do_func_thread.start()
            
            time.sleep(1)
            
        except sr.UnknownValueError:
            print("Not audible")
            hello_label.config(text="Not audible")
            time.sleep(1)
            chat_value="Not audible....I didn't understand..."
            chat(chat_value)
            listening=1
            
        except sr.RequestError:
            print("No connection!!!")
            hello_label.config(text="No connection!!!")
            chat_value="You are not connected to the internet..."
            chat(chat_value)
def do_func():
    global listening
    global chat_value
    global root
    global operation_label

    
    keywords=["hi","hai","hello","close","exit","rotate","import","open","intensity","brightness", "crop", "smooth", "smooth more","effect","effects","rotate","backward","embross", "undo","redo","back","next","forward","filter", "contour", "save", "quit","exit", "add text", "contrast","flip", "details", "saturation", "undo", "redo", "warmth"] 
                
    if q.qsize():            
        tokens=word_tokenize(q.get())   ###q.get() is used to pop out what is in queue          
        for i in tokens:
            if i in keywords:
                if i=="hi" or i=="hello" or "hai":
                    print("Speech Recognizer is Listening......")
                    operation_label.config(text=f"Hi I am root.......Welcome to Elements ....")
                    chat_value=f"Hi I am root.....Welcome to Elements........."
                    chat(chat_value)
                elif i=="close" or i=="exit": ###Take good care about the time.sleep since we should ajdust them to properly execute code properly
                    #############Here exiting is not working. May be because of threads are not dead or may be listening is not set to listening =0
                    ####plz try to solve
                    print("Exiting...")
                    operation_label.config(text=f"You said {i}...so exiting...")
                    chat_value=f"You said {i}........I am closing and won't do anymore listening............................."
                    chat(chat_value)
                    listening=0
                    # endApp()
                    exit_func()
                    
                elif i=="rotate":
                    print("Rotated")
                    operation_label.config(text=f"You said {i}...so rotated...")
                    chat_value=f"You said {i}...I am listening for next task........................."
                    chat(chat_value)

                
                # elif i=="brightness" or i=="intensity":

                #     #brightness_clicked()
                #     print(i)
                #     #break
                # elif i=="crop":
                #     crop_clicked()
                #     print(i)
                #     #break
                # elif i=="smoooth more":
                #     smooth_more_clicked()
                #     print(i)
                #     #break
                # elif i=="smooth":
                #     smooth_clicked()
                #     print(i)
                #     #break
                # elif i=="details":
                #     detail_clicked()
                #     print(i)
                #     #break
                # elif i=="sharpness":
                #     sharpness_clicked()
                #     print(i)
                #     #break
                # elif i=="contrast":
                #     contrast_clicked()
                #     print(i)
                #     #break
                # elif i=="flip":
                #     flip_clicked()
                #     print(i)
                #     #break
                # elif i=="filter" or i== "effects" or i=="effect":
                #     filter_clicked()
                #     print(i)
                #     #break
                # elif i=="blur":
                #     blur_clicked()
                #     print(i)
                # elif i=="save" or i== "export":
                #     save()
                #     Save = i
                #     print(i)
                #     #break
                # elif i=="open" or i== "import":
                #     import_clicked()
                #     #Save = i
                #     print(i)
                #     #break
                # elif i=="undo" or i=="back"or i=="backward":
                #     undo_clicked()
                #     #Save = i
                #     print(i)
                #     #break  
                # elif i=="redo" or i=="next" or i=="forward":
                #     redo_clicked()
                #     #Save = i
                #     print(i)
                #     #break   
                
                else:
                    print("Try Again...")
                    operation_label.config(text=f"You said something...I didn't understand...")
                    chat_value=f"You said something that I didn't understand...Try again.............................."
                    chat(chat_value)
    


def endApp():
    print("listening is set to 0")
    global listening
    listening=0

    

if __name__=="__main__":
    import random
    root2=tk.Tk()
    root2.geometry("800x500+350+160")
    root2.wm_attributes("-topmost",1)
    root2.overrideredirect(1)
    # splash_screen = Toplevel(root)
    # splash_screen.wm_attributes("-fullscreen",True)
    # splash_screen.wm_overrideredirect(1)


    
    def connection():

        canvasstatus = Canvas(root2, bg ="#0d0d0d", bd="0", borderwidth = "0", highlightthickness = "0" )
        canvasstatus.pack(side=BOTTOM, fill=X)
        #check status
        host='http://google.com'
        try:
            urllib.request.urlopen(host)
            print("connected")
            connectionLabel=Label(canvasstatus,bg="#0d0d0d",fg="black",text="Connection Established")
            connectionLabel.pack()
            closingLabel=Label(canvasstatus,bg="#0d0d0d",fg="black",text="voice enabled")
            closingLabel.pack()
            canvasstatus.after(10000, canvasstatus.destroy)
        except:
            print("not_connected")
            connectionLabel=Label(canvasstatus,bg="#0d0d0d",fg="black",text="NoConnection Err: 404")
            connectionLabel.pack()
            closingLabel=Label(canvasstatus,bg="#0d0d0d",fg="black",text="quit to close/ continue without voice")
            closingLabel.pack()
            quitButton=Button(canvasstatus,bg="#0d0d0d",fg="black",text="Quit",command=lambda:root2.destroy())
            quitButton.pack()
            canvasstatus.after(10000, canvasstatus.destroy)
    
    random_number = str(random.randint(0, 22))
    splash_logo = Image.open(r"elements2.0Images1\splashscreen/"+ random_number + ".png")
    splash_logo = splash_logo.resize((800,500), Image.ANTIALIAS)
    splash_logo1 = ImageTk.PhotoImage(splash_logo)
    l1= Label(root2, bg="silver", image=splash_logo1)
    l1.pack(fill=BOTH,expand=1)
    l1.photo=splash_logo1
    
    root2.after(10000,root2.destroy)
    connection()
    time.sleep(.5)
    gui_thread= threading.Thread(target=Gui(),daemon=True)
    gui_thread.start()
    root2.mainloop()
    #time.sleep(1)
    
    
    

        