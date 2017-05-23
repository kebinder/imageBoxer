import Tkinter as tk
from PIL import Image, ImageTk, ImageGrab

# Allow user to draw boxes in an image
class ImageBoxer:
    def __init__(self, root):
        self.downEvent = None
        self.dragEvent = None
        self.dragRect = None
        self.rectangles = []

        #self.deleted to keep track of removed rectangles
        self.deleted = []

        self.root = root
        self.root.title("Image Boxer")

        # create a frame for listbox
        self.frame = tk.Frame(root)
        self.frame.grid(row=0,column=1)
        #self.frame.pack(side=tk.RIGHT)

        self.image = tk.PhotoImage(file=r'image.gif')

        # displays image and boxes
        self.canvas = tk.Canvas(self.root, width=self.image.width(), height=self.image.height())
        self.canvas.bind("<Button-1>", self.canvasMouseDown)
        self.canvas.bind("<ButtonRelease-1>", self.canvasMouseRelease)
        self.canvas.bind("<B1-Motion>", self.canvasMouseMotion)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        #self.canvas.pack(side=tk.LEFT)
        self.canvas.grid(row=0,column=0)

        # let user double-click to delete box
        self.listbox = tk.Listbox(self.frame)
        self.listbox.bind("<Double-Button-1>", self.listboxDoubleClick)
        #self.listbox.pack(side=tk.LEFT,padx=5,pady=5)
        self.listbox.grid(row=0,column=3)

        # added scrollbar for listbox
        self.scrollbar = tk.Scrollbar(self.frame)
        #self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.scrollbar.grid(row=0,column=4,sticky="NS")
        # attach listbox to scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # added undo button for rectangles
        self.undo = tk.Button(self.root,text="Undo",command=self.undoRectangle)
        self.undo.grid(row=1,column=1)
       # self.undo.pack(side=tk.LEFT,padx=5,pady=5)

        # added redo button for rectangles
        self.redo = tk.Button(self.root,text="Redo",command=self.redoRectangle)
        self.redo.grid(row=1,column=2)
        #self.redo.pack(side=tk.LEFT,padx=5,pady=5)

        # added entry to set image name when saving
        tk.Label(self.root,text="Image Name: ").grid(row=2,column=1)
        self.imageName = tk.Entry(self.root)
        self.imageName.grid(row=2,column=2)

        # added reset button
        self.reset = tk.Button(self.root,text="Reset",command=self.resetAll)
        self.reset.grid(row=3,column=1)

        # added save picture button (windows only)
        self.save = tk.Button(self.root,text="Save",command=self.saveImage)
        self.save.grid(row=3,column=2)

        
    # delete box
    def listboxDoubleClick(self, event):
        if (len(self.listbox.curselection()) > 0): #added if to prevent index out of range error
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
             # adding coordinates of deleted rectangles to self.deleted
            self.deleted.append(self.canvas.coords(self.rectangles[index]))
            self.canvas.delete(self.rectangles[index])
            del self.rectangles[index]
        self.updateListbox()

    # drag size of box
    def canvasMouseMotion(self, event):
        self.dragEvent = event
        if self.dragRect:
            self.canvas.delete(self.dragRect)
        self.dragRect = self.canvas.create_rectangle(self.downEvent.x, self.downEvent.y, self.dragEvent.x, self.dragEvent.y, width=2, outline="#ff0000")

    # add box
    def canvasMouseRelease(self, event):
        self.canvas.delete(self.dragRect)
        if (self.dragEvent != None and self.downEvent != None):
            # create_rectangle returns object id. object id is unique to canvas
            self.rectangles.append(self.canvas.create_rectangle(self.downEvent.x, self.downEvent.y, self.dragEvent.x, self.dragEvent.y, width=2, outline="#ff0000"))
            self.listbox.insert(tk.END, str(len(self.rectangles)))
            print(len(self.rectangles))
        # set back self.dragEvent to None. If left without, clicking another area will
        # draw another rectangle with starting point = dragEvent, endpoint = clickEvent
        self.dragEvent = None

    # add box
    def canvasMouseDown(self, event):
        self.downEvent = event

    # undo rectangle in order of most recently added
    def undoRectangle(self):
        if len(self.rectangles) > 0:

            index = len(self.rectangles)-1
            self.listbox.delete(index)
            self.deleted.append(self.canvas.coords(self.rectangles[index]))
            self.canvas.delete(self.rectangles[index])
            del self.rectangles[index]
        self.updateListbox()

    # redo rectangle in order of most recently deleted
    def redoRectangle(self):
        if len(self.deleted) > 0:
            index = len(self.deleted)-1
            coords = self.deleted[index]
            self.rectangles.append(self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], width=2, outline="#ff0000"))
            self.listbox.insert(tk.END,str(len(self.rectangles)))
            del self.deleted[index]

    def resetAll(self):
        # Get the amount of rectangles and delete them from listbox/canvas/rectangles
        amount = len(self.rectangles)
        # Delete the first index to not go out of range
        for i in range(amount):
            self.canvas.delete(self.rectangles[0])
            self.listbox.delete(0)
            del self.rectangles[0]
        self.deleted = []
        self.imageName.delete(0, tk.END)

    # Used to fix numbers in listbox when deleting from earlier index and adding another box.
    # Previously doing so will create duplicate numbers because listbox is inserting str(len(self.rectangles))
    def updateListbox(self):
        self.listbox.delete(0,tk.END)
        for i in range(len(self.rectangles)):
            self.listbox.insert(tk.END,str(i+1))
        
    def saveImage(self):
        image = [self.canvas.canvasx(0),self.canvas.canvasy(0),self.canvas.canvasx(1),self.canvas.canvasy(1)]
        #self.canvas.postscript(file="out.eps")
        #image = Image.open("out.eps")
        #image.save("out.jpg")
        # Get x,y position of top left of window
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        print(self.imageName)
        # Setup coordinates of the canvas to take screenshot
        image[0] = self.root.winfo_x()+(self.canvas.winfo_width()-self.canvas.winfo_width())+10
        image[1] = self.root.winfo_y()+(self.root.winfo_height()-self.canvas.winfo_height())
        image[2] = abs(self.canvas.winfo_width()+window_x)
        image[3] = abs(self.canvas.winfo_height()+window_y)
        image = ImageGrab.grab(bbox=(image))
        image.show()
        image.save(self.imageName.get()+".jpg")
        #self.savedimage = ImageGrab.grab(bbox=image)
        #self.savedimage.show()
        #self.savedimage.save("out.jpg")
        print('Screenshoot of tkinter.Canvas saved in "'+self.imageName.get()+'.jpg"')

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(803,452)
    imageBoxer = ImageBoxer(root)
    root.mainloop()
