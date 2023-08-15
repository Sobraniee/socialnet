from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    subscribers = models.ManyToManyField(to=User, related_name='subscriber_user', blank=True)


class Post(models.Model):
    STATUS_CHOICES = (
        ('Опубликован', 'Опубликован'),
        ('Неопубликован', 'Неопубликован')
    )

    name = models.CharField('Наименование поста', max_length=80, null=True, blank=True)
    description = models.TextField('Описание', null=True)
    photo = models.ImageField('Фотография', upload_to='photo_post/', null=True, blank=True)
    status = models.CharField('Статус публикации', max_length=200, choices=STATUS_CHOICES, default='Опубликован')
    likes = models.IntegerField('Лайк', default=0)
    # many two one
    creator = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True, # необязательно в БД
        blank=False, # обязательно в джанго
        verbose_name='Автор поста',
        related_name='posts' # default == post_set
    )
    def __str__(self):
        return f"{self.name} - {self.status}"

    category = models.ManyToManyField(
        to='Category',
        blank=True,
        verbose_name='Категори'

    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.name} - {self.status}'

class Category(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )
    name = models.CharField('Наименование столба', max_length=50, null=True, blank=True)
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} - {self.rating}'

class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    comment_text = models.TextField()
    likes_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.comment_text[:20]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
        ordering = ['created_at']

class Short(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Автор',
        related_name='Short'
    )
    video = models.FileField('Видео', upload_to='video_post/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views_qty = models.PositiveIntegerField('Просмотры', default=0)


    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f'{self.video} - {self.created_at}'

class SavedPosts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post, verbose_name='saved post', related_name='saved_posts')

    class Meta:
        verbose_name = 'saved post'
        verbose_name_plural = 'saved posts'

    def __str__(self):
        return f'{self.user} - {self.post}'




