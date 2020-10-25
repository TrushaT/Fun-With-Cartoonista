from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from .forms import ImageUploadForm
from .models import Image
import base64
import cv2
import numpy as np
import boto3
import botocore
import os


def index(request):
    return render(request,'cartoonify/index.html')

def upload(request):
    if request.method == 'POST' :
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(request)
            name_of_image = form.cleaned_data['original_image']
            original_image_name = f'original_image/{name_of_image}'
            original_image_name = original_image_name[:original_image_name.index('.')]

            images = Image.objects.filter(original_image__startswith=original_image_name).order_by('-date_time')
            image = images[0]
            original_image_url = image.original_image.url
            cartoonified_image_url = image.cartoonified_image.url

            request.session['result_img_url'] = cartoonified_image_url
            request.session['result_img_name'] = image.cartoonified_image.name

            context = {
                    'form' : form ,
                    'original_image_url':original_image_url,
                    'result_image_url':cartoonified_image_url
                    }

            #updating meta-data for download 
            s3 = boto3.resource(
                service_name='s3',
                region_name='us-east-2',
                aws_access_key_id=os.environ.get('CARTOONISTA_AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('CARTOONISTA_AWS_SECRET_ACCESS_KEY')

            ) 
            s3_object = s3.Object('cartoonista-files',image.cartoonified_image.name)
            s3_object.metadata.update({'Content-Disposition':'attachment'})
            s3_object.copy_from(CopySource={'Bucket':'cartoonista-files','Key':image.cartoonified_image.name}, Metadata=s3_object.metadata, MetadataDirective='REPLACE')
           
            return render(request,'cartoonify/upload.html',context)

            

    else:
        form = ImageUploadForm()
        context = dict(form=form)
        return render(request,'cartoonify/upload.html',context)
            
