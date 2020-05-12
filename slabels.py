#! python3
# septoria-labels.py

"""
@author: Slawomir Bartosiak
requirements:

tesseract-ocr-w64-setup-v5.0.0-alpha.20200223.exe
pip	19.2.3	20.0.2
opencv-python	4.2.0.32
numpy	1.18.1	1.18.2
pytesseract	0.3.3	0.3.3
imutils	0.5.3	0.5.3
"""

import cv2
import numpy as np
import os
import pytesseract
import imutils
import concurrent.futures

import time
t1 = time.perf_counter()

# Parameters
ang_input = 10  # Rotation angle range default 10 (-10 to 10).

binar_threshold = 57  # Binarization grayscale threshold default 35,
label_hue_min = 80  # min HUE, default 80
label_hue_max = 97  # max HUE, default 97

save_im_ready = False  # True/False save an image ready to read
save_im_binar = False  # True/False save an binarized image

tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Path to tesseract

# Tesseract run and config
pytesseract.pytesseract.tesseract_cmd = tesseract_path
custom_config = r'-c tessedit_char_whitelist=-0123456789 --psm 7'

# Directories
dir_old = os.getcwd()
os.makedirs('labels_output', exist_ok=True)
os.makedirs('input_images', exist_ok=True)
input_path = dir_old + '\\input_images\\'
output_path = dir_old + '\\labels_output\\'

# Read object list form text file
with open('object_list.txt') as f:
    object_list = f.readlines()
    object_list = [x.strip() for x in object_list]  # Append lines to list
    object_list = [string for string in object_list if string != ""]  # Remove empty strings from list

# Remove old files from labels_output
output_files = [f for f in os.listdir(output_path)
                if f.endswith('.jpg')
                or f.endswith('.JPG')
                or f.endswith('.PNG')
                or f.endswith('.JPEG')]
if not output_files:
    pass

else:
    yes = {'yes', 'y', 'ye', 'tak', '[y]'}
    no = {'no', 'n', 'nie', '[n]'}

    choice = input('Please enter [y] - yes or [n] - no, to delete/leave the output folder contents.\n').lower()
    while choice not in yes and choice not in no:
        choice = input('Please enter [y] - yes or [n] - no, to delete/leave the output folder contents.\n').lower()

    if choice in yes:
        for file in output_files:
            os.remove(output_path + file)
    elif choice in no:
        pass


# Angle function
def angle_func(max_range):
    v_list = [0]
    for x in range(1, max_range):
        v_list.append(x)
        v_list.append(~x)
    return v_list


# Slice an image
def slice_func(mask, image):
    im_mask = mask > 0
    im = np.zeros_like(image, np.uint8)
    im[im_mask] = image[im_mask]
    return im


# Convert red labels to blue
def output_image(im_read, im_gray, mask, contours):
    im_blue_out = im_read
    im_blue = cv2.cvtColor(im_read, cv2.COLOR_BGR2RGB)

    # Slice the blue label
    im_label_blue = slice_func(mask, im_blue)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)

    # Draw blue labels
    mask_gray = np.zeros_like(im_gray)
    cv2.drawContours(mask_gray, contours, max_index, 255, -1)  # Draw filled contour in mask

    # Add the label
    imask = mask_gray > 0
    im_blue_out[np.where(imask > 0)] = im_label_blue[np.where(imask > 0)]
    return im_blue_out


# Main function
def main(im_name):
    print("Analysing file: ", im_name)
    angles = angle_func(ang_input)
    counter = []

    # Load image
    im_read = cv2.imread(input_path + im_name)

    # If red label inverse colours to apply HUE ~
    im_read_inv = ~im_read

    # Color threshold
    hsv = cv2.cvtColor(im_read_inv, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (label_hue_min, 0, 0), (label_hue_max, 255, 255))  # label hue

    # Slice the label
    im = slice_func(mask, im_read)

    # Convert image to grayscale
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Find contours
    contours, _ = cv2.findContours(im_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Create image with changed red label to blue
    im_blue_label = output_image(im_read, im_gray, mask, contours)

    # Find the biggest contour (c) by the area
    c = max(contours, key=cv2.contourArea)
    xmin, ymin, w, h = cv2.boundingRect(c)
    xmax = xmin + w
    ymax = ymin + h
    im_cropped = im_gray[ymin:ymax, xmin:xmax]

    # Binarize
    _, binar = cv2.threshold(im_cropped, binar_threshold, 255, cv2.THRESH_BINARY)
    if save_im_binar is True:
        cv2.imwrite(output_path + im_name, binar)  # Save an binarized image

    # Rotate image
    for angle in angles:
        rotated = imutils.rotate_bound(binar, angle)

        # Recognize label text
        text = pytesseract.image_to_string(rotated, config=custom_config)
        counter.append(angle)  # Loop counter

        # Check if text is in object_list
        if text in object_list:
            if save_im_ready is True:
                cv2.imwrite(output_path + text + 'ang_' + str(angle) + '.jpg', rotated)  # Save an image ready to read

            # Check if file already exist
            if_exist = os.path.isfile(output_path + text + '.jpg')
            if if_exist is True:
                # Save file with prefix CHECK_NAME if file exist to prevent override file
                cv2.imwrite(output_path + 'CHECK_NAME_' + text + '.jpg', im_blue_label)
            else:
                # Save an image named as recognized text from label
                cv2.imwrite(output_path + text + '.jpg', im_blue_label)
                print("File %s saved as %s.jpg" % (im_name, text))
            break
    # Save an unrecognized image
    if len(counter) == len(angles):
        cv2.imwrite(output_path + 'UNRECOGNIZED_' + im_name, im_blue_label)
    return


def img_show(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Multiprocessing:
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files_jpg = [f for f in os.listdir(input_path)
                     if f.endswith('.jpg')
                     or f.endswith('.JPG')
                     or f.endswith('.PNG')
                     or f.endswith('.JPEG')]
        executor.map(main, files_jpg)

    # Timer
    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
