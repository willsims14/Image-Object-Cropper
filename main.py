import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import urllib
import cv2
# from PIL import Image


from skimage import measure, color, io, transform
import sys

def main():
    ##############
    ###  PNGs  ###
    ##############
    png_denali = io.imread('images/pngs/2_Denali-01.png', as_grey=False)
    png_aptiv = io.imread('images/pngs/3_Aptiv-01.png', as_grey=False)
    png_believeland = io.imread('images/pngs/4_Believeland-01.png', as_grey=False)
    png_me = io.imread('images/pngs/5_Me-01.png', as_grey=False)
    png_berkshire = io.imread('images/pngs/6_Berkshire_2c-01.png', as_grey=False)

    # Change CURRENT_IMAGE variable to load and crop a different image
    CURRENT_IMAGE = png_believeland
    DPI = 300.0

    pixels_that_have_color = get_all_non_transparent_pixels(CURRENT_IMAGE)
    vertical_min, vertical_max, horizontal_min, horizontal_max = get_vertical_and_horizontal_mins_and_max(CURRENT_IMAGE, used_pixels=pixels_that_have_color)
    show_original_and_cropped_jpeg(CURRENT_IMAGE, DPI, vertical_max, vertical_min, horizontal_max=horizontal_max, horizontal_min=horizontal_min, is_jpeg=False)




def silence_all_axis_ticks(plt):
    plt.tick_params(
        axis='x',
        which='both',
        bottom='off',
        top='off',
        labelbottom='off',)

    plt.tick_params(
        axis='y',
        which='both',
        left='off',
        bottom='off',
        labelleft='off',)
    return plt


# Displays the image next to an image of the cropped object
def show_original_and_cropped_jpeg(original, dpi, vertical_max, vertical_min, horizontal_max, horizontal_min, is_jpeg=False):
    fig = plt.figure("Compare")

    ##############################
    ### Original Image Subplot ###
    ##############################
    ax = fig.add_subplot(1, 2, 1)
    # ax.patch.set_facecolor('grey') # Uncomment this line to change the background color of plot to gray
    ax.set_title("Original")
    ax.set_ylabel("{} inches".format(original.shape[0] / dpi))
    ax.set_xlabel("{} inches".format(original.shape[1] / dpi))
    ax.axhline(vertical_max)
    ax.axhline(vertical_min)
    ax.axvline(horizontal_min)
    ax.axvline(horizontal_max)
    silence_all_axis_ticks(plt)
    plt.imshow(original)

    #############################
    ### Cropped Image Subplot ###
    #############################
    cropped_image = original[vertical_min: vertical_max, horizontal_min: horizontal_max]
    ax = fig.add_subplot(1, 2, 2)
    # ax.patch.set_facecolor('grey') # Uncomment this line to change the background color of plot to gray
    ax.set_title("Cropped")
    ax.set_ylabel("{} inches ".format(round(float(cropped_image.shape[0] / dpi), 4)))
    ax.set_xlabel("{} inches ".format(round(float(cropped_image.shape[1] / dpi), 4)))
    silence_all_axis_ticks(plt)
    plt.imshow(cropped_image)

    original_area_dimensions_text = 'Original Size: {}w x {}h'.format(str(original.shape[0] / float(dpi)), str(original.shape[1] / float(dpi)))
    area_used_dimensions_text = 'Cropped Size: {}w x {}h'.format(str(round(cropped_image.shape[0] / float(dpi), 4)), str(round(cropped_image.shape[1] / float(dpi), 4)))
    plt.suptitle('PNG Images\n\n{}\n{}'.format(original_area_dimensions_text, area_used_dimensions_text))

    # Show Plot
    plt.show()

# Returns the first, the last, the leftmost, and the rightmost pixel coordinates for pixels that are NOT transparent
def get_vertical_and_horizontal_mins_and_max(image, used_pixels):
    ############################
    ###  Vertical Min / Max  ###
    ############################
    first_vertical_non_white_pixel = used_pixels[:,0]
    last_vertical_non_white_pixel = used_pixels[:, -1]

    vertical_min = first_vertical_non_white_pixel[0]
    vertical_max = last_vertical_non_white_pixel[0]

    # Rotate the image
    rotated_image = np.array(transform.rotate(image, 90, resize=0, preserve_range=True), dtype=np.uint8)

    ##############################
    ###  Horizontal Min / Max  ###
    ##############################
    horizontal_pixels_that_are_not_white = get_all_non_transparent_pixels(rotated_image)

    first_horizontal_non_white_pixel = horizontal_pixels_that_are_not_white[:, 0]
    last_horizontal_non_white_pixel = horizontal_pixels_that_are_not_white[:, -1]

    horizontal_max = first_horizontal_non_white_pixel[0]
    horizontal_min = last_horizontal_non_white_pixel[0]
    print "\n Minimums / Maxiumums"
    print "  * Horizontal Minimum:  X = {}".format(horizontal_min)
    print "  * Horizontal Maximum:  X = {}".format(horizontal_max)
    print "  * Vertical Minimum:    Y = {}".format(vertical_min)
    print "  * Vertical Maximum:    Y = {}".format(vertical_max)

    return vertical_min, vertical_max, (1500 - horizontal_min), (1500 - horizontal_max)


# Returns array of coordinates to pixels that are transparent or white
#   (pixels that are not a part of the object being cropped)
def get_all_non_transparent_pixels(png_image):
    good_vals = [255, 255, 255, 0]
    good_vals_2 = [254, 254, 254, 0]
    return np.array(np.where( (png_image != good_vals) & (png_image != good_vals_2) ))


if __name__=="__main__":
    main()
