# Axrorback.uz — Shaxsiy Portfoliyo va Veb-sayt

Ushbu loyiha **axrorback.dev** shaxsiy portfoliyo saytining manba kodi hisoblanadi. Loyiha orqali foydalanuvchilar muallifning qilgan ishlari, tajribasi va texnologik bilimlari bilan tanishishlari mumkin.

---

## 🌟 Asosiy Xususiyatlar

* **Dinamik Portfolio:** Admin panel orqali loyihalarni qo'shish, tahrirlash va o'chirish.
* **Blog Tizimi:** IT va dasturlashga oid maqolalar chop etish imkoniyati.
* **Aloqa Formasi:** Sayt tashrif buyuruvchilari tomonidan yuborilgan xabarlarni qabul qilish.
* **Responsive Dizayn:** Har qanday qurilmada (Desktop, Planchet, Mobil) mukammal ko'rinish.
* **SEO Optimallashgan:** Qidiruv tizimlari uchun moslashtirilgan meta-teglar va toza kod.

---

## 🛠 Texnologik Stek

### Backend:
* **Python:** Asosiy dasturlash tili.
* **Django Framework:** Kuchli va xavfsiz backend tizimi.
* **SQLite / PostgreSQL:** Ma'lumotlarni saqlash uchun bazalar.

### Frontend:
* **Django Templates:** Dinamik kontentni chiqarish uchun.
* **HTML5 & CSS3:** Saytning tuzilishi va ko'rinishi.
* **JavaScript:** Interaktiv elementlar uchun.

---

## ⚙️ Mahalliy muhitda sozlash (Local Setup)

Loyihani o'z kompyuteringizda ishga tushirish uchun quyidagi ketma-ketlikni bajaring:

1.  **Repozitoriyani nusxalash:**
    ```bash
    git clone [https://github.com/axrorback/axrorback.uz.git](https://github.com/axrorback/axrorback.uz.git)
    cd axrorback.uz
    ```

2.  **Virtual muhitni sozlash:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/MacOS:
    source venv/bin/activate
    ```

3.  **Kutubxonalarni o'rnatish:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ma'lumotlar bazasini tayyorlash:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Admin foydalanuvchi yaratish:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Serverni ishga tushirish:**
    ```bash
    python manage.py runserver
    ```

Brauzerda `http://127.0.0.1:8000/` manzilini oching.

---

Asosiy sayt: https://axrorback.dev
