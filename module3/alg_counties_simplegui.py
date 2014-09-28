"""
Visualizer for county-based cancer data - Data is collated from two sources

Overall lifetime cancer risk from air toxics
http://www.epa.gov/ttn/atw/nata2005/tables.html
T
Geographic county locations are computed from and relative to this image
http://commons.wikimedia.org/wiki/File:USA_Counties_with_FIPS_and_names.svg
"""

import math
import urllib2
import simplegui


# Constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 634

# Assets
DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"


def risk_color(risk):
    """
    Compute color associated with risk
    """
    magnitude = int(720 * (-math.log(risk, 10) - 4.3))
    magnitude = max(min(magnitude, 255), 0)
    color = "hsl(" + str(magnitude) + ",100%,50%)"
    return color


def circle_radius(pop):
    """
    Compute radius of circle whose area is proportional to population
    """
    return math.sqrt(pop) / 200


class PlotCountyData:
    """
    Interactive frame to visualize cancer data
    """

    def __init__(self):
        """
        Create a frame and load the cancer data
        """
        self._frame = simplegui.create_frame("Cancer risk visualization", CANVAS_WIDTH, CANVAS_HEIGHT)
        self._frame.set_canvas_background("White")
        self._frame.set_draw_handler(self.draw)
        self._frame.add_input("Enter cutoff (scaled by 0.00001)", self.enter_cutoff, 200)
        self._frame.add_button("Print data table in CSV", self.print_table, 200)
        self._data_table = self.load_data()
        self.enter_cutoff("0.0")
        self._USA_Counties = simplegui.load_image(MAP_URL)
        self._frame.start()

    def print_table(self):
        """
        Print all data points with risk above cutoff * 10^(-5)
        in CSV format
        """
        for line in self._current_table:
            print line[0] + ", " + str(line[1]) + ", " + \
                str(line[2]) + ", " + str(line[3]) + ", " + \
                str(line[4])

    def enter_cutoff(self, cutoff):
        """
        Select all data points with risk above cutoff * 10^(-5)
        """
        self._current_table = []
        for line in self._data_table:
            if line[4] > 0.00001 * float(cutoff):
                self._current_table.append(line)
        print "Displayed", len(self._current_table), "data points using cutoff", cutoff

    def load_data(self):
        """
        Load cancer risk data from .csv file
        """
        data_file = urllib2.urlopen(DATA_3108_URL)
        data = data_file.read()
        data_lines = data.split('\n')
        print "Loaded", len(data_lines), "data points"
        data_tokens = [line.split(',') for line in data_lines]
        return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] for tokens in data_tokens]

    def draw(self, canvas):
        """
        Draw handler for data visualizer
        """
        canvas.draw_image(self._USA_Counties, [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [CANVAS_WIDTH, CANVAS_HEIGHT],
                                              [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [CANVAS_WIDTH, CANVAS_HEIGHT])

        for line in self._current_table:
            color = risk_color(line[4])
            canvas.draw_circle([line[1], line[2]], circle_radius(line[3]), 1, color, color)


# create and start the application
PlotCountyData()
