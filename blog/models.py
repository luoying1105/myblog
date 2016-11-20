from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


# 文章管理
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category',
                       args=[self.slug])


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    # 分类
    Tag_CHOICES = (
        ('company', '大公司日报'),
        ('design', '设计日报'),
    )
    category = models.ForeignKey(Category,
                                 related_name='article')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    image = models.ImageField('图片', upload_to='blog/%Y/%m/%d', blank=True)
    objects = models.Manager()
    published = PublishedManager()
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')
    tag = models.CharField(max_length=10,
                           choices=Tag_CHOICES,
                           default='company')
    description = models.TextField(blank=True)



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    """
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])"""

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.id, self.slug])


# 登录人档案
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=250)
    image = models.ImageField('图片', upload_to='user/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.ForeignKey(User, related_name='comment_posts')
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

    # 投票管理
class TicketManager(models.Manager):
        def get_queryset(self):
            return super(TicketManager, self).get_queryset().filter(choice='like')


#投票
class Ticket(models.Model):
    voter = models.ForeignKey(User, related_name='vote_tickets')#投票人
    video = models.ForeignKey(Post,related_name='ticket')
    VOTE_CHOICE= (
        ('like', '点赞'),
        ('dislike', '差评'),
        ('nomarl', '朕知道了'),
    )
    choice = models.CharField(max_length=10,
                           choices=VOTE_CHOICE,
                           default='nomarl')
    Ticket_manage = TicketManager()

    def __str__(self):
        return  str(self.id)

    def __unicode__(self):
        return self.voter
