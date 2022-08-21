from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Post(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(User,blank=True , related_name='likes')
    savers = models.ManyToManyField(User,blank=True , related_name='saved')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        self.name = value

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }
    
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"

class PublicChatRoom(models.Model):
    title=models.CharField(max_length=255, unique=True, blank=False,)
    users=models.ManyToManyField(settings.AUTH_USER_MODEL, help_text="Users connected to chat") 

    def __str__(self):
        return self.title 
        
@property
def group_name(self):
    return f"PublicChatRoom: {self.id} "

class PublicChatManager(models.Manager):
    def by_room(self, room):
        qs=PublicChat.objects.filter(room=room).order_by("-timestamp")
        return qs 


class PublicChat(models.Model):
       user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE  )
       room=models.ForeignKey(PublicChatRoom   ,on_delete=models.CASCADE  )
       timestamp=models.DateTimeField(auto_now_add=True)
       content= models.TextField(unique=False, blank=False)

       objects=PublicChatManager()

def  __str__(self):
    return self.content  