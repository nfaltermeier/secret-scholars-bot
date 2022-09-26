import cv2
import numpy as np
import math
import aiohttp
import os
import config as conf
from PIL import Image

face_cascade = cv2.CascadeClassifier('lib/opencv/face_detector.xml')
eye_cascade = cv2.CascadeClassifier('lib/opencv/eye_detector.xml')
smile_cascade = cv2.CascadeClassifier('lib/opencv/smile_detector.xml')

def load_image_rgba(path):
  og_image = Image.open(path)
  rgba_image = og_image.convert(mode='RGBA')
  img = np.array(rgba_image)
  # B and R channels are swapped and there didn't seem to be a better way to do this
  copy = np.array(img)
  img[:,:,0] = copy[:,:,2]
  img[:,:,2] = copy[:,:,0]
  return img

# https://www.geeksforgeeks.org/python-smile-detection-using-opencv/
def box_faces(gray, frame):
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x, y, w, h) in faces:
    # print(f'{x}, {y}, {w}, {h}')
    cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0, 255), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = frame[y:y + h, x:x + w]
    # smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
    eyes = eye_cascade.detectMultiScale(roi_gray)

    for (sx, sy, sw, sh) in eyes:
      # print(f'{sx}, {sy}, {sw}, {sh}')
      cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255, 255), 2)
  return frame

# https://stackoverflow.com/a/59211216
def rgba_overlay(background, foreground):
  alpha_background = background[:,:,3] / 255.0
  alpha_foreground = foreground[:,:,3] / 255.0

  # set adjusted colors
  for color in range(0, 3):
      background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
          alpha_background * background[:,:,color] * (1 - alpha_foreground)

  # set adjusted alpha and denormalize back to 0-255
  background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255

def replace_faces(gray, frame, replacement, replacement_dims):
  faces = face_cascade.detectMultiScale(gray, 1.1, 5)
  base_w = frame.shape[1]
  base_h = frame.shape[0]
  found = False
  for (x, y, w, h) in faces:
    found = True
    overlay = np.zeros(frame.shape)
    replacement_scale_x = w / replacement_dims[0][2]
    replacement_scale_y = h / replacement_dims[0][3]
    scaled_replacement_x = x - math.ceil(replacement_dims[0][0] * replacement_scale_x)
    scaled_replacement_y = y - math.ceil(replacement_dims[0][1] * replacement_scale_y)
    scaled_full_w = math.ceil(replacement.shape[1] * replacement_scale_x)
    scaled_full_h = math.ceil(replacement.shape[0] * replacement_scale_y)
    resized = cv2.resize(replacement, (scaled_full_w, scaled_full_h), interpolation=cv2.INTER_CUBIC)
    up = base_h - (scaled_full_h + scaled_replacement_y)
    up = -scaled_replacement_y if scaled_replacement_y + up < 0 else 0
    left = base_w - (scaled_full_w + scaled_replacement_x)
    left = -scaled_replacement_x if scaled_replacement_x + left < 0 else 0
    insert_w = base_w - scaled_replacement_x if scaled_replacement_x + scaled_full_w > base_w else scaled_full_w
    insert_h = base_h - scaled_replacement_y - up if scaled_replacement_y + scaled_full_h + up > base_h else scaled_full_h
    overlay[scaled_replacement_y + up:scaled_replacement_y + insert_h + up, scaled_replacement_x + left:scaled_replacement_x + insert_w + left] = resized[0:insert_h, 0:insert_w]
    rgba_overlay(frame, overlay)
  
  return found, frame

def get_face_replace(replacing_image):
  face_replace = load_image_rgba(conf.face_picture)
  attachment_pic = load_image_rgba(replacing_image)
  gray = cv2.cvtColor(attachment_pic, cv2.COLOR_RGBA2GRAY)
  found,img = replace_faces(gray, attachment_pic, face_replace, conf.face_dims)

  if found:
    cv2.imwrite('face_detected.png', img)
    return True, 'face_detected.png'
  
  return False, None

if __name__ == '__main__':
  img = load_image_rgba('student_small.png')
  # img = load_image_rgba('group.png')
  student = np.array(img)

  face = load_image_rgba('face.png')
  face_dims = [
    [43, 208, 430, 430],
    [245, 125, 82, 82],
    [98, 131, 87, 87]
  ]
  gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
  found,img = replace_faces(gray, img, face, face_dims)
  cv2.imwrite("face_detected.png", img)
  print('Successfully saved')

# A video with faces applied for testing purposes
# video_capture = cv2.VideoCapture(0)
# while video_capture.isOpened():
# # Captures video_capture frame by frame
#   _, frame = video_capture.read()

#   # To capture image in monochrome				
#   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
#   # calls the box_faces() function
#   canvas = box_faces(gray, frame)

#   # Displays the result on camera feed					
#   cv2.imshow('Video', canvas)

#   # The control breaks once q key is pressed					
#   if cv2.waitKey(1) & 0xff == ord('q'):			
#     break

# # Release the capture once all the processing is done.
# video_capture.release()								
# cv2.destroyAllWindows()

