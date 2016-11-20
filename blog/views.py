from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category, Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, TicketForm
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


# 列表页
@login_required
def post_list(request, category_slug=None, ):
    object_list = Post.published.all()
    posts = Post.published.all()
    category = None
    categories = Category.objects.all()
    paginator = Paginator(object_list, 3)  # 每一页显示3个
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果第一页不是正整数
        posts = paginator.page(1)
    except EmptyPage:
        # 如果 超出页码返回最后一页
        posts = paginator.page(paginator.num_pages)
    except:
        pass
    # 文章包含分类
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category, status='published')
        paginator = Paginator(posts, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # 如果第一页不是正整数
            posts = paginator.page(1)
        except EmptyPage:
            # 如果 超出页码返回最后一页
            posts = paginator.page(paginator.num_pages)
        except:
            pass
    total_posts = Post.published.count()

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'category': category,
                   'categories': categories,
                   'total_posts': total_posts,

                   })


# 列表页管理器
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6  # y每页有几个
    template_name = 'blog/post/list.html'


# 详情页
def post_detail(request, id, slug):
    context = {}
    post = get_object_or_404(Post, id=id,
                             slug=slug, status='published', )
    context['post'] = post
    # 获取相似标签文章
    category = None
    categories = Category.objects.all()
    category = post.category
    similar_posts = Post.objects.filter(category=category)[:4]
    # 获取文章中评论
    comments = post.comments.filter(active=True)
    # 投票
    try:
        user_ticket_for_post = Ticket.objects.get(voter_id=request.user.id, video_id=post.id)
        print(user_ticket_for_post.choice)
        context['user_ticket_for_post'] = user_ticket_for_post
    except:
        pass

    if request.method == 'POST':
        # 如果评论被发表
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 创建
            new_comment = comment_form.save(commit=False)
            # 分配POST
            new_comment.post = post
            # 存档
            new_comment.save()
    else:
        comment_form = CommentForm()
    context['comments'] = comments
    context['comment_form'] = comment_form
    context['similar_posts'] = similar_posts
    return render(request,
                  'blog/post/detail.html',
                  context)


# 投票
@login_required
def detai_vote(request, id, slug):
    try:
        # 盖头
        user_ticket_for_this_post = Ticket.objects.get(voter_id=request.user.id, video_id=id)
        print(user_ticket_for_this_post)
        user_ticket_for_this_post.choice = request.POST['choice']
        print(user_ticket_for_this_post.choice)
        user_ticket_for_this_post.save()

    except ObjectDoesNotExist:  # 第一次投票
        user_ticket_for_this_post = Ticket(voter_id=request.user.id, video_id=id, choice=request.POST['choice'])
        user_ticket_for_this_post.save()
    except:
        pass
    return HttpResponseRedirect(reverse('blog:post_detail', args=(id, slug)))


# 邮件分享
def post_share(request, post_id):
    # 通过ID获取分享文章
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    form = EmailPostForm(request.POST)
    if request.method == 'POST':
        #  submitted
        if form.is_valid():
            # 通过验证
            cd = form.cleaned_data
            # 发邮件
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'luoying1105@yeah.net', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})




