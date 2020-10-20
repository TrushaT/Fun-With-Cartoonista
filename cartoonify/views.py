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

def index(request):
    return render(request,'cartoonify/index.html')

def upload(request):
    if request.method == 'POST' :
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(request)
            name_of_image = form.cleaned_data['original_image']
            original_image_name = f'original_image/{name_of_image}'
        
            images = Image.objects.filter(original_image=original_image_name).order_by('-date')
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
            
            return render(request,'cartoonify/upload.html',context)

            

    else:
        form = ImageUploadForm()
        context = dict(form=form)
        return render(request,'cartoonify/upload.html',context)
            
