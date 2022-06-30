from image import Image
import numpy as np
from PIL import Image as imge

def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!

    # # this is the non vectorized version
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor

    # faster version that leverages numpy
    new_im.array = image.array * factor

    return new_im

def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid

    return new_im

def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    neighbor_range = kernel_size // 2  # this is a variable that tells us how many neighbors we actually look at (ie for a kernel of 3, this value should be 1)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # we are going to use a naive implementation of iterating through each neighbor and summing
                # there are faster implementations where you can use memoization, but this is the most straightforward for a beginner to understand
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        total += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2)
    return new_im

def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    neighbor_range = kernel.shape[0] // 2  # this is a variable that tells us how many neighbors we actually look at (ie for a 3x3 kernel, this value should be 1)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_im.array[x, y, c] = total
    return new_im

def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c]**2 + image2.array[x, y, c]**2)**0.5
    return new_im
    
if __name__ == '__main__':
    check = 'Y'
    print("\n\t\t\t***PYPHoToSHoP***\n\n")

    while check == 'Y' or check == 'y':
        
        imagefile = input("Enter file name of image to be edited : ")
        img = Image(filename=imagefile)
        imgpil = imge.open('input/' + imagefile)
        imgpil.show()

        check2 = 'Y'
        while check2 == 'Y' or check2 == 'y':
            print("\n1. BRIGHTEN \n2. DARKEN \n3. INCREASE CONTRAST \n4. DECREASE CONTRAST \n5. BLUR \n6. X AXIS EDGE DETECTION \n7. Y AXIS EDGE DETECTION \n8. EDGE DETECTION\n")
            option = int(input("Select option: "))

            if option == 1:
                    brightened_im = brighten(img, 1.7)
                    brightened_im.write_image('output.png')
                    
            
            if option == 2:
                darkened_im = brighten(img, 0.3)
                darkened_im.write_image('output.png')
            
            if option == 3:
                incr_contrast = adjust_contrast(img, 2, 0.5)
                incr_contrast.write_image('output.png')

            if option == 4:
                decr_contrast = adjust_contrast(img, 0.5, 0.5)
                decr_contrast.write_image('output.png')
            
            if option == 5:
                # blur using kernel size of 15
                blur_15 = blur(img, 10)
                blur_15.write_image('output.png')
            
            if option == 6:
                # let's apply a sobel edge detection kernel on the x and y axis
                sobel_x = apply_kernel(img, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
                sobel_x.write_image('output.png')

            if option == 7:
                sobel_y = apply_kernel(img, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
                sobel_y.write_image('output.png')
            
            if option == 8:
                # let's combine these and make an edge detector!
                sobel_x = apply_kernel(img, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
                sobel_y = apply_kernel(img, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
                sobel_xy = combine_images(sobel_x, sobel_y)
                sobel_xy.write_image('output.png')
    
            imgpil = imge.open('output/output.png')
            imgpil.show()
            
            check2 = input("Do you want to continue editing this image?(Y/n)")
        check = input("Do you want to edit any other image?(Y/n)")

