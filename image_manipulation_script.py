import matplotlib.pyplot as plt
from PIL import Image
from osgeo import gdal
import numpy as np 
import cv2

#step 1: 
#takes an array for color bounds, String representing color name
def color_mask(bounds_array, color):
    img = cv2.imread('location_rich_image.tif', cv2.IMREAD_UNCHANGED)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if len(bounds_array) == 2: 
        color_bounds_low = bounds_array[0] 
        color_bounds_high = bounds_array[1]

        low = np.array(color_bounds_low)
        high = np.array(color_bounds_high)
        mask = cv2.inRange(hsv, low, high)
        result_image = cv2.bitwise_and(img, img, mask=mask)
        cv2.imwrite("masks/"+color+"_mask.tif", result_image)

        return result_image

    if len(bounds_array) == 4: 
        color_bounds_low_1 = bounds_array[0] 
        color_bounds_high_1 = bounds_array[1]
        color_bounds_low_2 = bounds_array[2] 
        color_bounds_high_2 = bounds_array[3]

        low_1 = np.array(color_bounds_low_1)
        high_1 = np.array(color_bounds_high_1)
        low_2 = np.array(color_bounds_low_2)
        high_2 = np.array(color_bounds_high_2)
        mask_1 = cv2.inRange(hsv, low_1, high_1)
        mask_2 = cv2.inRange(hsv, low_2, high_2)
        result_image = cv2.bitwise_and(img, img, mask=mask_1+mask_2)
        cv2.imwrite("masks/"+color+"_mask.tif", result_image)
        
        # plt.imshow(result_image)
        # plt.show()  
        return result_image

#step 2: 
#take mask, and find contours (border) around the polygons
def create_contours(img, color, bgr_color):
    # grayscale and average filter to smooth image 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((15,15),np.float32)/25
    gray = cv2.filter2D(gray,-1,kernel)

    #detect contours 
    ret, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_OTSU)
    #find the contours in the image
    contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #draw the obtained contour lines (or the set of coordinates forming a line) on the original image

    
    #creates all black image --> changes it to have white pixels equal color of choice 
    threshold_shape = thresh.shape
    color_img = np.zeros((threshold_shape[0], threshold_shape[1], 3), dtype = np.uint8)
    color_img[np.where(thresh == 255)] = bgr_color
    
    # thresh = cv2.drawContours(color_img, contours, -1, (255,0,0), 10)
    cv2.imwrite("masks/"+color+"_mask.tif", color_img)    

#step 3: 
#converts all black pixels to transparent
def make_image_transparent(color):
    img = Image.open("masks/"+color+"_mask.tif")
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)

    # Save the modified image
    img.save("masks/"+color+"_mask.tif") 

# blue 
blue_bounds = ([60, 50, 100], [100, 255, 255])
blue_mask_image = color_mask(blue_bounds, "blue")
create_contours(blue_mask_image, "blue", (141, 124, 28))
make_image_transparent("blue")


#green 
green_bounds = ([25, 30, 98], [80, 255, 255])
green_mask_image = color_mask(green_bounds, "green")
create_contours(green_mask_image, "green", (38, 95, 92))
make_image_transparent("green")

#purple
purple_bounds = ([100, 41, 98], [170, 250, 255])
purple_mask_image = color_mask(purple_bounds, "purple")
create_contours(purple_mask_image, "purple", (77, 34, 82))
make_image_transparent("purple")

#red 
red_bounds = ([0, 50, 50], [12, 255, 255], [160, 70, 50], [180, 255, 255])
red_mask_image = color_mask(red_bounds, "red")
create_contours(red_mask_image, "red", (46, 52, 201))
make_image_transparent("red")

#orange 
orange_bounds = ([5, 100, 100], [22, 255, 255])
orange_mask_image = color_mask(orange_bounds, "orange")
create_contours(orange_mask_image, "orange", (39, 117, 194))
make_image_transparent("orange")


