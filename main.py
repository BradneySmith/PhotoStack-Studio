import os
from pathlib import Path
from PIL import ImageTk, Image
import tkinter as tk


root = tk.Tk() # root window (Tk) must be created
root.withdraw() # remove from screen, working with Toplevel instead
root = tk.Toplevel() # can check resizing events with Toplevel but not Tk 
root.geometry("1280x720")
root.title('PhotoStack Studio')
root.iconbitmap('settings/favicon.ico')
root.minsize(1280, 720)
bg_colour = '#989898'
root.configure(bg=bg_colour)

main_directory = os.getcwd() # directory of main.py
photo_directory = main_directory+'/unstacked_photos' # default directory for unedited photos
home = str(Path.home())
desktop = (home+'/Desktop')

image_list = [] # stores a list of file names for every image in the photo directory
button_list = [] # stores Button objects for every image file in photo directory ('unstacked_photos/' by default)
preview_list =[] # stores a list of file names for all images displayed on preview screen in order of appearance
SEPARATOR = 5 # number of black pixels used to separate stacked images
output_image = None # the full-sized stacked PIL.Image object
window_width, window_height = 0,0


# Radio button initialisation
option_layout = tk.StringVar()
option_layout.set('vertical')
option_filetype = tk.StringVar()
option_filetype.set('jpg')

# ---------------------------------- Functions -------------------------------

''' Returns list of filenames for all images in unstacked_photos directory '''
def get_image_list():
    file_list = []
    extensions = ['png','jpg','jpeg']
    os.chdir(photo_directory)
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.split('.')[1] in extensions:
                absolute = os.path.abspath(file)
                file_list.append(absolute)
        break
    os.chdir(main_directory)
    return file_list

''' Takes in a PIL.Image object, resizes it, and returns a PIL.Image object '''
def resize_from_PIL_image(image, max_width = None, max_height = None):
    old_width, old_height = image.size
    
    # Limited by height
    if max_width == None and max_height != None:
        new_height = max_height
        new_width  = int(new_height * (old_width / old_height))
    
     # Limited by width
    elif max_width != None and max_height == None:
        new_width = max_width
        new_height  = int(new_width * (old_height / old_width))
        
    elif max_width != None and max_height != None:
        new_height = max_height
        new_width  = int(new_height * (old_width / old_height))
        if new_width > max_width:
            new_width = max_width
            new_height  = int(new_width * (old_height / old_width))
    
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    return resized_image


''' Takes in a file name and resizes the image, returns it as a Tkinter PhotoImage object '''
def resize_image(filename, max_width = None, max_height = None):
    global photo_directory
    image = Image.open(filename)
    width, height = image.size 
    
    # Limited by height
    if max_width == None and max_height != None:
        new_height = max_height
        new_width  = int(max_height * (width / height))

        
    # Limited by width
    elif max_width != None and max_height == None:
        new_width = max_width
        new_height  = int(max_width * (height / width))

    
    # Limited by width and height
    elif max_width != None and max_height != None:
        new_height = max_height
        new_width  = int(max_height * (width / height))
        if new_width > 500:
            new_width = 500
        new_height  = int(max_width * (height / width))
            
    
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    resized_image = ImageTk.PhotoImage(resized_image)
    return resized_image


''' Takes in a list of file names and returns the smallest height and the smallest width '''
def get_min_dimensions(file_list):
    os.chdir(photo_directory)
    images = [Image.open(x) for x in file_list]
    widths, heights = zip(*(i.size for i in images))
    min_width, min_height = min(widths), min(heights)
    os.chdir(main_directory)
    return min_width, min_height


''' Returns the new dimensions an image should be for a given width and aspect ratio '''
def get_new_vertical_dimensions(dimensions, min_width):
    width, height = dimensions
    ratio = width/height
    new_width = min_width
    new_height = round(min_width/ratio)      
    return new_width, new_height


''' Returns the new dimensions an image should be for a given height and aspect ratio '''
def get_new_horizontal_dimensions(dimensions, min_height):
    width, height = dimensions
    ratio = height/width
    new_height = min_height
    new_width = round(min_height/ratio)      
    return new_width, new_height


''' Takes in a list of file names and returns a list of resized PIL.Image objects, and a list of the new heights and widths '''
def resize_to_min_width_or_height(file_list, min_width, min_height):
    resized_images = []
    for file in file_list:
        image = Image.open(file)
        if option_layout.get() == 'vertical' or option_layout.get() == '2_column':
            new_width, new_height = get_new_vertical_dimensions(image.size, min_width)
        elif option_layout.get() == 'horizontal':
           new_width, new_height = get_new_horizontal_dimensions(image.size, min_height)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_images.append(image)
    new_widths, new_heights = zip(*(i.size for i in resized_images))
    return resized_images, new_widths, new_heights


''' Combines resized PIL.Image objects from a list and returns a single vertical PIL.Image object '''
def create_vertical(new_heights, min_width, resized_images):
    y_offset = 0
    total_height = sum(new_heights)
    new_image = Image.new('RGB', (min_width, total_height))
    for count, im in enumerate(resized_images):
        new_image.paste(im, (0,y_offset+(count*SEPARATOR)))
        y_offset += im.size[1]
    return new_image


''' Combines resized PIL.Image objects from a list and returns a single horizontal PIL.Image object '''
def create_horizontal(new_widths, min_height, resized_images):
    x_offset = 0
    total_width = sum(new_widths)
    new_image = Image.new('RGB', (total_width, min_height))
    for count, im in enumerate(resized_images):
        new_image.paste(im, (x_offset+(count*SEPARATOR), 0))
        x_offset += im.size[0]
    return new_image

''' Creates 2 vertical columns of images and combines them '''
def create_2_column(new_heights, min_width, resized_images):
    
    half_num = round(len(resized_images)/2)
    left_images = resized_images[0:half_num]
    right_images = resized_images[half_num:]
    
    total_height = max(sum(new_heights[0:half_num]), sum(new_heights[half_num:]))
    
    left_column = Image.new('RGB', (min_width, total_height))
    right_column = Image.new('RGB', (min_width, total_height))
    final_image = Image.new('RGB', (min_width*2, total_height))
    
    y_offset = 0
    for count, im in enumerate(left_images):
        left_column.paste(im, (0,y_offset+(count*SEPARATOR)))
        y_offset += im.size[1]
        
    y_offset = 0
    for count, im in enumerate(right_images):
        right_column.paste(im, (0,y_offset+(count*SEPARATOR)))
        y_offset += im.size[1]

    final_image.paste(left_column, (0,0))
    final_image.paste(right_column, (min_width+SEPARATOR,0))

    return final_image


''' Resizes the preview image on screen, updates image width and height labels '''
def resize_preview_exists():
    new_image = resize_from_PIL_image(output_image, max_width=root.winfo_width()-400, max_height =root.winfo_height()-250)
    new_image = ImageTk.PhotoImage(new_image)
    lbl_preview_box['text'] = ''
    lbl_preview_box['image'] = new_image
    lbl_preview_box.image = new_image # prevents garbage collection destroying image
    
    
''' Handles preview box resize if preview image does not exist i.e the screen is blank '''
def resize_preview_not_exists():       
    btn_export['state'] = tk.DISABLED
    lbl_preview_box['image'] = ''
    lbl_preview_box['text'] = 'Add photos to build preview'


''' Updates the preview image if resized, image is added/removed etc. Also handles export, radio button and dimension lable updates '''
def update_preview():   
    os.chdir(photo_directory)    
    lbl_success['text'] = ''
    global output_image
    
    if len(preview_list) != 0:
        
        if option_layout.get() == 'resize':
            output_image = Image.open(preview_list[-1]) # If no images were selected before, or if images were, take the most recent
            lbl_image_width['fg'] = 'black'
            lbl_image_height['fg'] = 'black'
            ent_image_width['state'] = 'normal'
            ent_image_height['state'] = 'normal'
            ent_image_width.delete(0, tk.END)
            ent_image_height.delete(0, tk.END)
            ent_image_width.insert(0, f'{output_image.size[0]}')
            ent_image_height.insert(0, f'{output_image.size[1]}')
            del(preview_list[:-1])


            if ent_image_width.get() != '' and ent_image_height.get() != '':
                btn_export['state'] = tk.NORMAL
            else:
                btn_export['state'] = tk.DISABLED
        
        else:
        
            btn_export['state'] = tk.NORMAL
            min_width, min_height = get_min_dimensions(preview_list)
            resized_images, new_widths, new_heights = resize_to_min_width_or_height(preview_list, min_width, min_height)
            
            if option_layout.get() == 'vertical':
                output_image = create_vertical(new_heights, min_width, resized_images)
            elif option_layout.get() == 'horizontal':
                output_image = create_horizontal(new_widths, min_height, resized_images) 
            elif option_layout.get() == '2_column':
                output_image = create_2_column(new_heights, min_width, resized_images)
        
            ent_image_width['state'] = 'normal'
            ent_image_height['state'] = 'normal'
            ent_image_width.delete(0, tk.END)
            ent_image_height.delete(0, tk.END)
            ent_image_width.insert(0, f'{output_image.size[0]}')
            ent_image_height.insert(0, f'{output_image.size[1]}')
            ent_image_width['state'] = 'disabled'
            ent_image_height['state'] = 'disabled'
            
            
        resize_preview_exists()

    else:

        ent_image_width['state'] = 'normal'
        ent_image_height['state'] = 'normal'
        ent_image_width.delete(0, tk.END)
        ent_image_height.delete(0, tk.END)
        ent_image_width['state'] = 'disabled'
        ent_image_height['state'] = 'disabled'
        
        resize_preview_not_exists()
        
    os.chdir(main_directory)


''' Increases/decreases the preview image with screen resizing '''
def resize(event):
    global window_width, window_height, output_image
    if event.widget.widgetName == "toplevel":
        
        if (window_width != event.width) or (window_height != event.height):
            window_width, window_height = event.width,event.height
            #update_preview()
            if len(preview_list) != 0:
                resize_preview_exists()
                
            else:
                resize_preview_not_exists()   


''' Takes in a Button object and returns the file name string '''
def get_filename_from_button(button):
    global image_list, button_list
    index = button_list.index(button) # find which number button was clicked, e.g. the first (0), the second (1)
    image_name = image_list[index] # find the full size image of the button clicked
    return image_name


''' Handles photo buttons to add/remove photos from the preview screen '''
def click(button):
    if get_filename_from_button(button) in preview_list:
        preview_list.remove(get_filename_from_button(button))
        button.config(relief=tk.RAISED)
    else:
        preview_list.append(get_filename_from_button(button))
        if option_layout.get() != 'resize':
            button.config(relief=tk.SUNKEN)

    update_preview()


''' Checks file name and if valid saves photo  '''
def export():
    if ent_new_filename.get() == '':
        lbl_success['fg'] = 'red'
        lbl_success['text'] = 'File name cannot be empty'
    
    else:
        global output_image
        if ent_image_width.get() != '' and ent_image_height.get() != '':
            
            try:
                output_image = output_image.resize((int(ent_image_width.get()), int(ent_image_height.get())), Image.ANTIALIAS)
                filename = ent_new_filename.get()+'.'+option_filetype.get()
                filename_exists = os.path.exists(main_directory+'/stacked_photos/'+filename)
        
                if filename_exists and lbl_success['text'] != 'Overwrite Existing File?':
                    lbl_success['fg'] = 'orange'
                    lbl_success['text'] = 'Overwrite Existing File?'
                else:
                    lbl_success['fg'] = 'green'
                    lbl_success['text'] = 'Image Saved'
                    os.chdir(main_directory+'/stacked_photos')
                    output_image.save(filename)
                    os.chdir(main_directory)
            except:
                lbl_success['fg'] = 'red'
                lbl_success['text'] = 'Invalid Dimensions'
                
        else:
            lbl_success['fg'] = 'red'
            lbl_success['text'] = 'Empty Dimension(s)'
        
        
''' Removes all images from the preview screen '''
def clear_preview():
    global preview_list
    preview_list.clear()
    for button in button_list:
        button.config(relief=tk.RAISED)
    update_preview()


''' Deletes all image thumbnail buttons from the scrollbar '''
def delete_buttons():
    global button_list
    if len(button_list) > 0:
        for button in button_list:
            button.destroy()
        button_list.clear()


''' Creates image thumbnail button in scrollbar for each image in photo directory '''
def create_buttons(photo_directory):
    global image_list
    image_list = get_image_list()
    for count, filename in enumerate(image_list):
        pic_thumbnail = resize_image(filename, max_height=100)
        pic_button = tk.Button(master=frm_buttons, image = pic_thumbnail, borderwidth=3, bg=bg_colour)
        pic_button.image = pic_thumbnail # This line prevents garbage collection from destroying images after each loop
        pic_button['command'] = lambda pic_button=pic_button: click(pic_button)
        pic_button.grid(row = count, column = 0, pady = 10, padx=40)
        button_list.append(pic_button)


''' Changes the photo directory, deletes old thumbnail images and creates new ones '''
def update_directory(clicked_directory):
    global photo_directory, image_list, output_image
    delete_buttons()
    image_list.clear()
    #clear_preview()
    if clicked_directory == 'Desktop':
        photo_directory = desktop
    elif clicked_directory == 'Unstacked Photos':
        photo_directory = main_directory+'/unstacked_photos'
    else:
        photo_directory = desktop+'/'+clicked_directory
    create_buttons(photo_directory)    
    
    
''' Resets buttons and preview screen when switching to resize mode '''
def enable_resize():
    global preview_list
    preview_list.clear()
    for button in button_list:
        button.config(relief=tk.RAISED)
    update_preview()
    #ent_image_width.delete(0, tk.END)
    #ent_image_height.delete(0, tk.END)
    
    
''' Greys out dimensions labels and entries - called by other radio buttons when disabling resize mode '''
def disable_resize():
    ent_image_width['state'] = 'disabled'
    ent_image_height['state'] = 'disabled'
    lbl_image_width['fg'] = 'gray'
    lbl_image_height['fg'] = 'gray'
    ent_image_width.delete(0, tk.END)
    ent_image_width.delete(0, tk.END)
    update_preview()
    
    
''' Enters borderless fullscreen mode '''
def full_screen():
    root.attributes('-fullscreen', True)


''' Enters windowed mode '''
def windowed():
    root.attributes('-fullscreen', False)
    
    
''' Displays help message box '''   
def help_message():
    tk.messagebox.showinfo(title='Help', message='For help refer to the help.txt file in the PhotoStack directory')


# -------------------------------- Function Calls -----------------------------
        
root.bind("<Configure>", resize)    

# ----------------------------------- Widgets ---------------------------------  

''' Menu Bar '''
# Create Menu Bar
menubar = tk.Menu(root)

# File
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=clear_preview)
filemenu.add_command(label="Save", command=export)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

# View
viewmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
viewmenu.add_command(label="Full Screen (Borderless)", command=full_screen)
viewmenu.add_command(label="Windowed", command=windowed)

# Help
helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Help Index", command=help_message)
root.config(menu=menubar)


''' Photos Label '''
frm_photos_label = tk.Frame(master=root)
frm_photos_label.grid(row=0, column=0, sticky='nesw', ipadx=45, ipady=10)
lbl_photos = tk.Label(master=frm_photos_label, text='Photos',fg='black', font = "Verdana 30 bold")
lbl_photos.pack()


''' Scrollbar '''
frm_scrollbar = tk.Frame(master=root)
frm_scrollbar.grid(row=1, column=0, rowspan=2, sticky='nesw')

directories = next(os.walk(desktop))[1]
directories.insert(0, 'Desktop')
directories.insert(0, 'Unstacked Photos')
clicked = tk.StringVar()
clicked.set(directories[0])
drop = tk.OptionMenu(frm_scrollbar, clicked, *directories, command=update_directory)
drop.pack()

canvas = tk.Canvas(frm_scrollbar, height = 600, width = 200)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=(0, 25))
scrollbar = tk.Scrollbar(frm_scrollbar, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 25))
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
frm_buttons = tk.Frame(canvas)
canvas.create_window((0,0), window=frm_buttons, anchor="nw")


create_buttons(photo_directory)


''' PhotoStack Studio Label '''
frm_title_label = tk.Frame(master=root)
frm_title_label.grid(row=0, column=1, columnspan=3, sticky='nsew')
lbl_title = tk.Label(master=frm_title_label, text='PhotoStack Studio',fg='black', font = "Verdana 30 bold")
lbl_title.pack()


''' Preview Box '''
frm_preview_box = tk.Frame(master = root, width=500, height=500)
frm_preview_box.grid(row=1, column=1, columnspan=3)
lbl_preview_box = tk.Label(master=frm_preview_box, bg=bg_colour, text='Add photos to build preview', fg='white', font = "Verdana 20 bold")
lbl_preview_box.grid(row=0, column=0, sticky='nesw')


''' Options Bar '''
# Frame
frm_option_bar = tk.Frame(master = root, width=500, height=100)
frm_option_bar.grid(row=2, column=1, columnspan=3, sticky='nesw')

# Layout
lbl_layout = tk.Label(frm_option_bar, text='Layout')
rb_vertical = tk.Radiobutton(frm_option_bar, text='Vertical', variable=option_layout, value='vertical', command=disable_resize)
rb_horiztonal = tk.Radiobutton(frm_option_bar, text='Horizontal', variable=option_layout, value='horizontal', command=disable_resize)
rb_resize = tk.Radiobutton(frm_option_bar, text='Resize', variable=option_layout, value='resize', command=enable_resize)
rb_2_column = tk.Radiobutton(frm_option_bar, text='2 Columns', variable=option_layout, value='2_column', command=disable_resize)

lbl_layout.grid(row=0, column=0, columnspan=2, sticky='nesw', padx=(20,0), pady=10)
rb_vertical.grid(row=1, column=0, sticky='nesw')
rb_horiztonal.grid(row=2, column=0, sticky='nesw', padx=(15,0))
rb_2_column.grid(row=1, column=1, sticky='nesw', padx=(25,0))
rb_resize.grid(row=2, column=1, sticky='nesw')

# Dimensions
frm_dimensions = tk.Frame(master=frm_option_bar)
lbl_dimensions = tk.Label(master=frm_dimensions, text='Dimensions', fg='black')
lbl_image_width = tk.Label(master=frm_dimensions, text='Width:', fg='gray')
lbl_image_height = tk.Label(master=frm_dimensions, text='Height:', fg='gray')
ent_image_width = tk.Entry(master=frm_dimensions, text='', state='disabled', width=8)
ent_image_height = tk.Entry(master=frm_dimensions, text='', state='disabled', width=8)

frm_dimensions.grid(row=0, column=2, rowspan=3, sticky='nesw', padx=(20,0), pady=(15,0))
lbl_dimensions.grid(row=0, column=0, columnspan=2, sticky='nesw')
lbl_image_width.grid(row=1, column=0, sticky='nesw', pady=10)
lbl_image_height.grid(row=2, column=0, sticky='nesw', pady=10)
ent_image_width.grid(row=1, column=1, pady=10)
ent_image_height.grid(row=2, column=1, pady=10)

# File Type
lbl_filetype = tk.Label(frm_option_bar, text='File Type')
rb_jpg = tk.Radiobutton(frm_option_bar, text='.JPG', variable=option_filetype, value='jpg')
rb_png = tk.Radiobutton(frm_option_bar, text='.PNG', variable=option_filetype, value='png')
lbl_filetype.grid(row=0, column=3, columnspan=2, sticky='nesw')
rb_jpg.grid(row=1, column=3, columnspan=2, sticky='nesw')
rb_png.grid(row=2, column=3, columnspan=2, sticky='nesw', padx=(5,0))

# File Name
lbl_new_filename = tk.Label(master=frm_option_bar, text='Filename: ')
ent_new_filename = tk.Entry(master=frm_option_bar)
ent_new_filename.insert(0, 'untitled')
btn_export = tk.Button(master=frm_option_bar, text='Export', width=15, height=3, command=export, state=tk.DISABLED)
lbl_success = tk.Label(master=frm_option_bar, text='', fg='green')
lbl_new_filename.grid(row=0,column=5)
ent_new_filename.grid(row=1,column=5)

# Export Button
btn_export.grid(row=1, column=6, rowspan=2)
lbl_success.grid(row=3, column=6, columnspan=2)

# Right Edge of Screen
frm_edge = tk.Frame(master = root, width=25)
frm_edge.grid(row=0, column=2, rowspan=3, sticky='nesw')


''' Row/Column Configuration '''
root.columnconfigure(1, weight=3, minsize=600)
root.rowconfigure(1, weight=1, minsize=50)
for col in range(0,7):
    frm_option_bar.columnconfigure(col, weight=1)
    
for col in range(0,2):
    frm_dimensions.columnconfigure(col, weight=1)


''' Mainloop '''
root.mainloop()

