from django import forms
from .models import Image
import cv2
import numpy as np
import os
import boto3
from botocore.exceptions import ClientError



class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['original_image']

    