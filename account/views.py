from django.shortcuts import render, get_object_or_404, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post, Comment, Category, Ticket
from blog.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('登录成功')
                else:
                    return HttpResponse('该账户不存在')
        else:
            return HttpResponse('非法登录')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request, category_slug=None):
    object_list = Post.published.all()
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(status='published')
    paginator = Paginator(object_list, 6)  # 每一页显示六个
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果第一页不是正整数
        posts = paginator.page(1)
    except EmptyPage:
        # 如果 超出页码返回最后一页
        posts = paginator.page(paginator.num_pages)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category)

    total_posts = Post.published.count()

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'category': category,
                   'categories': categories,
                   'total_posts': total_posts,
                   })


def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


# 个人中心
@login_required
def myinfo(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    profile = get_object_or_404(Profile,
                                user=request.user,
                                )
    print(profile.image)

    return render(request,
                  'account/myinfo.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'profile': profile
                   })


# 用户列表

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    profile = Profile.objects.filter()
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users,
                   'porfile': profile
                   })


# 用户互相关注
@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


# 获取我所评论过的文章
@login_required
def Mycollection(request):

    profile = Profile.objects.get(user=request.user)
    ticket = Ticket.Ticket_manage.filter(voter=request.user)
    print(ticket)
    posts = Post.published.filter()
    print(posts)
    #posts = Post.objects.filter(title=category.video, status='published')
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

    return render(request,
                  'blog/post/mycollection.html',
                  {
                      'posts': ticket,
                      'profile': profile,
                      'page': page,

                  })
