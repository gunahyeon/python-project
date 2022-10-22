from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, Review, Comment, Like

# admin review page 에서 댓글을 추가.
class CommentInline(admin.StackedInline):
    model = Comment

# 제네릭은 제네릭으로 받아야함.
class LikeInline(GenericStackedInline):
    model = Like

class UserInline(admin.StackedInline):
    model = User.following.through # 다대다관계
    fk_name = 'to_user' # from_model, to_model : 만약 셀프관계가 아니라면 명시하지 않아도 된다.
    verbose_name = "Follower" # admin page
    verbose_name_plural = 'Followers' # admin page

UserAdmin.fieldsets += ('Custom fields', {'fields': ('nickname', 'profile_pic', 'intro', 'following',),}),
UserAdmin.inlines = (UserInline,)
# inline 상속, reviewAdmin 커스텀마이징
class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        LikeInline,
    ]

class CommentAdmin(admin.ModelAdmin):
    inlines = [
        LikeInline,
    ]

admin.site.register(User, UserAdmin)

# 커스텀마이징한 비교대상 리뷰어드민 추가
admin.site.register(Review, ReviewAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Like)
