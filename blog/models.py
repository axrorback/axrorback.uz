from django.db import models
from django.conf import settings  # ✅ eng to‘g‘ri yo‘l shu

# 📌 Blog Post modeli
class Post(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="Sarlavha"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug (URL nomi)"
    )
    content = models.TextField(
        verbose_name="Maqola matni"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqt"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqt"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Muallif"
    )
    image = models.ImageField(
        upload_to='media/blog',
        null=True,
        blank=True,
        verbose_name="Rasm"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ['-created']  # 🕒 eng oxirgi yaratilganlar birinchi chiqadi


class Question(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Ism"
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name="Telefon raqami"
    )
    question = models.TextField(
        max_length=200,
        verbose_name="Savol matni"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqt"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answered_questions',
        verbose_name="Javob bergan admin",
        null=True,
        blank=True
    )
    answer_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Javob berilgan vaqt"
    )
    answer = models.TextField(
        null=True,
        blank=True,
        verbose_name="Javob matni"
    )

    def masked_phone(self):
        """Telefon raqamni qisman yashirib ko‘rsatish."""
        if len(self.phone_number) >= 4:
            return self.phone_number[:-4].replace(
                self.phone_number[:-4], "*" * (len(self.phone_number) - 4)
            ) + self.phone_number[-4:]
        return self.phone_number

    masked_phone.short_description = "Yashirilgan raqam"

    def __str__(self):
        return f"{self.name} ({self.masked_phone()})"

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ['-created']


class Certificate(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Sertifikat nomi"
    )
    file = models.FileField(
        upload_to='certificates/',
        verbose_name="Fayl (rasm yoki PDF)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yuklangan sana"
    )

    def is_image(self):
        return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))

    def is_pdf(self):
        return self.file.name.lower().endswith('.pdf')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        ordering = ['-created_at']


class AdminLog(models.Model):
    LEVELS = (
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    )
    level = models.CharField(max_length=10, choices=LEVELS)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level}: {self.message[:50]}"