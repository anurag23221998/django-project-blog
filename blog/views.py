from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from .blog_create_form import CreatePost
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.


# def home(request):
#     context = {
#         'posts': Post.objects.all().order_by('date_posted').reverse(),
#         'title': 'Dummy Data'
#     }
#     return render(request, 'blog_themes/content.html', context)

# Blog List
class PostListView(ListView):
    model = Post
    # template_name = 'blog_themes/content.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog_themes/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



# Blog Detail
class PostDetailView(DetailView):
    model = Post
    # template_name = 'blog_themes/post_detail.html'


# Blog Create
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']   
    template_name = 'blog_themes/blog_create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
# Blog update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog_themes/blog_create_form.html'
    success_url = '/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.get_object().author == self.request.user:
            return True
        return False



# Blog Delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog_themes/blog_delete.html'
    success_url = '/'

    def test_func(self):
        if self.get_object().author == self.request.user:
            return True
        return False
    
    
        

def about(request):
    return render(request, 'blog_themes/about.html')



@login_required
def createBlog(request):
    if not request.user.is_authenticated:
        return HttpResponse('Not Authorized')
    if request.method == 'POST':
        form = CreatePost(request.POST)
        instance = form.save(commit=False)
        instance.author = request.user
        if form.is_valid():
            instance.save()
            post_title = form.cleaned_data.get('title')
            messages.success(request, f'{post_title} Post is created')
            return redirect('blog-home')
        
    else:
        form = CreatePost()
    return render(request, 'blog_themes/blog_create_form.html', {'form': form})