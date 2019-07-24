import clr
import datetime
import numpy as np
import time


clr.AddReference("OpenCV.Net")
from OpenCV.Net import *

trajectory = None
histogram = None
current_time = None


# gets coordinates and updates histogra array
def update_histogram(hist, time_of_last_visit, x, y, bin_ranges_x, bin_ranges_y):
    now = time.time()

    bin_index_x = np.digitize(x, bin_ranges_x)
    bin_index_y = np.digitize(y, bin_ranges_y)
    # check what's in time bin
    time_bin = time_of_last_visit[bin_index_x, bin_index_y]
    # if it's been long enough
    if time_bin - now > 5:
        if hist[bin_index_x, bin_index_y] < 2:
            hist[bin_index_x, bin_index_y] += 1
        time_of_last_visit[bin_index_x, bin_index_y] = datetime.datetime.now()  # todo check if this should always update regardless up time

    return hist, time_of_last_visit


def get_histogram_state(current_x, current_y, x_max, y_max, x_min, y_min, number_of_bins_x=20, number_of_bins_y=20):
    global histogram
    global time
    if histogram is None:
        histogram = np.zeros((number_of_bins_x, number_of_bins_y))
    if time is None:
        time = np.zeros((number_of_bins_x, number_of_bins_y))
    bin_ranges_x = np.arange(x_min, x_max, (x_max - x_min)/number_of_bins_x)
    bin_ranges_y = np.arange(y_min, y_max, (y_max - y_min) / number_of_bins_y)
    histogram, time = update_histogram(histogram, time, current_x, current_y, bin_ranges_x, bin_ranges_y)


@returns(IplImage)
def process(value):
    global trajectory
    red = value.Item1
    green = value.Item2
    image = value.Item3

    if trajectory is None:
        trajectory = IplImage(image.Size, image.Depth, 3)
        trajectory.SetZero()

    if red.Area > 0:
        CV.Circle(trajectory, Point(red.Centroid), 4, Scalar.Rgb(0, 125, 125), -1)
    if green.Area > 0:
        CV.Circle(trajectory, Point(green.Centroid), 4, Scalar.Rgb(125, 0, 125), -1)

    output = image.Clone()
    mask = IplImage(image.Size, image.Depth, 1)
    CV.CvtColor(trajectory, mask, ColorConversion.Bgr2Gray)
    CV.Threshold(mask, mask, 0, 255, ThresholdTypes.Binary)
    CV.Copy(trajectory, output, mask)
    if red.Area > 0:
        CV.Circle(output, Point(red.Centroid), 4, Scalar.Rgb(0, 255, 255), -1)
    if green.Area > 0:
        CV.Circle(output, Point(green.Centroid), 4, Scalar.Rgb(255, 0, 255), -1)

    return output



if __name__ == '__main__':

    process(value)