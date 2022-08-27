from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, View, FormView, DeleteView, UpdateView
from .forms import PostForm, CommentsForm, CommentNewForm
from .models import Post, Comment, News, User
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from .emails import notify_request_accept


class NewPostView(CreateView, PermissionRequiredMixin):
    template_name = 'new_post.html'
    form_class = PostForm
    context_object_name = 'new_post'
    success_url = '/board'
    permission_required = 'board.add_post'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NewPostView, self).form_valid(form)


class PostsList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts_list.html'
    context_object_name = 'posts'
    paginate_by = 8


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object(queryset=None)
        context['comments'] = instance.comment_set.all()
        context['post_user'] = instance.user
        context['user'] = self.request.user
        context['form'] = CommentNewForm
        return context


@login_required
def comment_save(request, pk):
    if request.method == 'POST':
        comment_form = CommentNewForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = Post.objects.get(pk=pk)
            comment.save()

            return redirect(f'/board/post/{comment.post.pk}')





class PostUpdate(UpdateView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_update.html'
    context_object_name = 'post'
    form_class = PostForm
    permission_required = 'board.change_post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object(queryset=None)
        context['post'] = instance
        return context

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk})


class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    permission_required = 'board.delete_post'
    success_url = '/board'


class CommentsList(ListView):
    model = Comment
    template_name = 'post_detail.html'
    context_object_name = 'comments'


class NewsList(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news'


class NewsArticle(DetailView):
    model = News
    template_name = 'news_article.html'
    context_object_name = 'news'


#  class CommentAdd(CreateView):
#      model = Comment
#      form_class = CommentNewForm
#      template_name =


@login_required
def post_view(request, user):
    comments = Comment.objects.filter(post__user__username=user)
    threshold_weekly = datetime.datetime.now() - datetime.timedelta(weeks=1)
    threshold_hour = datetime.datetime.now() - datetime.timedelta(hours=1)

    dict = {'all': Comment.objects.filter(post__user__username=user),
            'weekly': Comment.objects.filter(time_in__gt=threshold_weekly, post__user__username=user),
            'daily': Comment.objects.filter(time_in__gt=threshold_hour, post__user__username=user),
            'test_choice': Comment.objects.filter(pk=2),
            }

    if request.method == 'POST':
        form = CommentsForm(request.POST)
    else:
        form = CommentsForm()

    if request.POST.get('time_period'):
        comments = dict[request.POST['time_period']]
    print(comments)
    viewer = request.user
    variables = {'comments': comments, 'form': form, 'viewer': viewer}
    return render(request, 'post_personal.html', context=variables)


class CommentDelete(DeleteView, PermissionRequiredMixin):
    model = Comment
    queryset = Comment.objects.all()
    template_name = 'comment_delete.html'
    context_object_name = 'comment'
    permission_required = 'board.delete_comment'

    def get_success_url(self):
        user = self.get_object().post.user
        return reverse('post_personal', kwargs={'user': user})


def comment_accept(request, **kwargs):
    comment_ = Comment.objects.get(pk=kwargs['pk'])
    context = {'comment': comment_}
    notify_request_accept(comment=comment_)
    return render(request, template_name='comment_accept.html', context=context)


def test_news_mail(request):
    emails = User.objects.all().values_list('email', flat=True)
    threshold = datetime.datetime.now() - datetime.timedelta(weeks=1)
    news = Post.objects.filter(time_in__gt=threshold)
    subject = 'Weekly news from Best MMORPG Fun site'
    body = ''
    context = {"news": news, 'request': request.get_host}
    return render(request, template_name='news_email.html', context=context)
