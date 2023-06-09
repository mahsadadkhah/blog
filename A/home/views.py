from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostUpdateCreateForm
from django.utils.text import slugify
from django.contrib import messages
from .models import Post


class HomeView(View):
    def get(self, request):
        posts = Post.objects.order_by('-created')
        return render(request, 'home/home.html', {'posts': posts})


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:30])
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'you created a new post successfully.', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'], slug=kwargs['post_slug'])
        return render(request, 'home/detail.html', {'post': post})


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.author.id == request.user.id:
            messages.error(request, 'you cant update post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form':form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you updated this post', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.author.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('home:home')












