**Septoria-leaf**

Septoria-leaf is a free open source software for measuring the disease
percentage of leaves infected by *Parastagonospora nodorum* or
*Zymoseptoria tritici* in a computationally efficient manner. Software
automate labels reading from digital images and facilitates septoria
disease severity examination. Program analyses digital images, examines
the leaves on an image sample (each leaf individually) and summarizes
results in the table. Software creates also a pivot table of total leaf
area and disease area as pixel sums and average disease percentage of
each image sample.

**Getting Started**

**Requirements:**

Windows 10:

Python 3.8.2 with following modules installed:\
opencv-python 4.2.0.32

imutils 0.5.3\
numpy 1.18.2\
pandas 1.0.3 modules

pytesseract 0.3.3

tesseract v5.0.0 - <https://github.com/UB-Mannheim/tesseract/wiki>,
install tesseract, use default path: C:\\Program
Files\\Tesseract-OCR\\tesseract.exe.

**Installing:**

Download septoria-leaf.zip and unzip the folder. Make sure that program
path is encoded in Latin-1 (ISO-8859-1).

**Definitions:**

**Image sample** is a digital image of wheat or triticale leaves in a
seedling growth stage.

**sample\_name** is a text read from label. Code name of image sample.

**leaf\_area** is a total area in pixels of one extracted leaf from an
image sample.

**disease\_area** is a total diseased area in pixels of leaf extracted
from an image sample.

**disease\_percetage** is a ratio of disease\_area to leaf\_area \*100.

**Preparation of image samples:**

Leaves in an image sample should be in one piece, using fragmented
leaves is not advised because the program will interpret them as a whole
leaf. Leaves should not touch each other, otherwise software will
interpret them as a single leaf. The suggested colour of background is
blue in order to easily extract leaves from image samples. Image sample
labels by default should be rectangular approximately 5 cm in width and
1 cm in height with black characters description on a red background.

**Run the program:**

slabels.py -- is a small software assisting with the laborious and time
consuming image file naming task. The program extracts a text from
labels in an image and renames each file. Depending on various factors
an image colour reproduction can differ, therefore for optimization of
the parameters follow the steps:

1.  Prepare a list of labels to read in *object\_list.txt* file located
    in the main directory - *septoria-leaf*. Each row should contain a
    single label name formatted in d-d-d manner, where d is a number. By
    default slabels.py use following whitelist characters: -0123456789.

1-1-1

1-1-2

1-2-1

...

2.  Place prepared images in the directory - *input\_images*. Make sure
    that object samples are not duplicated.

3.  Adjust the *label\_hue\_min*, *label\_hue\_max* and
    *binary\_threshold* in the slabels.py file. The HUE parameter is
    used for slicing the red label contour while the *binar\_threshold*
    is a grayscale threshold for extraction of label characters.

binar\_threshold = 57 \# Binarization grayscale threshold default 57

label\_hue\_min = 80 \# min HUE, default 80\
label\_hue\_max = 97 \# max HUE, default 97

4.  Enable writing of sliced and binarized images in order to check if
    thresholding parameters were optimised successfully. Sliced and
    binarized images will be located in the *lables\_output* directory.

save\_im\_ready = True \# True/False save an image ready to read\
save\_im\_binar = True \# True/False save an binarized image

5.  The label orientation in an image can differ from -10 to 10 degrees
    by default. To manually apply rotation degrees edit maximum rotation
    angle in *ang\_input*.

ang\_input = 10 \# Rotation angle range default 10 (-10 to 10).

6.  Run the slabels.py program.

7.  Output images will be located in the *labels\_output* directory.
    Unrecognized images will be named as UNRECOGNIZED\_\<img\_name\>. If
    a read file name is doubled or a file label will not match any
    object in the object\_list.txt, the image will be saved as
    CHECK\_NAME\_\<label\_name\>.jpg. If settings were optimized user
    have to manually correct file names.

sleaves.py -- the software evaluates diseased area percentage and
summarises results in tables. To run the program and optimize the
parameters follow the protocol:

1.  The Sleaves.py program analyses files from the *labels\_output*
    folder.

2.  To enable extracted leaves and diseased tissue write, set the
    *save\_leaf\_im* and *save\_diseased\_im* variables to True. Files
    will be located in the *output* folder.

save\_leaf\_im = True \# True/False save an extracted leaf image

save\_diseased\_im = True \# True/False save an diseased image

3.  To calibrate the leaf HUE parameter *leaf\_hue\_min* and
    *leaf\_hue\_max* values can be modified:

leaf\_hue\_min = 0 \# Min leaf HUE, default 0\
leaf\_hue\_max = 90 \# Max leaf HUE, default 90

4.  To calibrate the diseased tissue HUE parameter, the
    *diseased\_hue\_min* and *diseased\_hue\_max* values can be
    modified:

diseased\_hue\_min = 0 \# Min diseased HUE, default 0\
diseased\_hue\_max = 45 \# Max diseased HUE, default 45

5.  Run the sleaves.py program.

6.  After the program completes analysis output files in \*.csv format
    will be created in the main folder *septoria-leaf*. The results.csv
    file will contain all leaves results summary (sample leaf\_area,
    disease\_area and disease\_percentage). The pivot\_table.csv file is
    table summary of a results table grouped by sample name. The
    pivot\_table.csv contain leaf\_area and disease\_area aggregated by
    sum for each object name and average of a disease\_percentage.


**Acknowledgments**

Stack Overflow community.

Authors
-------
Sławomir Bartosiak
