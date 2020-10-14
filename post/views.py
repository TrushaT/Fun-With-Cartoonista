from django.shortcuts import render,get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, RedirectView, ListView
from .forms import PostForm,SearchForm
from django.urls import reverse_lazy, reverse
from django.template.defaultfilters import slugify
from taggit.models import Tag
from cartoonify.views import upload
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import json
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            txtSearch = form.cleaned_data['txtSearch']
            qs = Post.objects.filter(tags__name__icontains=txtSearch)
            context = {
                'posts': qs,
                'txtSearch': txtSearch,
                'title': f"'{txtSearch}' Results"
                }      
            return render(request,'post/search.html',context)
    return HttpResponseRedirect('/gallery')

def autocompleteModel(request):

    if 'term' in request.GET:
        qs = Tag.objects.filter(name__icontains=request.GET.get('term'))
        tags_list = list()
        for p in qs:
            tags_list.append(p.name)
        return JsonResponse(tags_list,safe=False)

class PostListView(ListView):
    model = Post
    template_name = 'post/gallery.html' # <app>/<model>_<viewtype>.html is the naming convention, here we modified it !
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        common_tags = Post.tags.most_common()[:5]
        context['common_tags'] = common_tags
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'post/category.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 6

    def get_queryset(self, **kwargs):
        category = get_object_or_404(Tag,slug=self.kwargs.get('slug'))
        return Post.objects.filter(tags=category).order_by('-pub_date') 

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Tag,slug=self.kwargs.get('slug'))
        context['category'] = category
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_posts_feed.html' 
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 6
    
    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username')) 
        return Post.objects.filter(author=user).order_by('-pub_date')

    def get_context_data(self, *args, **kwargs):
        context = super(UserPostListView, self).get_context_data()
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        context['user_name'] = user.username
        context['user_bio'] = user.profile.bio
        context['profile_image'] = user.profile.image.url
        return context 

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/add_post1.html'
    #fields = ('title','caption')
    def get_context_data(self, *args, **kwargs):
        context = super(AddPostView, self).get_context_data()
        url = self.request.session['result_img_url']
        context['image_url'] = f'/media/{ url }'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.author = self.request.user
        newpost.header_image = self.request.session['result_img_url']
        newpost.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        return super().form_valid(form)
    

class PostDetailView(DetailView):
    model = Post 
    template_name = 'post/post_detail.html'

    def get_context_data(self , *args, **kwargs):
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        context = super(PostDetailView, self).get_context_data()
        context['related_posts'] = stuff.tags.similar_objects()
        return context
        
class UpdatePostView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    template_name = 'post/post_update.html'
    fields = ['title','caption','tags'] 
    form = PostForm
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DeletePostView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post 
    template_name = 'post/delete_post.html'
    success_url = '/'    
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostLikeToggle(RedirectView):
    def get_redirect_url(self,*args, **kwargs):
        id_ = self.kwargs.get("pk")
        obj = get_object_or_404(Post,pk=id_)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                 obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None,format=None):
        obj = get_object_or_404(Post,pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        verb = None
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                verb = 'Like'
                obj.likes.remove(user)
                count = obj.likes.all().count()
            else:
                liked = True
                verb = 'Unlike'
                obj.likes.add(user)
                count = obj.likes.all().count()
            updated = True
        data = {
            "updated":updated,
            "liked":liked,
            "count":count,
            "verb":verb
        }
        return Response(data)
