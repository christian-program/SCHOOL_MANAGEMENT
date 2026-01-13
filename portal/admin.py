from django.contrib import admin
from .models import Department, Post, Comment, StudentResult, Promotion

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'author', 'created_at')
    list_filter = ('post_type', 'created_at')

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_id', 'promotion')
    search_fields = ('student_id', 'student_name')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department',)

admin.site.register(Comment)