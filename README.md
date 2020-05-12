Septoria-leaf 
Septoria-leaf is a free open source software for measuring the disease percentage of leaves infected by Parastagonospora nodorum or Zymoseptoria tritici in a computationally efficient manner. Software automate labels reading from digital images and facilitates septoria disease severity examination. Program analyses digital images, examines the leaves on an image sample (each leaf individually) and summarizes results in the table. Software creates also a pivot table of total leaf area and disease area as pixel sums and average disease percentage of each image sample.   

Getting Started
Requirements:
Windows 10: 
Python 3.8.2 with following modules installed:
opencv-python 4.2.0.32
imutils 0.5.3
numpy 1.18.2
pandas 1.0.3 modules
pytesseract 0.3.3
tesseract v5.0.0 - https://github.com/UB-Mannheim/tesseract/wiki, install tesseract, use default path: C:\Program Files\Tesseract-OCR\tesseract.exe. 

Installing:
Download septoria-leaf.zip and unzip the folder. Make sure that program path is encoded in Latin-1 (ISO-8859-1). 
septoria-leaf/
|-- slabels.py
|-- sleaves.py
|-- object_list.txt
|-- output
|   |-- 1-1-1_leafNO_1.jpg
|   |-- 1-1-1_leafNO_2.jpg
|   …
|   |-- diseased_1-1-1_leafNO_1.jpg
|   |-- diseased_1-1-1_leafNO_1.jpg
|   …
|-- labels_output
|   |-- 1-1-1.jpg
|   |-- 1-1-2.jpg
|   …
|-- input_images
    |-- image1.jpg
    |-- image2.jpg
    …

You may install modules automatically by running:
python setup.py develop
in the command line in the directory where setup.py is located.
Definitions:
Image sample is a digital image of wheat or triticale leaves in a seedling growth stage.
Sample_name is a text read from label. Code name of image sample.
leaf_area is a total area in pixels of one extracted leaf from an image sample.
disease_area is a total diseased area in pixels of leaf extracted from an image sample.
disease_percetage is a ratio of disease_area to leaf_area *100.

Preparation of image samples:
Leaves in an image sample should be in one piece, using fragmented leaves is not advised because the program will interpret them as a whole leaf. Leaves should not touch each other, otherwise software will interpret them as a single leaf. The suggested colour of background is blue in order to easily extract leaves from image samples. Image sample labels by default should be rectangular approximately 5 cm in width and 1 cm in height with black characters description on a red background.
Run the program:
slabels.py – is a small software assisting with the laborious and time consuming image file naming task. The program extracts a text from labels in an image and renames each file. Depending on various factors an image colour reproduction can differ, therefore for optimization of the parameters follow the steps: 
1.	Prepare a list of labels to read in object_list.txt file located in the main directory - septoria-leaf. Each row should contain a single label name formatted in d-d-d manner, where d is a number. By default slabels.py use following whitelist characters: -0123456789.
1-1-1
1-1-2
1-2-1
…
2.	Place prepared images in the directory - input_images. Make sure that object samples are not duplicated. 
3.	Adjust the label_hue_min, label_hue_max and binary_threshold in the slabels.py file. The HUE parameter is used for slicing the red label contour while the binar_threshold is a grayscale threshold for extraction of label characters.
binar_threshold = 57  # Binarization grayscale threshold default 57
label_hue_min = 80  # min HUE, default 80
label_hue_max = 97  # max HUE, default 97
4.	Enable writing of sliced and binarized images in order to check if thresholding parameters were optimised successfully. Sliced and binarized images will be located in the lables_output directory.
save_im_ready = True  # True/False save an image ready to read
save_im_binar = True  # True/False save an binarized image
5.	The label orientation in an image can differ from -10 to 10 degrees by default. To manually apply rotation degrees edit maximum rotation angle in ang_input. 
ang_input = 10  # Rotation angle range default 10 (-10 to 10).
6.	Run the slabels.py program.
7.	Output images will be located in the labels_output directory. Unrecognized images will be named as UNRECOGNIZED_<img_name>. If a read file name is doubled or a file label will not match any object in the object_list.txt, the image will be saved as CHECK_NAME_<label_name>.jpg. If settings were optimized user have to manually correct file names. 

sleaves.py – the software evaluates diseased area percentage and summarises results in tables. To run the program and optimize the parameters follow the protocol: 
1.	The Sleaves.py program analyses files from the labels_output folder.
2.	To enable extracted leaves and diseased tissue write, set the save_leaf_im and save_diseased_im variables to True. Files will be located in the output folder.
save_leaf_im = True  # True/False save an extracted leaf image
save_diseased_im = True  # True/False save an diseased image
3.	To calibrate the leaf HUE parameter leaf_hue_min and leaf_hue_max values can be modified:
leaf_hue_min = 0  # Min leaf HUE, default 0
leaf_hue_max = 90  # Max leaf HUE, default 90
4.	To calibrate the diseased tissue HUE parameter, the diseased_hue_min and diseased_hue_max values can be modified:
diseased_hue_min = 0  # Min diseased HUE, default 0
diseased_hue_max = 45  # Max diseased HUE, default 45
5.	Run the sleaves.py program.
6.	After the program completes analysis output files in *.csv format will be created in the main folder septoria-leaf. The results.csv file will contain all leaves results summary (sample leaf_area, disease_area and disease_percentage). The pivot_table.csv file is table summary of a results table grouped by sample name. The pivot_table.csv contain leaf_area and disease_area aggregated by sum for each object name and average of a disease_percentage.

Authors
Sławomir Bartosiak

License

Acknowledgments
Stack Overflow community.
  
