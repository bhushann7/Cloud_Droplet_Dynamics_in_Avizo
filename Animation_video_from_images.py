
#Check whether necessry modules i.e. "opencv","numpy","glob" are installed



#-------------------------------- Main Program begins ---------------------------------------

import cv2
import numpy as np
import glob
#---------------------------------------- For timesteps 100-3500 ---------------------------------------------------------------------------------------------

files =glob.glob("/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Outputs/0.5_avizo_outputs_0_4k/*.png")
img_array = []
#For loop for range 100-3500 timesteps
for i in range(100,3600,100):
  path = "/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Outputs/0.5_avizo_outputs_0_4k/img_"+str(i)+".png"
  image = cv2.imread(path)
  print('b '+str(i))
  height, width, layers = image.shape
  print('a '+str(i))
  size = (width,height)
  img_array.append(image)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('CloudDropletVisualization_100_to_3500.mp4',fourcc,1, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

#---------------------------------------- For timesteps 11000 -15000 ---------------------------------------------------------------------------------------------

files =glob.glob("/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Outputs/0.5_avizo_outputs_11k_to_15k/*.png")
image_array =[]
#For loop for range 11000-15000 timesteps
for i in range(11000,15100,100):
  path = "/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Outputs/0.5_avizo_outputs_11k_to_15k/img_"+str(i)+".png"
  image1 = cv2.imread(path)
  height, width, layers = image.shape
  size = (width,height)
  image_array.append(image1)
  i+=100

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('CloudDropletVisualization_11000_to_15000.mp4',fourcc,1, size)

for i in range(len(image_array)):
    out.write(image_array[i])
out.release()
