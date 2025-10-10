from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.text import slugify
from .models import Post, Question, Certificate, AdminLog


# 📌 Post modeli uchun admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')  # ko‘rinadigan ustunlar
    list_filter = ('created', 'author')                       # yon tarafda filterlar
    search_fields = ('title', 'content')                      # qidiruv
    prepopulated_fields = {'slug': ('title',)}                # slug avtomatik to‘ldiriladi
    ordering = ('-created',)

    # Agar title o'zgarsa slugni avtomatik qayta yozish
    def save_model(self, request, obj, form, change):
        if not obj.slug or change:  # slug bo‘sh yoki post o‘zgartirilsa
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created', 'is_active')
    list_filter = ('is_active', 'created')
    search_fields = ('name', 'phone_number', 'question')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)



@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('level', 'message', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)  # shu yerda correct field name