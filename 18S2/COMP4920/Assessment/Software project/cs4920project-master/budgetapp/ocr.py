from PIL import Image
import pytesseract
import cv2
import os
import re
import numpy as np
import imutils
from skimage.filters import threshold_local

'''
Given a list of points, try to order them in a 4x2 array
where for each corner, going from top left in a clockwise direction
first, second, third and fourth point
'''
def order_points(pts):
    ordered = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    # top left point has the least sum
    ordered[0] = pts[np.argmin(s)]
    # bottom right point has the most sum
    ordered[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    # top right point has the least difference
    ordered[1] = pts[np.argmin(diff)]
    # bottom left point has the most difference
    ordered[3] = pts[np.argmax(diff)]

    return ordered


'''
given the four points coordinates, transform the given image to fit said coordinates
returns a warped image with said coordinates
'''
def four_point_transform(image, pts):
    ordered = order_points(pts)
    (tl, tr, br, bl) = ordered

    # compute width of new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute height of new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # for new image array
    new_image = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # transform the perspective
    M = cv2.getPerspectiveTransform(ordered, new_image)

    # warp the perspective
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


'''
perspective-correct the input image and produce a B&W image
'''
def scan_image(path_to_image):
	# load image
    image = cv2.imread(path_to_image)

    # get ratio
    ratio = image.shape[0] / 500.0

    # copy original image
    orig = image.copy()

    # resize the image to heigh 500 for easier manipulation
    image = imutils.resize(image, height = 500)

    # convert to gray colour
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply gaussian blur
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # apply canny edge detection
    edged = cv2.Canny(gray, 75, 200)

    # find contours from the edged image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # grab the necessary contours
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
 
 	# loop through every contour
    for c in cnts:
    	# find 4 controus
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    # correct the perspective for the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # convert warped image to gray
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    # apply threshold local filter using gaussian method
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")

    # stretch the colours back from 0-1 to 0-255
    warped = (warped > T).astype("uint8") * 255

    # write image
    cv2.imwrite("warped.jpg", warped)


'''
apply ocr to an image
preprocess with thresholding to segment image
'''
def run_ocr(path_to_image, preprocess=True):
	# read image
    image = cv2.imread(path_to_image)

    # convert to gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply preprocessing
    if preprocess:
        print("preprocessing")
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # save the threshold image temporarily
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # apply tesseract ocr
    text = pytesseract.image_to_string(Image.open(filename))

    # delete temporary image
    os.remove(filename)

    return(text)

'''
kinda dumb, bruteforce-y way to find the sum from a wall of text
using regex
'''
def find_most_likely_sum(text):
	# try to find the word "total"
    matched_total = re.search(r'.*(total).*\$(\d+\[ ]*.[ ]*\d*).*',text,re.IGNORECASE)

    # if found something
    if matched_total is not None:
    	# remove empty spaces between dollar and cents due to ocr
        number = matched_total.group(2).replace(" ","")
        return number
    else:
        # total normally includes a $ at the front
        matched_dollar_sign = re.findall(r'.*\$(\d+[ ]*.[ ]*\d*).*', text, re.IGNORECASE)
        # if found something
        if matched_dollar_sign is not None:
        	# remove empty spaces between dollar and cents due to ocr
            return (max(matched_dollar_sign).replace(" ",""))
        else:
            # go hailmary and just pick the biggest number in the entire script
            matched_numbers = re.findall(r'.*(\d+[ ]*.[ ]*\d{1,2}).*', text, re.IGNORECASE)
            # if found something
            if matched_numbers is not None:
                print(matched_numbers)
                # remove empty spaces between dollar and cents due to ocr
                return (max(matched_numbers).replace(" ",""))
            else:
            	# i give up
                error_message = "Couldn't find the amount, please input manually"
                return error_message


'''
run through the entire process to attempt to find the number
'''
def ocr_execute(path_to_image):
    try: 
    	# try to apply perspective correction
        scan_image(path_to_image)
        # run ocr
        to_return = find_most_likely_sum(run_ocr("warped.jpg"))
        # os.remove("warped.jpg")
        return to_return
    except:
    	# if there is an error (normally because it can't find 4 edges of the receipt), run the ocr 
    	# without applying transformation
        print("ERROR, skipping transformation preprocess")
        return(find_most_likely_sum(run_ocr(path_to_image)))


if __name__ == '__main__':
    print(ocr_execute("sample_receipts/receipt5.jpg"))