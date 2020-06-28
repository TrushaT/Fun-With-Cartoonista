import cv2
from django.shortcuts import render,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify
from .models import Post
from .form import PostForm
from taggit .models import Tag

def upload(request):
    if request.method == 'POST' :
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        recent_file_name = uploaded_file.name

        img = cv2.imread(f"media/{recent_file_name}") # FILEPATH
        print(img)

        # img = cv2.resize(img,(500,650)) # RESIZE IF NEEDED

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 3)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        color = img
        for _ in range(50): 
            color = cv2.bilateralFilter(color, 5, 14, 7) 

        cartoon = cv2.bitwise_and(color, color, mask=edges) # FINAL CARTOON IMAGE
        print(cartoon)
        cv2.imwrite(f'media/{recent_file_name}_result.png',cartoon)
        print('image saved')
        # ret, frame_buff = cv2.imencode('.jpg', cartoon) #could be png, update html as well
        # frame_b64 = base64.b64encode(frame_buff)

        img_url = f'media/{recent_file_name}_result.png'
        return render(request, 'conversion/upload.html', {'img_url': img_url})

    else:
        return render(request, 'conversion/upload.html')

def share(request):
    #img = Post(uploaded_pic = image)

    #posts = Post.objects.order_by('-published')
    # Show most common tags 
    #common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST)
    if form.is_valid():
        newpost = form.save(commit=False)
        #newpost.slug = slugify(newpost.title)
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
    context = {
        #'posts':posts,
        #'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'conversion/share.html', context)

