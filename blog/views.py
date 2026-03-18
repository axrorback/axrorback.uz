import json
import os
from django.http import HttpResponseForbidden, FileResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils._os import safe_join
from .forms import QuestionForm
from .models import *
from django.core.cache import cache
from django.conf import settings
from urllib.parse import urlparse

ALLOWED_DOMAINS = settings.ALLOWED_HOSTS

def protected_media(request, path):
    referer = request.META.get("HTTP_REFERER")
    if referer:
        try:
            referer_host = urlparse(referer).hostname
        except Exception:
            return HttpResponseForbidden("Invalid referer")

        if referer_host not in ALLOWED_DOMAINS:
            return HttpResponseForbidden("Hotlink forbidden")

    try:
        media_path = safe_join(settings.MEDIA_ROOT, path)
    except Exception:
        return HttpResponseForbidden("Invalid path")

    if os.path.exists(media_path):
        return FileResponse(open(media_path, "rb"))

    try:
        static_path = safe_join(settings.STATIC_ROOT, path)
    except Exception:
        return HttpResponseForbidden("Invalid path")

    if os.path.exists(static_path):
        return FileResponse(open(static_path, "rb"))

    raise Http404()

def secure_certificate_view(request, pk, expire, token):
    cert = get_object_or_404(Certificate, pk=pk)

    # Hozirgi vaqt
    now = int(time.time())

    # Muddati tugaganini tekshirish
    if now > int(expire):
        return render(request, "blog/error_expired.html", {
            "cert": cert,
            "message": "Havola muddati tugagan.",
            "expired_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(expire))),
        }, status=403)

    # Tokenni tekshirish
    expected = hashlib.sha256(f"{cert.pk}:{expire}:{settings.SECRET_KEY}".encode()).hexdigest()
    if token != expected:
        return render(request, "blog/error_invalid.html", {
            "cert": cert,
            "message": "Noto‘g‘ri yoki buzilgan token.",
        }, status=403)

    # Qolgan vaqtni hisoblash
    remaining = int(expire) - now

    return render(request, "blog/certificate_view.html", {
        "cert": cert,
        "remaining": remaining
    })





def thanks(request):
    if not request.session.get('question_id', None):
        return redirect('ask_question')
    return render(request, 'blog/thanks.html')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def donate(request):
    return render(request, 'blog/donate.html')


def blog(request):
    blogs = Post.objects.all()
    return render(request, 'blog/blogs.html', {'blogs': blogs})

def achievements(request):
    certificates = Certificate.objects.all().order_by('-created_at')

    # Har bir sertifikat uchun 30 daqiqalik xavfsiz tokenli URL yasaymiz
    for c in certificates:
        secure_link = c.get_secure_url(expires_in_minutes=30)
        c.full_url = request.build_absolute_uri(secure_link)

    return render(request, 'blog/achievements.html', {
        'certificates': certificates
    })


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
            request.session['question_id'] = question.id
            return redirect('thanks')
    else:
        form = QuestionForm()
    return render(request, 'blog/ask_question.html', {
        'form': form,
        'questions': questions
    })