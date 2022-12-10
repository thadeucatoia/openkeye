from tkinter import Frame, Grid, Label, Button, Canvas, Grid, Toplevel
from tkinter import ttk 
import tkinter as Tk
from PIL import Image, ImageTk
import PIL.Image
import PIL
import cv2 as cv
import time
import numpy as np
import os
from use_json import *



#inicio de constantes no programa


font = "Arial"
cap = cv.VideoCapture(0)
counter_tool_fix = 0
path_img_reference = os.path.join(os.path.dirname(__file__), 'refs', 'reference.jpg')
path_img_reference_filter = os.path.join(os.path.dirname(__file__), 'refs', 'filter_rgb.jpg')

#inicio classes
class draw_rec(Frame):
    def __init__(self,master):
        Frame.__init__(self,master=None)

        self.frame_init = cv.imread(path_img_reference)
        height, width, no_channels = self.frame_init.shape
        self.x = self.y = 0
        self.canvas = Canvas(master,  cursor="cross", width=width, height=height, bg='Orange')
        self.canvas.grid(row=1,column=0,sticky=Tk.N+Tk.S+Tk.E+Tk.W)
       
        #binds mouse
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        #variables
        self.rect = None
        self.rect_init = None
        self.rect_end = None
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        #load image
        self.im = PIL.Image.open(path_img_reference)
        self.wazil,self.lard=self.im.size
        self.canvas.config(scrollregion=(-2,-2,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        if not self.rect:
          self.rect = self.canvas.create_rectangle(self.x, self.y, 3, 3, fill="", outline="Blue")
        
        if self.rect_init == None:
            pass
        else:
            self.canvas.delete(self.rect_end)
            self.canvas.delete(self.rect_init)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.curX = curX
        self.curY = curY
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
      self.rect_init = self.canvas.create_rectangle(self.start_x+2, self.start_y+2, self.start_x-2, self.start_y-2, fill="Red", outline="red")
      if self.curX>0 or self.curY>0:
        self.rect_end = self.canvas.create_rectangle(self.curX+2,self.curY+2,self.curX-2,self.curY-2, fill="Red", outline="red")     
      pass

class get_color_canvas(Frame, ):
    def __init__(self,master,numer_tool):

        self.number_tool = numer_tool
        self.top_corner = read_json(self.number_tool,"top_corner")
        self.botton_corner = read_json(self.number_tool,"botton_corner")

        Frame.__init__(self,master=None)
        self.frame_rgb = cv.imread(path_img_reference)
        height, width, no_channels = self.frame_rgb.shape
        self.frame_hsv = cv.cvtColor(self.frame_rgb, cv.COLOR_BGR2HSV)


        self.x = self.y = 0
        self.canvas = Canvas(master,  cursor="crosshair", height=height, width=width, bg='Orange')
        self.canvas_black = Canvas(master,  cursor="X_cursor", height=height, width=width, bg='black')
        self.retangle_ref = self.canvas_black.create_rectangle(self.top_corner[0],  self.top_corner[1], self.botton_corner[0], self.botton_corner[1], fill="", outline="Blue")

        self.canvas.grid(row=0,column=0)
        self.canvas_black.grid(row=0,column=3)
        #,sticky=N+S+E+W

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.coord_colors=[]
        self.value_colors=[]

        self.low_rgb = []
        self.high_rgb = []

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.curX = None
        self.curY = None


        self.im = PIL.Image.open(path_img_reference)
        self.wazil,self.lard=self.im.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

    def on_button_press(self, event):
            # save mouse drag start position
        self.start_x = event.y
        self.start_y = event.x
        #invertido de propósito =|

        #invertido pra frame_rgb para frame_hsv
        self.value_colors.append(self.frame_hsv[self.start_x,self.start_y].tolist())
        self.dimension = self.frame_hsv.shape


    def on_move_press(self, event):
      pass


    def on_button_release(self, event):

      #print(self.value_colors)

      if self.value_colors:
  
        self.minb = min(c[0] for c in self.value_colors)
        self.ming = min(c[1] for c in self.value_colors)
        self.minr = min(c[2] for c in self.value_colors)
        self.maxb = max(c[0] for c in self.value_colors)
        self.maxg = max(c[1] for c in self.value_colors)
        self.maxr = max(c[2] for c in self.value_colors)
        self.lb = [self.minb,self.ming,self.minr]
        self.ub = [self.maxb,self.maxg,self.maxr]
        self.low_rgb = np.array(self.lb)
        self.high_rgb = np.array(self.ub)
        self.rgb_mask = cv.inRange(self.frame_hsv, self.low_rgb, self.high_rgb)

      cv.imwrite(path_img_reference_filter, self.rgb_mask)
      self.img_black = PIL.Image.open(path_img_reference_filter)
      self.tk_img_black = ImageTk.PhotoImage(self.img_black)
      self.canvas_black.create_image(0, 0,anchor="nw", image=self.tk_img_black)
      self.retangle_ref = self.canvas_black.create_rectangle(self.top_corner[0],  self.top_corner[1], self.botton_corner[0], self.botton_corner[1], fill="", outline="Blue")
      
      #calculo white pixels
      cropped_image = self.rgb_mask[self.top_corner[1]:self.botton_corner[1],self.top_corner[0]:self.botton_corner[0]]
      self.n_white_pix = np.sum(cropped_image == 255)

class video_canvas(Frame):
    def __init__(self,master,numer_tool):
        Frame.__init__(self,master=None)

        self.number_tool = numer_tool
        self.top_corner = read_json(self.number_tool,"top_corner")
        self.botton_corner = read_json(self.number_tool,"botton_corner")


        self.canvas = Canvas(master,  cursor="crosshair", height=480, width=640, bg='Black')
        self.canvas.grid(row=0,column=0)


def take_shot():
    
    global frame
    _, frame = cap.read()
    blue,green,red = cv.split(frame)
    frame_ = cv.merge((red,green,blue))
    img = ImageTk.PhotoImage(image=Image.fromarray(frame_))
    img_label = Label(image=img, bg="white")
    img_label.image = img
    img_label.grid(row=1, column=0, rowspan=3, columnspan=2)
    save_ref_btn.lift()
      
def creat_texts_const():
    #title
    title_openkeye = Label(root, text="OpenKeye V1.0", font=(font, 30))
    title_openkeye.grid(row=0, columnspan=3, sticky=Tk.NS, padx=5, pady=5)
    #tool 1 label
    tool1_label = Label(root, text="TOOL 1", font=(font, 12))
    tool1_label.grid(row=1, column=2, sticky=Tk.N, padx=5, pady=5)
    #tool 2 label
    tool2_label = Label(root, text="TOOL 2", font=(font, 12))
    tool2_label.grid(row=1, column=3, sticky=Tk.N, padx=5, pady=5)

def creat_frame_const():

    #white space for the photo
    photo_grid = Frame(root, width=645, height=485, bg="white")
    photo_grid.grid(columnspan=2, rowspan=3, row=1, column=0)

def init_img_ref():

    try:
        ref_img = cv.imread(path_img_reference)
        blue,green,red = cv.split(ref_img)
        ref_img_ = cv.merge((red,green,blue))
        img = ImageTk.PhotoImage(image=Image.fromarray(ref_img_))
        img_label = Label(image=img, bg="white")
        img_label.image = img
        img_label.grid(row=1, column=0, rowspan=3, columnspan=2)
    except:
        pass

def save_img():
    
    try:
        cv.imwrite(path_img_reference, frame)
    except:
        popupmsg('Image not found!')

def popupmsg(msg):
    popup = Toplevel()
    popup.wm_title("Error")
    label = ttk.Label(popup, text=msg, font=font)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Ok", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def get_color_tool(tool_number):

  lvl_up_trig = Tk.StringVar()
  lvl_dw_trig = Tk.StringVar()
  
  def update_value_tags(event):
    if any(get_colors.low_rgb):

        values_rgb.config(text=f'RGB_L = {get_colors.low_rgb} || RGB_H = {get_colors.high_rgb}') 
        values_white_pixel.config(text=f'White Pixels: {get_colors.n_white_pix}')



    #retangle_ref = get_colors.canvas_black.create_rectangle(top_corner[0],  top_corner[1], botton_corner[0], botton_corner[1], fill="", outline="Blue")

  def clear_values():

    get_colors.value_colors *= 0
    get_colors.n_white_pix = ''
    get_colors.low_rgb = '[- - -]'
    get_colors.high_rgb = '[- - -]'
    get_colors.canvas_black.delete('all')
   
  def save_colors(tool_number):

    try:
        write_json(tool_number,"lvl_dw_trig",int(lvl_dw_trig.get()))
        write_json(tool_number,"lvl_up_trig",int(lvl_up_trig.get()))
    except:
        popupmsg('Please enter a number,\nDumbass...')

    if get_colors.value_colors:            
        write_json(tool_number,"low_rgb",get_colors.lb)
        write_json(tool_number,"high_rgb",get_colors.ub)
        colors.destroy()
    else:
        popupmsg('Please Draw a Square\nBefore you save,\nDumbass...')



    #retangle_ref = get_colors.canvas_black.create_rectangle(top_corner[0],  top_corner[1], botton_corner[0], botton_corner[1], fill="Blue", outline="Blue")
    #retangle_comp = get_colors.canvas_black.create_rectangle(0, 0, 100, 100, fill="Blue", outline="Blue")

  colors=Toplevel()
  #colors.geometry('1450x700') #size gui
  colors.geometry('+%d+%d'%(200, 200)) #place gui
  get_colors = get_color_canvas(colors, tool_number)



  values_rgb = Label(colors, text='RGB_L = [- - -] || RGB_H = [- - -]', font=('Arial', 20), background='white')
  values_rgb.grid(row=4, column=0, sticky=Tk.W, padx=5, pady=5)

  bSaveColors = Button(colors, text="Save All", command=lambda: save_colors(tool_number), font=('Arial',12), height=1, width=15)
  bSaveColors.grid(row=0, column=1, padx=5, pady=5)

  bClearColor = Button(colors, text="Clear All", command=clear_values, font=('Arial',12), height=1, width=15)
  bClearColor.grid(row=0, column=2, padx=5, pady=5)

  #Entry's
  #entry upper
  label_entry_upper = Label(colors, text='Upper window', font=('Arial', 20), background='white').grid(row=5, column=0, sticky=Tk.NS, padx=5, pady=5)
  upper_num_entry = Tk.Entry(colors, textvariable=lvl_up_trig,font=('Arial', 20), highlightbackground='Orange').grid(row=5, column=1) 
  #entry lower
  label_entry_lower = Label(colors, text='Lower window', font=('Arial', 20), background='white').grid(row=6, column=0, sticky=Tk.NS, padx=5, pady=5)
  lower_num_entry = Tk.Entry(colors, textvariable=lvl_dw_trig, font=('Arial', 20), highlightbackground='Orange').grid(row=6, column=1)
  #pixel reference
  values_white_pixel = Label(colors, text='White Pixels: ', font=('Arial', 20), background='white')
  values_white_pixel.grid(row=7, column=0, sticky=Tk.NS, padx=5, pady=5)

  colors.bind("<ButtonRelease-1>", update_value_tags)

  colors.mainloop()

def build_square(tool_number):
    retangle=Toplevel()
    retangle.resizable(width=False, height=False)
    #retangle.geometry('1000x700') #size gui
    retangle.geometry('+%d+%d'%(350, 10)) #place gui
    ret_value = draw_rec(retangle)

    TitleWindow = Label(retangle, text='Draw Tool Window', font=('Arial', 30))
    TitleWindow.grid(row=0, column=0, columnspan=2, sticky=Tk.EW, padx=5, pady=5)
    values_upper = Label(retangle, text='X0 = - - - || Y0 = - - -', font=('Arial', 20), background='white')
    values_upper.grid(row=4, column=0, sticky=Tk.W, padx=5, pady=5)
    values_downer = Label(retangle, text='X1 = - - - || Y1 = - - -', font=('Arial', 20), background='white')
    values_downer.grid(row=5, column=0, sticky=Tk.W, padx=5, pady=5)

    def update_value_label(event):

        values_upper.config(text=f'X0 = {ret_value.start_x} || Y0 = {ret_value.start_y}')
        values_downer.config(text=f'X1 = {ret_value.curX} || Y1 = {ret_value.curY}')

    def save_coord(tool_number):
        if ret_value.start_x:            
            write_json(tool_number,"top_corner",(ret_value.start_x,ret_value.start_y))
            write_json(tool_number,"botton_corner",(ret_value.curX,ret_value.curY))
            retangle.destroy()
        else:
            popupmsg('Please Draw a Square\nBefore you save,\nDumbass...')

    retangle.bind("<ButtonRelease-1>", update_value_label)

    bSaveCoord = Button(retangle, text="Save Coord", command=lambda: save_coord(tool_number), font=(font,12), height=1, width=15)
    bSaveCoord.grid(row=1, column=1, padx=5, pady=5)


    retangle.mainloop()

def exit_cmd():
    cap.release()
    root.destroy()


def now_im_gonna_fucking_judge(tool_number):

    def video_run():
  

        while True:

            _, now_frame = cap.read()

            back_ground = cv.cvtColor(now_frame, cv.COLOR_BGR2RGB)
            hsv_frame = cv.cvtColor(now_frame, cv.COLOR_BGR2HSV)
            video_to_show_background = ImageTk.PhotoImage(image = Image.fromarray(back_ground))
            canvas_video.canvas.create_image(0, 0,anchor="nw", image=video_to_show_background)

            rgb_mask = cv.inRange(hsv_frame, low_rgb_np, high_rgb_np)
            cropped_image = rgb_mask[top_corner[1]:botton_corner[1],top_corner[0]:botton_corner[0]]
            n_white_pix = np.sum(cropped_image == 255)   
            label_white_pixel.config(text=n_white_pix)      
            
            if down_tr < n_white_pix < upper_tr:
                retangle_ref = canvas_video.canvas.create_rectangle(top_corner[0], top_corner[1], botton_corner[0], botton_corner[1], fill="", outline="Green", width=3)
                lbl_ok_ng = canvas_video.canvas.create_text(botton_corner[0]+10, botton_corner[1]+10, text="OK", fill="Green", font=('ARIAL', 20))
            else:
                retangle_ref = canvas_video.canvas.create_rectangle(top_corner[0], top_corner[1], botton_corner[0], botton_corner[1], fill="", outline="Red", width=3)
                lbl_ok_ng = canvas_video.canvas.create_text(botton_corner[0]+10, botton_corner[1]+10, text="NG", fill="Red", font=('ARIAL', 20))
            
            #canvas_video.canvas.delete('all')
            judge.update()

    def exit():
        judge.destroy()

    #carrega tools crop
    top_corner = read_json("tool_1","top_corner")
    botton_corner = read_json("tool_1","botton_corner")

    #carrega tools rgb
    low_rgb = read_json("tool_1","low_rgb")
    high_rgb = read_json("tool_1","high_rgb")

    upper_tr = read_json("tool_1","lvl_up_trig")
    down_tr = read_json("tool_1","lvl_dw_trig")

    print(upper_tr,down_tr)

    low_rgb_np = np.array(low_rgb)
    high_rgb_np = np.array(high_rgb)


    judge = Toplevel()

   
    judge.geometry('+%d+%d'%(200, 200)) #place gui

    canvas_video = video_canvas(judge, tool_number)

    bStart = Button(judge, text="Start...!", command=video_run, font=(font,12), height=1, width=15)
    bStart.grid(row=0, column=2, padx=5, pady=5)

    label_white_pixel = Label(judge, text='---', font=('Arial', 20), background='white')
    label_white_pixel.grid(row=1, column=2)

    #bExit = Button(judge, text="Exit...", command=exit, font=(font,12), height=1, width=15)
    #bExit.grid(row=2, column=2, padx=5, pady=5)

    judge.mainloop()



root = Tk.Tk()
root.resizable(width=False, height=False)
root.geometry('+%d+%d'%(350, 10)) #place GUI at x=350, y=10



creat_texts_const()
creat_frame_const()
try:
    ref_img = cv.imread(path_img_reference)
    blue,green,red = cv.split(ref_img)
    ref_img_ = cv.merge((red,green,blue))
    img = ImageTk.PhotoImage(image=Image.fromarray(ref_img_))
    img_label = Label(image=img, bg="Cyan")
    img_label.image = img
    img_label.grid(row=1, column=0, rowspan=3, columnspan=2)
except:
    pass



#button draw for tool 1
bDraw_tool_1 = Button(root, text="Draw Tool 1", command=lambda: build_square("tool_1"), font=(font,12), height=1, width=15)
bDraw_tool_1.grid(row=1, column=2, padx=5, pady=5)
#button get color tool 1
get_color1_btn = Button(root, text="Get Color Tool 1", command=lambda: get_color_tool("tool_1"), font=(font,12), height=1, width=15)
get_color1_btn.grid(row=1, column=2, padx=5, pady=5, sticky=Tk.S)

#button draw for tool 2
bDraw_tool_2 = Button(root, text="Draw Tool 2", command=lambda: build_square("tool_2"), font=(font,12), height=1, width=15)
bDraw_tool_2.grid(row=1, column=3, padx=5, pady=5)

#Button to take a shot...
shot_btn = Button(root, text="Take a Shot!", command=take_shot, font=(font,12), height=1, width=15)
shot_btn.grid(column=2, row=4, pady=5, padx=5, stick=Tk.NW)

#Button to safe ref
save_ref_btn = Button(root, text="Save REF.", command=save_img, font=(font,12), height=1, width=15)
save_ref_btn.grid(column=1, row=3, pady=5, padx=5, sticky=Tk.SE)

#button exit
exit_button = Button(root, text="Exit", command=exit_cmd, font=(font,12), height=1, width=15)
exit_button.grid(column=3, row=4, pady=5, padx=5)


#button draw for tool 2
bJudge = Button(root, text="** JUDGE **", command=lambda: now_im_gonna_fucking_judge('tool_1'), font=(font,12), height=1, width=15)
bJudge.grid(row=3, column=3, padx=5, pady=5)


root.mainloop()