from django.db import models
from django.contrib.auth.models import User
from user_newsdatabase.resources import TYPES

class Author(models.Model):
    rate = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rate = 0
        posts_list = Author.objects.filter(id=self.id).values('post__rate') # [{key:value},{key:value}]
        your_comments_list = Comment.objects.filter(user_id=self.user_id).values('rate')
        for_you_comments_list = Post.objects.filter(author_id=self.id).values('comment__rate')

        comments_sum = list(your_comments_list) + list(for_you_comments_list)
        posts_sum = [int(*i.values())*3 for i in posts_list]
        comments_sum = [int(*i.values()) for i in comments_sum]
        for i in posts_sum + comments_sum:
            self.rate = self.rate + i
        self.save()

        return f'{self.rate}'


class Category(models.Model):
    name = models.TextField(unique=True)


class Post(models.Model):
    type = models.CharField(max_length=64, choices=TYPES, default='article')
    data_time = models.DateTimeField(auto_now_add=True)
    title = models.TextField(unique=True)
    text = models.TextField()
    rate = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rate = self.rate + 1
        self.save()

    def dislike(self):
        self.rate = self.rate - 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    data_time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate = self.rate + 1
        self.save()

    def dislike(self):
        self.rate = self.rate - 1
        self.save()