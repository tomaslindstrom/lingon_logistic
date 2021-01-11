# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:16:04 2020

Detta är rensade produktionsfilen dvs alla utlis fpör development är urrensade.
Det finns en "developmentversion" med stöd för utveckling
Modulens extraherar tränings- och testdata från lingonbilderna som placerats i biblioteken:
    .\datasets\train_lingonset
    .\datasets\test_lingonset

Funktionen anropas med:  load_lingon_dataset()
Resultatet levereras med: 
    return train_lingonset_x_orig, train_lingonset_y_orig, test_lingonset_x_orig, test_lingoset_y_orig, lingonklasser

Seten är av klassen numpy array av storleken antal bilder, num_px, num_px, 3, där höjden = num_px, bredden = num_px, 
med default num_px = 64.

Bilderna i tränings- och testsetet är märkta (lablade) med "lingon" , "icke-lingon" i exif-metadata fältet: tag ="UserComment".
Lingonklasser är en numpy array som anger vilka lablar (etiketter) som finns dvs: "lingon" och "icke-lingon"  
@author: ISOFT
"""
    
import os 
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS


def extract_y(lingon_path,image):
    """
    Parameters
    ----------
    lingon_path: 
    image : string
        DESCRIPTION.
        Extracts the label of the image from the exif-metadata tag 
        tag = "UserComment".
        Tests if all images are labeled i.e. has a value in tag.
    Returns
    -------
    1 if "lingon", 0 if "icke-lingon"
    """    
    image_extract = Image.open(lingon_path+"/"+image)    
    image_exifdata = image_extract.getexif()
    # itterate over exifdata and find "UserComment"
    for tag_id in image_exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        
        if tag == "UserComment":
            data = image_exifdata.get(tag_id)
            # decode bytes 
            
            if  isinstance(data, bytes):
                data = data.decode()
                data = data.strip("ASCII\x00\x00\x00")
                
                #print(f"{tag:25}: {data}")
                #print(data)
                return data
               
def convert_dataset(set_cat):
    """
    
    
    Parameters
    ----------
    set_cat : TYPE
        DESCRIPTION.
        The arguments "train" or "test"
    Returns
    -------
     returns extracted x (set features) and y (set labels) as numpy arrays.
     return "set_cat"_dataset_x "set_cat"_dataset_y  
     """
    
    lingonset_x_list = []
    lingonset_y_list = []
    if set_cat == "test" or set_cat == "train":
        lingon_path = lingon_path_main+set_cat+"_lingonset"+"/"
    else:
        lingon_path = lingon_path_main+set_cat+"/"
    for image in os.listdir(lingon_path):
        
        #Create label list i.e. y= 1 if "lingon", y = 0 if "icke-lingon"
        image_label =  extract_y(lingon_path,image)
        #print(image_label)
        lingonset_y_list.append(1) if image_label == "lingon" else  lingonset_y_list.append(0)
                
        # Create numpy array of image
        image_conv = Image.open(lingon_path+"/"+str(image))
        image_array = np.asarray(image_conv)
        lingonset_x_list.append(image_array)
        
    # Gör om listorna till numpy arrays
    lingon_arr_x = np.array(lingonset_x_list)
    lingon_arr_y = np.array(lingonset_y_list)
    
    return tuple(lingon_arr_x),tuple(lingon_arr_y)       
                    





def extract_dataset(set_cat):
    """
    
    
    Parameters
    ----------
    set_cat : arguments "train" or "test"
        DESCRIPTION.
        Extracts the image names with lanbels (exif) as a tuple with strings
    Returns
    -------
     returns extracted x (set images) and y (set labels) as string elements.
     return "set_cat"_dataset_x "set_cat"_dataset_y  
     """
    
    lingonset_x = []
    lingonset_y = []
    #print(set_cat)
    if set_cat == "test" or set_cat == "train":
        lingon_path = lingon_path_main+set_cat+"_lingonset"+"/"
    else:
        lingon_path = lingon_path_main+set_cat+"/"
    for image in os.listdir(lingon_path):
        lingonset_x.append(image)
        lingonset_y.append(extract_y(lingon_path,image))
        
        #print(lingonset_y)
    
    return lingonset_y, lingonset_x 
     
   
def resize_image_set (num_px, num_py):
    """
    Resizes the images to num_x and num_y sizes.
    Renames the images to "imagename"_res.ext.
    Resizes both sets i.e. train and test.

    Parameters
    ----------
    num_x : int
        DESCRIPTION.
    num_y : int
        DESCRIPTION.

    Returns
    -------
    None.

    """
   
    for data_set in data_sets:               # Sets path to test or train
        lingon_path = lingon_path_main+data_set+"_lingonset"
        
        for image in os.listdir(lingon_path):
         
            im = Image.open(str(lingon_path)+"/"+image)
            im_exifdata = im.getexif()
            im = im.resize((num_px,num_py))
            #print(image, lingon_path)
            im.save(str(lingon_path)+"/"+image, exif=im_exifdata)   #Save with replace of old name, possible change in future
            im.close()
    
 
def data_assure():
    """
    Parameters:
        None
        DESCRIPTION:
        Qualityassurance the dataset i.e. test and train set by:
            - Checking that all images are labeled and  with right labels (correct_lables)
            - Ensure that there are no copies  within the test-train set
            - Ensure that the there are no copies (names) between the test and train set.  

    Returns
    -------
     assu_mess: Tuplpe that includes  
        True : All images are correct labeled, with no messate
        False: Uncorrect labeling, includes a message assu_mess[0]
    """
    test_lingonset_y, test_lingonset_x = extract_dataset("test")
    train_lingonset_y, train_lingonset_x = extract_dataset("train")
    
    
    # Test completness and accuracy of labels
    for data_set_y in data_sets:                   #data_sets contains "train" and "test" 
         
        if data_set_y == "train":  
            qa_set_y = set(train_lingonset_y)
        else: 
            qa_set_y = set(test_lingonset_y)
        
        #Loop trhough the set and find wrong or missing label
        for qa_test_obj in qa_set_y:
            
            if qa_test_obj not in correct_labels:           #Tests if label not "lingon" or "icke-lingon"
                assu_mess = (False, data_set_y +"set includes wrong or emtpy label")
                break
            
            else:
                assu_mess = (True, "")      
       
    return  assu_mess



def load_lingon_dataset(num_px = 64, num_py = 64):

    """

    Parameters:
        num_x, num_y resize parameters, default 64.
        num_px = width , num_py = hight
        
        DESCRIPTION:
        Changed copy from lab, only return is changed.
        
        Prepares- preprocesses the dataset from loaded images in:
            - train : ./dataset/train_lingonset , m_train labeled images
            - test : ./dataset/test_lingonset , m_test labeled images
        
        Input images are:
            - labeled "lingon" - "icke-lingon" in exif filed "UserComment"
            - of different sizes
    
         Data set preparations :
             - quality assurance i.e. lable names correct and all have labels
             - no duplicates in sets or between sets ( to be developed)
             - resizing , default num_x and num_y = 60 (to be developed.
             - create feature arrays with RGB codes
                 - train_set_x_orig:  numpy-array of shape( m_train, num_px, num_py, 3).
                 - test_set_x_orig:    numpy-array of shape (m_test, num_px, num_py, 3)
            - create the label arrays: lingon (y=1), icke-lingon (y=0)   
    Returns
    -------
      train_set_x_orig #Train set features, numpy array f shape (m_train, num_px, num_py,3)
      train_set_y_orig #Train set lables 
      
      test_set_x_orig #Test set features, numpy array f shape (m_test, num_px, num_py,3)
      test_set_y_orig #Test  set labels
      
      classes  np array of the classes i.e. labels
      
    """

    
    #Set paths and correct labels as globals for alla functions
    
    global lingon_path_main, data_sets, correct_labels 
    
    lingon_path_main = "./datasets/"             #Home directory for both sets
    data_sets = ("train", "test")
    correct_labels = ("lingon", "icke-lingon")   #Labels for images corresponding to 1 and 0
    
    
    # Quality assure sets

    qa_stat, qa_mess = data_assure()
    if qa_stat  is False:              #Calls the data assure function
        raise ValueError (qa_mess)
    
    # Resize images to num_px and num_py- dafault num_px = 64, num_py = 64
    # To do:
    #  -  Currently resize with same name, should change name after resize, maybe tag as well
    
    resize_image_set (num_px, num_py)
    
    # Build data sets
    #Create and convert trainset to numpy.ndarrays  
    train_set_x_tuple, train_set_y_tuple = convert_dataset("train")
    train_set_x_orig = np.array(train_set_x_tuple)      # Train set features
    train_set_y_orig = np.array(train_set_y_tuple)      # Train set labels
    
    #Create and convert trainset to numpy.ndarrays
    test_set_x_tuple, test_set_y_tuple = convert_dataset("test")
    test_set_x_orig = np.array(test_set_x_tuple)      # Test set features
    test_set_y_orig = np.array(test_set_y_tuple)      # Test set labels
    
    #reshape label arrays to (1, number of images)
    train_set_y_orig = train_set_y_orig.reshape(1,train_set_y_orig.shape[0])
    test_set_y_orig = test_set_y_orig.reshape(1, test_set_y_orig.shape[0])
    #Create classes - list i.e. the two classes "lingon" och "icke-lingon"
    
    classes = correct_labels
    
 
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes
     



def load_lingon_testset(re_test_lingonset, num_px = 64, num_py = 64):
    
    """
        Parameters:
        num_x, num_y resize parameters, default 64.
        num_px = width , num_py = hight
        
        DESCRIPTION:
        Prepeare a selected test-set to be verified on the model.
        
        
        Prepares- preprocesses the dataset from loaded images in:
            - test : ./dataset/re_test_lingonset , m_test labeled images
        
        Input images are:
            - labeled "lingon" - "icke-lingon" in exif filed "UserComment"
            - of different sizes
    
         Data set preparations :
             - quality assurance i.e. lable names correct and all have labels
             - no duplicates in sets or between sets ( to be developed)
             - resizing , default num_x and num_y = 64 (to be developed.
             - create feature arrays with RGB codes
                 - train_set_x_orig:  numpy-array of shape( m_train, num_px, num_py, 3).
                 - test_set_x_orig:    numpy-array of shape (m_test, num_px, num_py, 3)
            - create the label arrays: lingon (y=1), icke-lingon (y=0)   
    Returns
    -------
            
      re_test_set_x_orig #Test set features, numpy array f shape (m_test, num_px, num_py,3)
      re_test_set_y_orig #Test  set labels
      
      classes  np array of the classes i.e. labels
    
    """
    
    #Qualtity ensure that all images are labeled
    re_test_lingonset_y, re_test_lingonset_x_orig = extract_dataset(re_test_lingonset)
    
    #Loop through the set and find wrong or missing label
    for qa_test_obj in re_test_lingonset_y:
        #print(qa_test_obj)
        if qa_test_obj not in correct_labels:           #Tests if label not "lingon" or "icke-lingon"
            raise ValueError ("Missing or wrong label")
            break
    
    #Resize test set
    test_set_path = lingon_path_main+re_test_lingonset
    for image in os.listdir(test_set_path):
        im = Image.open(str(test_set_path)+"/"+image)
        im_exifdata = im.getexif()
        im = im.resize((num_px,num_py))
        #print(image, test_set_path)
        im.save(str(test_set_path)+"/"+image, exif=im_exifdata)   #Save with replace of old name, possible change in future
        im.close()
    
    # Build data sets
        
    #Create and convert trainset to numpy.ndarrays
    re_test_set_x_tuple, re_test_set_y_tuple = convert_dataset(re_test_lingonset)
    re_test_set_x_orig = np.array(re_test_set_x_tuple)      # Test set features
    re_test_set_y_orig = np.array(re_test_set_y_tuple)      # Test set labels
    
    #reshape label arrays to (1, number of images)
    re_test_set_y_orig = re_test_set_y_orig.reshape(1, re_test_set_y_orig.shape[0])
    #Create classes - list i.e. the two classes "lingon" och "icke-lingon"
    
    #print(re_test_set_x_orig)
    #print(re_test_set_y_orig)
    
    return re_test_set_x_orig, re_test_set_y_orig

# In[3]
"""
Call for load function for test purposes : load_ligon_testset

re_test_set_x_orig, re_test_set_y = load_lingon_testset("testset_lingon_skräp_bär_100",64 ,64)

print(type(re_test_set_x_orig))
print((re_test_set_x_orig).shape)
print(type(re_test_set_y))
print((re_test_set_y).shape)
print(re_test_set_y)
"""
# In[2]
"""
Call for load function - for test purposes for : load_lingon_dataset - function

train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes = load_lingon_dataset(64,64)        #Paramenters num_px, num_py could be added
print(type(train_set_x_orig))
print((train_set_x_orig).shape)
print(type(train_set_y_orig))
print((train_set_y_orig).shape)
print(type(test_set_x_orig))
print((test_set_x_orig).shape)
print(type(test_set_y_orig))
print((test_set_y_orig).shape)
print(type(classes))
print(train_set_y_orig)
print(test_set_y_orig)
"""
