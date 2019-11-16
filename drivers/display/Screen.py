from ..Driver import Driver
from tkinter import *
from typing import List
from threading import Thread

class Screen(Driver):

    CanvasWidth: int = 300
    CanvasHeight: int = 300

    def open(self, width: int, height: int):

        self.virtualImage: List[List[str]] = self._createVirtualImage(width, height)

        root = Tk()
        zimg = self._drawImage(self.virtualImage)
        canvas = Canvas(root, width=Screen.CanvasWidth, height=Screen.CanvasHeight, bg="#000000")
        canvas.create_image(0, 0, anchor="nw", image=zimg)
        canvas.pack()

        self.canvas: Canvas = canvas
        self.root: Tk = root

        try:
            Thread(mainloop).start()
        except:
            pass

    def _createVirtualImage(self, width: int, height: int) -> List[List[str]]:
        img: List[List[str]] = []
        for x in range(width):
            row: List[str] = []
            for y in range(height):
                row.append("#00ff00")
            img.append(row)
        return img

    def _drawImage(self, virtualImage: List[List[str]]) -> PhotoImage:
        width: int = len(virtualImage)
        height: int = len(virtualImage[0])
        img: PhotoImage = PhotoImage(width=width, height=height)
        for x in range(len(virtualImage)):
            for y in range(len(virtualImage[x])):
                img.put(virtualImage[x][y], (x, y))
        return img.zoom(int(Screen.CanvasWidth / width), int(Screen.CanvasHeight / height))

    def write(self, x: int, y: int, value: str) -> bool:
        if not (0 <= x < len(self.virtualImage)):
            return False
        row = self.virtualImage[x]
        if not (0 <= y < len(row)):
            return False
        row[y] = value

    def flush(self):
        self.canvas.delete("all")
        img = self._drawImage(self.virtualImage)
        print(self.virtualImage)
        self.canvas.create_image(0, 0, anchor="nw", image=img)
        self.canvas.pack()
        self.canvas.bell()
        self.canvas.update()
        self.canvas.update_idletasks()
        self.root.after(200)
        try:
            Thread(mainloop).start()
        except:
            pass