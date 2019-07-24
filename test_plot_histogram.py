import numpy as np
import plot_histogram


def test_update_histogram():
    number_of_bins_x = 20
    number_of_bins_y = 20
    histogram = np.zeros((number_of_bins_x, number_of_bins_y))
    times = np.zeros((number_of_bins_x, number_of_bins_y))
    current_x = 0.5
    current_y = 0.9
    x_min = 0.1
    y_min = 0.2
    x_max = 101
    y_max = 104
    number_of_bins_x = 20
    number_of_bins_y = 20
    bin_ranges_x = np.arange(x_min, x_max, (x_max - x_min)/number_of_bins_x)
    bin_ranges_y = np.arange(y_min, y_max, (y_max - y_min) / number_of_bins_y)

    histogram, times = plot_histogram.update_histogram(histogram, times, current_x, current_y, bin_ranges_x, bin_ranges_y)
    
    histogram_expected = histogram
    histogram_expected[0, 0] = 1

    assert np.allclose(histogram, histogram_expected, rtol=1e-05, atol=1e-08)
    # assert np.allclose(times, times_expected, rtol=1e-05, atol=1e-08)


def main():
    test_update_histogram()


if __name__ == '__main__':
    main()

