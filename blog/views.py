import os

from django.http import HttpResponseForbidden ,FileResponse,Http404
from django.shortcuts import render, redirect
import requests
from .forms import QuestionForm
from .models import *


ALLOWED_DOMAINS = ['axrorback.uz', 'www.axrorback.uz','127.0.0.1:8000']

def protected_media(request, path):
    """
    Faol referrer tekshirish: faqat bizning domenimizdan kelgan so‘rovga rasm ko‘rsatiladi.
    MEDIA_ROOT va STATIC_ROOT fayllarini tekshiradi.
    """
    referer = request.META.get('HTTP_REFERER', '')
    if not any(domain in referer for domain in ALLOWED_DOMAINS):
        return HttpResponseForbidden(
            "Rasmlarimni URLni olganiz bilan boshqa yerda ishlata olmaysiz. "
            "Hotlinking faqat domenimizdan so‘rov borsagina rasm URL ishlaydi."
        )

    # MEDIA_ROOT ichida tekshirish
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, 'rb'))

    #  Agar MEDIA_ROOT da topilmasa, STATIC_ROOT ichida tekshirish
    full_path = os.path.join(settings.STATIC_ROOT, path)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, 'rb'))

    # Agar topilmasa
    raise Http404()

def thanks(request):
    return render(request, 'blog/thanks.html')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')


def blog(request):
    blogs = Post.objects.all()
    return render(request, 'blog/blogs.html', {'blogs': blogs})

def achievements(request):
    certificates = Certificate.objects.all().order_by('-created_at')
    # har bir sertifikat uchun to‘liq URL yasaymiz
    for c in certificates:
        c.full_url = request.build_absolute_uri(c.file.url)
    return render(request, 'blog/achievements.html', {'certificates': certificates})



def blog_detail(request, slug):
    blog = Post.objects.get(slug=slug)
    return render(request, 'blog/blog_detail.html', {'blog': blog})


def questions_list(request):
    questions = Question.objects.filter(is_active=True)
    return render(request, 'blog/questions_list.html', {'questions': questions})

def send_telegram_message(text):
    """Bot orqali kanalga xabar yuborish"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHANNEL_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",  # agar <b>bold</b> ishlatmoqchi bo‘lsangiz
    }
    requests.post(url, data=data)


def ask_question(request):
    questions = Question.objects.filter(is_active=True).order_by('-created')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()

            # Telegramga yuborish
            text = (
                f"📌 <b>Yangi Savol</b>\n"
                f"Ism: {question.name}\n"
                f"Telefon: {question.masked_phone()}\n"
                f"Savol: {question.question}\n"
            )
            send_telegram_message(text)

            return redirect('ask_question')
    else:
        form = QuestionForm()
    return render(request, 'blog/ask_question.html', {
        'form': form,
        'questions': questions
    })