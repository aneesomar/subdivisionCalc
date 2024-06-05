
import time
import pandas as pd
import numpy as np
import math
import multiprocessing


def calculate_area(XSUB3, YSUB3, XSUB2, YSUB1, YSUB2, cords, areaPlot, area1, PlannedAreaOf1):
    distance = 0


if __name__ == "__main__":

    start = time.time()

    # opens the excel data file with all points
    try:
        cords = pd.read_excel('data.xlsx')

    except FileNotFoundError:
        print("could not open file")
        exit()

    print(cords)

    pointsyx = []

    # makes a list of x and y cords of all points

    for i in range(12):
        y = (cords.y[i])
        x = (cords.x[i])
        pointsyx.append((x, y))

    # print(pointsyx)

    print()
    print("question 2")
    print()

    areaPlot = 7.6237*10000
    PlannedAreaOf1 = areaPlot*(1/3)
    print("Brief Area : ", PlannedAreaOf1)

    # calculates the area given a set of co-ordinates in the form [(x1,y1),.....(xn,yn)]

    def area(cords):

        n = len(cords)
        area = 0.0

        for i in range(n):
            x1, y1 = cords[i]
            x2, y2 = cords[(i + 1) % n]
            area += (x1 * y2) - (x2 * y1)

        return abs(area) / 2.0

    # calcualtes a join between two points with x and y co-ordinates

    def join(cord_y_1, cord_x_1, cord_y_2, cord_x_2):

        dy = cord_y_2-cord_y_1
        dx = cord_x_2-cord_x_1

        angle = math.atan(dy/dx)

        angle = np.degrees(angle)

        if dx < 0 and dy < 0:
            finalangle = angle + 180

        if dx >= 0 and dy < 0:

            finalangle = angle + 180

        if dx < 0 and dy > 0:

            finalangle = angle+360

        if dx > 0 and dy > 0:
            finalangle = angle

        distance = np.sqrt(dy**2+dx**2)

        if finalangle > 360:

            return finalangle-360, distance

        elif finalangle < 0:

            return finalangle+360, distance

        else:
            return finalangle, distance

    # calcualtes a polar given co-oridnates for one point and a direction and distance to the next point

    def polar(y1, x1, distance, direction):

        x2 = x1 + distance*np.cos(np.radians(direction))
        y2 = y1 + distance*np.sin(np.radians(direction))
        return (x2, y2)

    # converts from decimal degrees to dms

    def dec2dms(Dec):

        d = int(Dec)
        m = int(abs(Dec - d) * 60)
        s = round((((abs(Dec - d) * 60)-m)*60), 0)

        return d, m, s

    # converts from dms to decimal degrees

    def dms2dec(dms):
        degrees, minutes, seconds = dms.split(",")
        degrees = eval(degrees)
        minutes = eval(minutes)
        seconds = eval(seconds)
        decimal_degrees = degrees + minutes / 60 + seconds / 3600
        return decimal_degrees

    # calc for sub 1 and sub 2

    area1 = 0
    distanceJP = 0
    distanceamount = 0
    directionJP = (dms2dec("47,45,40"))+90
    directionJK = dms2dec("124,51,40")
    directionHJ = dms2dec("47,45,40")
    directionGH = dms2dec("305,36,30")
    directionPSUB2 = (directionHJ)+180
    directionPSUB1 = (directionHJ)
    directionHSUB2 = directionGH - (180)
    dirctionSUB1SUB2 = directionHJ + (180)

    while area1 < PlannedAreaOf1:

        # polar from J to P

        polarJP = polar(cords.y[8], cords.x[8], distanceJP, directionJP)

        # intersection of P and J to get SUB3

        XSUB1 = (cords.x[8]) + (((polarJP[1]-cords.y[8])-((polarJP[0]-cords.x[8])*(np.tan(np.radians(directionHJ))))) / (
            np.tan(np.radians(directionJK))-np.tan(np.radians(directionHJ))))

        YSUB1 = cords.y[8] + (XSUB1 - cords.x[8]) * \
            (np.tan(np.radians(directionJK)))

        SUB1 = (XSUB1, YSUB1)

        # intersection of P and H to get SUB3

        XSUB2 = (polarJP[0]) + (((polarJP[1])-cords.y[7])-(((polarJP[0])-cords.x[7]) *
                                                           math.tan(math.radians(directionHSUB2))))/(math.tan(math.radians(directionHSUB2)) - math.tan(math.radians(dirctionSUB1SUB2)))

        YSUB2 = (polarJP[1]) + ((XSUB2-(polarJP[0])) *
                                math.tan(math.radians(dirctionSUB1SUB2)))

        SUB2 = (XSUB2, YSUB2)

        # area calc for area1

        YX1 = cords.y[8] * cords.x[7]
        YX2 = cords.y[7] * XSUB2
        YX3 = YSUB2 * XSUB1
        YX4 = YSUB1 * cords.x[8]
        totalYX = YX1 + YX2 + YX3 + YX4

        XY1 = cords.x[8] * cords.y[7]
        XY2 = cords.x[7] * YSUB2
        XY3 = XSUB2 * YSUB1
        XY4 = XSUB1 * cords.y[8]
        totalXY = XY1 + XY2 + XY3 + XY4

        area1 = (totalYX-totalXY)/2  # area of section 1

        # increase distance to P
        distanceJP += 0.0001

        # counter to see how many distances have been tried
        distanceamount += 1

    print("Calculated Area of section 1 : ", area1)

    print("SUB1(x,y):", SUB1)
    print("SUB2(x,y):", SUB2)
    print("Tried ", distanceamount, "distances in ",
          round((time.time()-start), 4), "seconds")

    print()

    print("performing direction check")

    joinJSUB1 = join(cords.y[8], cords.x[8], SUB1[1], SUB1[0])

    joinHSUB2 = join(cords.y[7], polarJP[1], SUB2[1], SUB2[0])

    joinSUB1SUB2 = join(SUB1[1], SUB1[0], SUB2[1], SUB2[0])

    print("join from SUB1 to SUB2 is ",
          round(joinSUB1SUB2[1], 3), "m at ", dec2dms(joinSUB1SUB2[0]), "DMS")

    print("direction should be:", dec2dms(dirctionSUB1SUB2))

    print()
    print("performing area check")
    print("brief Area : ", round(PlannedAreaOf1, 2),
          "Calculated Area : ", round(area1, 2))

    print()

    area2 = 0
    area3 = 0
    distanceSUB1toSUB3 = 0
    XSUB3 = XSUB2+0.001
    distances = 0
    start = time.time()

    while XSUB1 > XSUB3 > XSUB2:

        gradient = (YSUB1 - YSUB2)/(XSUB1 - XSUB2)

        dx = XSUB1 - XSUB3
        dy = gradient*dx

        YSUB3 = YSUB1 - dy

        SUB3 = (XSUB3, YSUB3)

        YX1 = YSUB3 * XSUB2
        YX2 = YSUB2 * cords.x[6]
        YX3 = cords.y[6] * cords.x[5]
        YX4 = cords.y[5] * cords.x[4]
        YX5 = cords.y[4] * cords.x[3]
        YX6 = cords.y[3] * XSUB3

        totalYX = YX1 + YX2 + YX3 + YX4 + YX5 + YX6

        XY1 = XSUB3 * YSUB2
        XY2 = XSUB2 * cords.y[6]
        XY3 = cords.x[6] * cords.y[5]
        XY4 = cords.x[5] * cords.y[4]
        XY5 = cords.x[4] * cords.y[3]
        XY6 = cords.x[3] * YSUB3
        totalXY = XY1 + XY2 + XY3 + XY4 + XY5 + XY6

        area2 = (totalYX-totalXY)/2  # area of section 2

        area3 = areaPlot - area2 - area1

        if area2 >= PlannedAreaOf1:
            break

        XSUB3 += 0.001
        distances += 1

    print("tried ", distances, "distances in ",
          round((time.time()-start), 4), "seconds")
    print("SUB3(x,y):", SUB3)

    print()

    print("performing area check:")

    print("area of section 2 and 3 are : ", round(
        area2, 2), "m^2", round(area3, 2), "m^2")

    print("brief area of section 2 and 3 are : ", round(PlannedAreaOf1, 2))

    print()

    print("area1+area2+area3 = ", round(area1+area2+area3, 2), "m^2")

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import tkinter as tk
    import pandas as pd

    # Load the data
    cords = pd.read_excel('tut02.xlsx')

    # Create the root window
    root = tk.Tk()
    root.title("Coordinates Plot")

    # Create a Figure
    fig = plt.Figure(figsize=(5, 5), dpi=100)

    # Add a subplot to the figure
    plot = fig.add_subplot(111)

    # Plot the data
    plot.scatter(cords.x, cords.y)
    plot.scatter(XSUB1, YSUB1)
    plot.scatter(XSUB2, YSUB2)
    plot.scatter(XSUB3, YSUB3)

    # Draw lines between the points
    plot.plot(cords.x, cords.y, 'r-')
    plot.plot(XSUB1, YSUB1, 'r-')
    plot.plot(XSUB2, YSUB2, 'r-')
    plot.plot(XSUB3, YSUB3, 'r-')

    # Create a canvas and add the plot to it
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # Pack the canvas into the root window
    canvas.get_tk_widget().pack()

    # Start the main loop
root.mainloop()
