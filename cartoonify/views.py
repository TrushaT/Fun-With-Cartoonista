from django.shortcuts import render
from django.http import HttpResponse
import cv2
from django.shortcuts import render,get_object_or_404
from django.core.files.storage import FileSystemStorage


def home(request):
    if request.method == 'POST' :
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage(location='media/original_pics')
        fs.save(uploaded_file.name, uploaded_file)
        recent_file_name = uploaded_file.name

        img = cv2.imread(f"media/original_pics/{recent_file_name}") # FILEPATH

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 3)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        color = img
        for _ in range(50): 
            color = cv2.bilateralFilter(color, 5, 14, 7) 

        cartoon = cv2.bitwise_and(color, color, mask=edges) # FINAL CARTOON IMAGE
        
        cv2.imwrite(f'media/cartoonified_images/{recent_file_name}_result.png',cartoon)
        original_img_url = f'media/original_pics/{recent_file_name}'
        result_img_url = f'media/cartoonified_images/{recent_file_name}_result.png'
        request.session['result_img_url'] =  f'cartoonified_images/{recent_file_name}_result.png'
        context = {
            'original_img_url': original_img_url,
            'result_img_url' : result_img_url,
        }
        return render(request, 'cartoonify/home.html', context)

    else:
        return render(request, 'cartoonify/home.html')

