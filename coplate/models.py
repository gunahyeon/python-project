from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .validators import validate_no_special_characters, validate_restaurant_link


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )

    profile_pic = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')

    intro = models.CharField(max_length=60, blank=True)


    following =models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True,
        related_name='followers'
    )

    kakao_id = models.CharField(
        max_length=50,
        null = True
    )
    # 역관계 이름 리네임 : realated_name user_set -> follwers
    # sysmmetrical : ex)친구를 맺으면 너랑나랑은 친구, 하지만 팔로우는 비대칭 관계로 너랑나랑팔로우는 아니기 때문ㅇ
    # symmetrical=False
    # 다대다, 1대1 관계는 맺을 때 self로 맺어도 된다. 
    # 다대다는 null 옵션이 없다. 

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )

    profile_pic = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')

    intro = models.CharField(max_length=60, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.CharField(max_length=30)

    restaurant_name = models.CharField(max_length=20)

    restaurant_link = models.URLField(validators=[validate_restaurant_link])

    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)

    image1 = models.ImageField(upload_to='review_pics')

    image2 = models.ImageField(upload_to='review_pics', blank=True)

    image3 = models.ImageField(upload_to='review_pics', blank=True)

    content = models.TextField()

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    # genericForiegnKey는 역관계 형성을 직접해줘야한다. 역관계 형성하면 자동으로 CASCADE도 생긴다. 
    likes = GenericRelation('Like', related_query_name='review')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-dt_created']

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_modified = models.DateTimeField(auto_now=True)

    # 특정 유저가 작성한 댓글들
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # 특정 리뷰에 달려있는 댓글들
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    likes = GenericRelation('Like', related_query_name='comment')

    def __str__(self):
        return self.content[:30]

    class Meta:
        ordering = ['-dt_created']

class Like(models.Model):
    dt_created = models.DateField(auto_now_add=True)

    # 특정 유저가 좋아요한 컨텐츠
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()
    
    liked_object = GenericForeignKey()

    def __str__(self):
        return f"(${self.user},${self.liked_object})"
    # on_delete 속성으로 삭제할 수 없다. 다수의 모델을 참조하기 때문에.
    # content_type , object_id 만들어주면, 오브젝트는 자동으로 생성된다. genericKey안에 파라미터 생략해도 된다. 
    # liked_object = GenericForeignKey('content_type','object_id')
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']