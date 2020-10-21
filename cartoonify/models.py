from django.db import models
import cv2
import numpy as np
import os
import boto3
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from django.contrib.auth.models import User

class Image(models.Model):
    date = models.DateField(auto_now_add=True)
    cartoonified_image = models.ImageField(upload_to='cartoonified_image')
    original_image = models.ImageField(upload_to='original_image')

    def save(self,*args,**kwargs):
        if self.original_image:
            b64_img = base64.b64encode(self.original_image.file.read())
            im_bytes = base64.b64decode(b64_img)
            im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            gray = cv2.medianBlur(gray, 3)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

            color = img
            for _ in range(50): 
                color = cv2.bilateralFilter(color, 5, 14, 7) 

            cartoon = cv2.bitwise_and(color, color, mask=edges)
            image_content = cv2.imencode('.jpg', cartoon)[1].tostring()
            result_image_name = f'{self.original_image.name}_result.png'
            self.cartoonified_image = SimpleUploadedFile(result_image_name,image_content)
        super(Image,self).save(*args,**kwargs)



    


        



            