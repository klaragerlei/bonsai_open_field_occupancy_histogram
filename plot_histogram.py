# import clr
import matplotlib.pylab as plt
import numpy as np
import time


# clr.AddReference("OpenCV.Net")
# from OpenCV.Net import *

trajectory = None
histogram = None
times_of_last_visits = None


# gets coordinates and updates histogra array
def update_histogram(hist, time_of_last_visits, x, y, bin_ranges_x, bin_ranges_y):
    now = time.time()

    bin_index_x = np.digitize(x, bin_ranges_x)
    bin_index_y = np.digitize(y, bin_ranges_y)
    # check what's in time bin
    time_bin = time_of_last_visits[bin_index_x, bin_index_y]
    # if it's been long enough
    if now - time_bin > 5:
        if hist[bin_index_x, bin_index_y] < 2:
            hist[bin_index_x, bin_index_y] += 1
        # todo check if this should always update regardless up time
        time_of_last_visits[bin_index_x, bin_index_y] = time.time()

    return hist, time_of_last_visits


def get_histogram_state(current_x, current_y, x_max, y_max, x_min, y_min, number_of_bins_x=20, number_of_bins_y=20):
    global histogram
    global times_of_last_visits
    if histogram is None:
        histogram = np.zeros((number_of_bins_x, number_of_bins_y))
    if times_of_last_visits is None:
        times_of_last_visits = np.full((number_of_bins_x, number_of_bins_y), time.time())
    bin_ranges_x = np.arange(x_min, x_max, (x_max - x_min)/number_of_bins_x)
    bin_ranges_y = np.arange(y_min, y_max, (y_max - y_min) / number_of_bins_y)
    histogram, times_of_last_visits = update_histogram(histogram, times_of_last_visits, current_x, current_y, bin_ranges_x, bin_ranges_y)
    # print(histogram)
    # plt.imshow(histogram)


'''
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
'''


def main():
    get_histogram_state(10, 2, 100, 100, 0, 0, number_of_bins_x=20, number_of_bins_y=20)


if __name__ == '__main__':
    main()

