import Tkinter as tk

# Allow user to draw boxes in an image
class ImageBoxer:
    def __init__(self, root):
        self.downEvent = None
        self.dragEvent = None
        self.dragRect = None
        self.rectangles = []

        self.root = root
        self.root.title("Image Boxer")

        self.image = tk.PhotoImage(file=r'image.gif')

        # displays image and boxes
        self.canvas = tk.Canvas(self.root, width=self.image.width(), height=self.image.height())
        self.canvas.bind("<Button-1>", self.canvasMouseDown)
        self.canvas.bind("<ButtonRelease-1>", self.canvasMouseRelease)
        self.canvas.bind("<B1-Motion>", self.canvasMouseMotion)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.canvas.pack(side=tk.LEFT)

        # let user double-click to delete box
        self.listbox = tk.Listbox(self.root)
        self.listbox.bind("<Double-Button-1>", self.listboxDoubleClick)
        self.listbox.pack(side=tk.LEFT)

    # delete box
    def listboxDoubleClick(self, event):
        index = self.listbox.curselection()[0]
        self.listbox.delete(index)
        self.canvas.delete(self.rectangles[index])
        del self.rectangles[index]

    # drag size of box
    def canvasMouseMotion(self, event):
        self.dragEvent = event
        if self.dragRect:
            self.canvas.delete(self.dragRect)
        self.dragRect = self.canvas.create_rectangle(self.downEvent.x, self.downEvent.y, self.dragEvent.x, self.dragEvent.y, width=2, outline="#ff0000")

    # add box
    def canvasMouseRelease(self, event):
        self.canvas.delete(self.dragRect)
        self.rectangles.append(self.canvas.create_rectangle(self.downEvent.x, self.downEvent.y, self.dragEvent.x, self.dragEvent.y, width=2, outline="#ff0000"))
        self.listbox.insert(tk.END, str(len(self.rectangles)))
        print(len(self.rectangles))

    # add box
    def canvasMouseDown(self, event):
        self.downEvent = event

if __name__ == "__main__":
    root = tk.Tk()
    imageBoxer = ImageBoxer(root)
    root.mainloop()
