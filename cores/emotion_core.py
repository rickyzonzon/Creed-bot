# Emotion core

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import operator


class Emotion:

    def __init__(self, j, sad, t, d, f, ang, sup, ant):
        self.emotions = {"joy": j,
                         "sadness": sad,
                         "trust": t,
                         "disgust": d,
                         "fear": f,
                         "anger": ang,
                         "surprise": sup,
                         "anticipation": ant}
        self.feelings = [j, sad, t, d, f, ang, sup, ant]

        self.theta = radar_factory(8, frame='polygon')
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection='radar'))
        self.spoke_labels = ['Joy', 'Anticipation', 'Anger', 'Disgust',
                             'Sadness', 'Surprise', 'Fear', 'Trust']
        self.data = [[[0, 0, 0, 0, 0, 0, 0, 0]]]
        for d, in self.data:
            lines = self.ax.plot(self.theta, d, color='b')
            filling = self.ax.fill(self.theta, d, facecolor='b', alpha=0.45)

        self.ani = None

    def change(self, emotion, num):
        if self.emotions[emotion] < 2:
            self.emotions[emotion] += num
        elif self.emotions[emotion] >= 2 and num < 0:
            self.emotions[emotion] += num

    def generator(self):
        while True:

            if self.emotions["joy"] >= 0.25:
                self.change("joy", -0.005 * self.emotions["joy"])
            else:
                self.emotions["joy"] = 0.25

            if self.emotions["sadness"] >= 0.25:
                self.change("sadness", -0.005 * self.emotions["sadness"])
            else:
                self.emotions["sadness"] = 0.25

            if self.emotions["trust"] >= 0.25:
                self.change("trust", -0.005 * self.emotions["trust"])
            else:
                self.emotions["trust"] = 0.25

            if self.emotions["disgust"] >= 0.25:
                self.change("disgust", -0.005 * self.emotions["disgust"])
            else:
                self.emotions["disgust"] = 0.25

            if self.emotions["fear"] >= 0.25:
                self.change("fear", -0.005 * self.emotions["fear"])
            else:
                self.emotions["fear"] = 0.25

            if self.emotions["anger"] >= 0.25:
                self.change("anger", -0.005 * self.emotions["anger"])
            else:
                self.emotions["anger"] = 0.25

            if self.emotions["surprise"] >= 0.25:
                self.change("surprise", -0.005 * self.emotions["surprise"])
            else:
                self.emotions["surprise"] = 0.25

            if self.emotions["anticipation"] >= 0.25:
                self.change("anticipation", -0.005 * self.emotions["anticipation"])
            else:
                self.emotions["anticipation"] = 0.25

            self.feelings = [self.emotions["joy"], self.emotions["anticipation"], self.emotions["anger"],
                             self.emotions["disgust"], self.emotions["sadness"], self.emotions["surprise"],
                             self.emotions["fear"], self.emotions["trust"]]

            yield self.feelings

    # any emotes above a certain level, add to strongest
    # output list of words describing the feeling
    def status(self):
        maxnum = max(self.emotions.items(), key=operator.itemgetter(1))[1]
        strongest = [s for s in self.emotions if maxnum == self.emotions[s]]

        if len(strongest) == 1:
            if strongest == 'joy':
                return ["happy", "cheerful", "joyful", "delighted"]
            elif strongest == 'sadness':
                return ["unhappy", "sad", "depressed", "gloomy", "down"]
            elif strongest == 'trust':
                return ["trusting", "unsuspecting", "wide-eyed"]
            elif strongest == 'disgust':
                return ["disgusted", "revolted", "sickened", "yucky"]
            elif strongest == 'fear':
                return ["scared", "afraid", "frightened", "nervous", "worried"]
            elif strongest == 'anger':
                return ["angry", "mad", "upset", "annoyed", "irritated"]
            elif strongest == 'surprise':
                return ["surprised", "astonished", "startled", "shocked"]
            elif strongest == 'anticipation':
                return ["expecting", "hopeful", "anticipative"]
        else:
            return ["not implemented"]

    def initialize(self):
        self.ax.set_varlabels(self.spoke_labels)
        self.ax.set_rgrids([])
        self.ax.set_rlim(0, 2)
        self.ax.set_facecolor((240 / 255, 240 / 255, 237 / 255))
        self.fig.text(0.5, 0.965, 'Creed', horizontalalignment='center', color='black', weight='bold', size='large')
        self.fig.patch.set_facecolor((240 / 255, 240 / 255, 237 / 255))

    def update(self, frame):
        self.data = [[frame]]
        for d, in self.data:
            lines = self.ax.set_radar_data(self.theta, d, color='b')
            filling = self.ax.set_fill_data(self.theta, d, facecolor='b', alpha=0.45)


def radar_factory(num_vars, frame='circle'):
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            self.fills = super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            self.lines = super().plot(*args, **kwargs)
            for line in self.lines:
                self._close_line(line)

        def set_radar_data(self, data, *args, **kwargs):
            new_lines = super().plot(data, *args, **kwargs)
            self.lines = new_lines
            for line in self.lines:
                self._close_line(line)

        def get_radar_data(self):
            return self.lines

        def set_fill_data(self, data, *args, closed=True, **kwargs):
            self.fills[0].set_visible(False)
            new_fill = super().fill(data, closed=closed, *args, **kwargs)
            self.fills = new_fill

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars, radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self, spine_type='circle', path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta
