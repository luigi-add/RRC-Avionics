from tkinter import *
import tkinter.font as tkfont
import tkinter.messagebox
from time import sleep
import os,sys,random
from PIL import ImageTk,Image

#Defines frame dimensions
height=220
width=450


'''
smallmap_corners = {topleft: [32.955651, -106.930123], topright: [32.955651, -106.892924],
                    botleft: [32.937436, -106.930123], botright: [32.937436, -106.892924]}
largemap_corners = {topleft: [32.979024, -106.967445], topright: [32.979024, -106.858726],
                    botleft: [32.925260, -106.930123], botright: [32.925260, -106.858726]}
change'''

class Map:

    # ***************** Instantiate *********************
    def __init__(self, master):
        self.__master = master

        self.firstImage = 0
    # Sets frame
        if __name__ == '__main__':
            self.__master.resizable(width=False, height=False)
            self.__master.geometry('{}x{}'.format(370, 220))
            self.__frame = Frame(self.__master)
        else:
            self.__mainFrame = self.__master
            self.__frame = Frame(self.__mainFrame)
        self.__frame.pack()

    # Runs Map functions
        self.__label_map = None
        self.__load_first_maps()
        self.__load_Circle()
        self.__map_parameters()
        if __name__ == '__main__':
            self.__getRandomNumber()  # Gets random Coordinates for Path
        else:
            self.__coordiantes = [0,0]
        self.__choose_first_map()
        self.__setup_display_map()  # Display the map on the Window/Fram FOR THE FIRST TIME
        self.__run()
    # *****************************************************

    #**************** Defined Functions  ******************
        # Runs all functions
    def __run(self):
        self.update()
        self.__map = ImageTk.PhotoImage(self.__load_map)
        self.__label_map.config(image = self.__map)
        self.__master.after(700, self.__run)



    def update(self):
        if __name__ == '__main__':
            self.__getRandomNumber()  # Gets random Coordinates for Path
        try:
            self.__choose_maps()  # Chooses Small or Large Map based on location of Crosshair and pastes Images over New Map files
            self.__load_mod_maps()  # Loads Modified Maps
        except:
            pass

        # Loads Original Large and Small Map
    def __load_first_maps(self):
        if self.firstImage == 0:
            self.__load_smallmap = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Small Map.png")
            self.__load_smallmap.load()
            self.__load_smallmap.thumbnail(size=(width, height))
            self.__load_largemap = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map.png")
            self.__load_largemap.load()
            self.__load_largemap.thumbnail(size=(width, height))
        else:
            self.__load_smallmap = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Small Map1.png")
            self.__load_smallmap.load()
            self.__load_smallmap.thumbnail(size=(width, height))
            self.__load_largemap = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map1.png")
            self.__load_largemap.load()
            self.__load_largemap.thumbnail(size=(width, height))

        # Loads Modified Maps
    def __load_mod_maps(self):
        self.__load_largemap = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map1.png")
        self.__load_largemap.load()
        self.__load_largemap.thumbnail(size=(width, height))
        self.__load_smallmap.load()
        self.__load_smallmap = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Small Map1.png")
        self.__load_smallmap.thumbnail(size=(width, height))

        # Loads Crosshair
    def __load_Crosshair(self):
        self.__load_crosshair = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../appImages/Crosshair.png")
        self.__crosshair_size = (20, 20)
        self.__load_crosshair.thumbnail(size=(self.__crosshair_size[0], self.__crosshair_size[1]))

    def __load_Circle(self):
        self.__load_circle = Image.open(os.path.dirname(os.path.realpath(__file__))+"/../appImages/circle.png")
        self.__circle_size = (5, 5)
        self.__load_circle.thumbnail(size=(self.__circle_size[0], self.__circle_size[1]))

        # Coordinates of Small and Large Map sides
    def __map_parameters(self):
        self.__smallmap_side = {'top': 32.955651, 'bot': 32.937436, 'left': -106.930123, 'right': -106.892924}
        self.__largemap_side = {'top': 32.979024, 'bot': 32.925260, 'left': -106.967445, 'right': -106.858726}


        # Random test Coordinates
    def __getRandomNumber(self):
        self.__coordiantes = [round(random.uniform(self.__largemap_side['bot'], self.__largemap_side['top']), 6), round(random.uniform(self.__largemap_side['right'], self.__largemap_side['left']), 6)]
        print(self.__coordiantes)

        # Converts latitude/longitude coordinates to x,y pixels for Crosshair placement
    def __convert_pixel(self):
        # Sets length, width, and border values of map frame in terms of latitude and longitude coordinates
        self.__latitude_length = self.__map_side['top'] - self.__map_side['bot']
        self.__longitude_length = (self.__map_side['left'] - self.__map_side['right']) * (-1)

        # Derives proportionality between latitude/longitude coordinates and x,y direction pixels
        y_factor = height / self.__latitude_length
        x_factor = width / self.__longitude_length

        # Converts latitude/longitude coordinates to x,y pixel parameters
        y = (self.__map_side['top'] - self.__coordiantes[0]) * y_factor
        x = (self.__map_side['left'] - (self.__coordiantes[1])) * (-1) * x_factor

        # Seperates integers and decimals
        self.__pixel_integer = [int(y), int(x)]
        print(int(y), int(x))
        self.__pixel_decimals = (y % 1, x % 1)
        print(y % 1, x % 1)


        # {Chooses *****Ininial***** Map Image, Merges Path and Map, Saves the latter as a .png file and notifies user if Rocket leaves Small Map} in __init__
    def __choose_first_map(self):
            # Chooses Large Map if Rocket leaves top or bot and left or right sides of Small Map
        if (self.__coordiantes[0] > self.__smallmap_side['top'] or self.__coordiantes[0] < self.__smallmap_side['bot']) or (self.__coordiantes[1] < self.__smallmap_side['left'] or self.__coordiantes[1] > self.__smallmap_side['right']):
            print("Rocket leaving competition area!!!")

            self.__map_side = self.__largemap_side.copy()
            self.__convert_pixel()
            self.__load_largemap.paste(self.__load_circle, (self.__pixel_integer[1] - int(self.__circle_size[0] / 2), self.__pixel_integer[0] - int(self.__circle_size[1] / 2)), self.__load_circle)
            self.__load_largemap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map1.png")
            self.__load_smallmap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Small Map1.png")
            self.__load_map = self.__load_largemap

            # Chooses Small Map if Rocket enters top or bot and left or right sides of Small map
        elif self.__coordiantes[0] < self.__smallmap_side['top'] or self.__coordiantes[0] > self.__smallmap_side['bot'] or (self.__coordiantes[1] > self.__smallmap_side['left'] or self.__coordiantes[1] < self.__smallmap_side['right']):

            self.__map_side = self.__smallmap_side.copy()
            self.__convert_pixel()
            self.__load_smallmap.paste(self.__load_circle, (self.__pixel_integer[1] - int(self.__circle_size[0] / 2), self.__pixel_integer[0] - int(self.__circle_size[1] / 2)), self.__load_circle)
            self.__load_smallmap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Small Map1.png")
            self.__load_largemap.paste(self.__load_circle, (self.__pixel_integer[1] - int(self.__circle_size[0] / 2), self.__pixel_integer[0] - int(self.__circle_size[1] / 2)), self.__load_circle)
            self.__load_largemap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map1.png")
            self.__load_map = self.__load_smallmap

        # {Chooses *****Consecutive***** Map Images, Merges Path and Map, Saves the latter as a .png file and notifies user if Rocket leaves Small Map} in run()
    def __choose_maps(self):
            # Chooses Large Map if Rocket leaves top or bot and left or right sides of Small Map
        if (self.__coordiantes[0] > self.__smallmap_side['top'] or self.__coordiantes[0] < self.__smallmap_side['bot']) or (self.__coordiantes[1] < self.__smallmap_side['left'] or self.__coordiantes[1] > self.__smallmap_side['right']):
            print("Rocket leaving competition area!!!")

            self.__map_side = self.__largemap_side.copy()
            self.__convert_pixel()
            self.__load_largemap.paste(self.__load_circle, (self.__pixel_integer[1] - int(self.__circle_size[0] / 2), self.__pixel_integer[0] - int(self.__circle_size[1] / 2)),self.__load_circle)
            self.__load_largemap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map1.png")
            self.__load_map = self.__load_largemap

            # Chooses Small Map if Rocket enters top or bot and left or right sides of Small map
        elif self.__coordiantes[0] < self.__smallmap_side['top'] or self.__coordiantes[0] > self.__smallmap_side['bot'] or (self.__coordiantes[1] > self.__smallmap_side['left'] or self.__coordiantes[1] < self.__smallmap_side['right']):

            self.__map_side = self.__smallmap_side.copy()
            self.__convert_pixel()
            self.__load_smallmap.paste(self.__load_circle, (self.__pixel_integer[1] - int(self.__circle_size[0] / 2), self.__pixel_integer[0] - int(self.__circle_size[1] / 2)), self.__load_circle)
            self.__load_smallmap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Small Map1.png")
            self.__map_side = self.__largemap_side.copy()
            self.__convert_pixel()
            self.__load_largemap.paste(self.__load_circle, (self.__pixel_integer[1] - int(self.__circle_size[0] / 2), self.__pixel_integer[0] - int(self.__circle_size[1] / 2)), self.__load_circle)
            self.__load_largemap.save(os.path.dirname(os.path.realpath(__file__))+"/../Maps/Large Map1.png")
            self.__load_map = self.__load_smallmap


        # Displays Map and Path
    def __setup_display_map(self):
        self.__map = ImageTk.PhotoImage(self.__load_map)
        self.__label_map = Label(self.__frame, image=self.__map)
        self.__label_map.image = self.__map
        self.__label_map.pack(side = TOP, anchor =NW)

    def setCoordinate(self, coordinates):
        self.__coordiantes = coordinates

    def getCoordinates(self):
        return self.__coordiantes

    def setFrame(self, frame):
        self.__frame = frame


    # *****************************************************

#   ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **

if __name__ == '__main__':
    root = Tk()
    run_map = Map(root)
    root.mainloop()





#self.__load_map.paste(self.__load_crosshair, (self.__pixel_integer[1] - int(self.__crosshair_size[0] / 2),self.__pixel_integer[0] - int(self.__crosshair_size[1] / 2)), self.__load_crosshair)  # Positions and blends Crosshair with map

#self.__map_canvas = Canvas(self.__master, height=height, width=width, bg="blue")
#self.__display = self.__map_canvas.create_image(width / 2, height / 2, image=self.__map)
#self.__map_canvas.pack()
