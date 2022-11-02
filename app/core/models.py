from django.db import models
import os
from django.conf import settings
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



def get_anonymous_user():
    return get_user_model().objects.get_or_create(email='nouser@example.com', first_name='Anonymous')

def _image_upload_helper(filename):

    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return filename

def user_image_path(instance, filename):

    filename = _image_upload_helper(filename)
    return os.path.join('profile_pics', instance.id, filename)

def blog_image_path(instance, filename):
    """Generating file path for a updated image"""
    filename = _image_upload_helper(filename)
    return os.path.join('uploads',instance.slug,  filename)


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, first_name, password=None, **kwargs):
        """Create user """
        if not email:
            raise ValueError("[-] Kindly provide an email address for registration [-]")
        if not first_name:
            raise ValueError("[-] User should have a first name [-]")

        user = self.model(email=self.normalize_email(email), first_name=first_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, **kwargs):
        """Create a superuser"""
        user = self.create_user(email, first_name, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        """Get user full name"""
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """Get short name for user"""
        return self.first_name

    def __str__(self):
        """Get string representation for the object"""
        return self.first_name + " " + self.last_name



class Tag(models.Model):

    caption = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):

        return self.caption


class UserComment(models.Model):
    """User comments on the posts"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_anonymous_user))
    content = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    root_comment = GenericRelation("self", null=True, blank=True)

    updated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20] + "..."

    def get_replies(self):
        """Get all the replies to the comment"""
        return UserComment.objects.filter(root_comment=self)

    @property
    def is_reply(self):
        """To check if comment is a reply to other comment"""
        if self.root_comment is not None:
            return True
        return False



class Blog(models.Model):
    """Model for Blog data"""
    image = models.ImageField(null=True, upload_to=blog_image_path)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = GenericRelation(UserComment, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    slug = models.SlugField(unique=True)
    created_on = models.DateTimeField(auto_now=True)
    updated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        
        try:
            q = Blog.objects.latest('id').id
        except:
            q = 0
        if not self.updated:
            slug = slugify(self.title)
            self.slug = slug + '_' + str(q +1)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """Detailed model for user profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, upload_to=user_image_path)
    about = models.TextField(null=True)
    GENDER_CHOICE = (('M','Male'), ('F','Female'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=None, null=True)

    def __str__(self):

        return self.user.email
    @property
    def get_user_blogs(self):
        """Get all teh blogs for a user"""
        #user_blog = self.user.blog_set.values_list('title')
        user_blog = self.user.blog_set.values()
        return user_blog
    @property
    def get_user_tags(self):
        """Get all the tags for user"""
        #user_tags = self.user.tag_set.values_list('caption')
        user_tags = self.user.tag_set.values()
        return user_tags
