#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.

# In[1]:


import zipfile
from zipfile import ZipFile 
import PIL
from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!


# In[2]:


#images=[]
def display_contactSheet(facelist):
    
    images=facelist
    first_image=images[0]
    column=len(images)//5+1
    contact_sheet=PIL.Image.new(first_image.mode, (500,100*column))
    x=0
    y=0

    for img in images:
        # Lets paste the current image into the contact sheet
        contact_sheet.paste(img, (x, y) )
        # Now we update our X position. If it is going to be the width of the image, then we set it to 0
        # and update Y as well to point to the next "line" of the contact sheet.
        if x+first_image.width == contact_sheet.width:
            x=0
            y=y+first_image.height
        else:
            x=x+first_image.width

    # resize and display the contact sheet
    #contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
    
    display(contact_sheet)
        
    


# ### SMALL DATA SET small zip

# In[3]:


smallzip = "readonly/small_img.zip"
#bigzip = "readonly/images.zip"
file_name=smallzip
my_dict = {}
with ZipFile(file_name, 'r') as zip: 
    for info in zip.infolist(): 
        #print(info.filename) 
        facelist=[]
        image=Image.open(info.filename)
        grayimage = image.convert('L')
        text = pytesseract.image_to_string(grayimage)
        
        if "Christopher" in text:
            print("Results found in file "+ str(info.filename))
            #img = cv.imread(info.filename)
            #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            #faces = face_cascade.detectMultiScale(gray,1.3,5)
            img = np.array(image)
            faces = face_cascade.detectMultiScale(img,1.3,5)
            #drawing=ImageDraw.Draw(image)
            for x,y,w,h in faces:
                #drawing.rectangle((x,y,x+w,y+h), outline="white")
                cropped_image=image.crop((x,y,x+w,y+h))
                cropped_image.thumbnail((100, 100), Image.ANTIALIAS)  
                #display(cropped_image)
                facelist.append(cropped_image)
            #Finally lets display this
            if len (facelist) == 0 :
                print("But there were no faces in that file!")
            else:
                display_contactSheet(facelist)
                my_dict[info.filename] = [image,text,facelist]


# ### BIG DATA SET big zip

# In[11]:


bigzip = "readonly/images.zip"
file_name=bigzip
my_dict = {}
imagefilelist = []
with ZipFile(file_name, 'r') as zip:
    #info_lst = zip.infolist()
    for info  in zip.infolist():
        with zip.open(info) as file:
            image = Image.open(file)
            image.load()
            info = {'image': image, 'filename': info.filename}
            imagefilelist.append(info)

searchtext = 'Mark'

for file in imagefilelist:
    image=file['image']
    gray = image.convert('L')
    text = pytesseract.image_to_string(gray)
    facelist=[]
    if searchtext in text:
        print('Results found in file {}'.format(file['filename']))
        # find and display faces
        
        img = np.array(image) #convert img to ndarray
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        if len(faces) == 0:
            print('But there were no faces in that file')
        else:
            for x,y,w,h in faces:
                #drawing.rectangle((x,y,x+w,y+h), outline="white")
                cropped_image=image.crop((x,y,x+w,y+h))
                cropped_image.thumbnail((100, 100), Image.ANTIALIAS)  
                #display(cropped_image)
                facelist.append(cropped_image)
            display_contactSheet(facelist)
                


# In[ ]:




