# Money Tracker API

Money Tracker API - bu kirim-chiqimlarni boshqarish uchun Django Rest Framework asosida qurilgan RESTful API.

## Xususiyatlar

- ✅ **Authentication**: JWT (Simple JWT) autentifikatsiya
- ✅ **User Management**: Ro'yxatdan o'tish, profil boshqaruvi, parol o'zgartirish
- ✅ **Cards/Accounts**: Naqd pul, plastik kartalar va bank hisoblarini boshqarish
- ✅ **Transactions**: Kirim va chiqim tranzaksiyalarini boshqarish
- ✅ **Categories**: Tranzaksiya kategoriyalarini boshqarish
- ✅ **Multi-Currency**: UZS, USD, EUR, RUB valyutalarini qo'llab-quvvatlash
- ✅ **Statistics**: Kirim-chiqim statistikasi va hisobotlar
- ✅ **Swagger/OpenAPI**: To'liq API dokumentatsiyasi
- ✅ **Filtering & Search**: Kuchli filtrlash va qidiruv imkoniyatlari

## Texnologiyalar

- Python 3.10+
- Django 5.0.1
- Django REST Framework 3.14.0
- Simple JWT 5.3.1
- drf-yasg (Swagger/OpenAPI)
- SQLite (development)

## O'rnatish

### 1. Repository ni clone qiling

```bash
git clone <repository_url>
cd money_tracker_api
```

### 2. Virtual environment yarating

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Dependencies ni o'rnating

```bash
pip install -r requirements.txt
```

### 4. Migratsiyalarni bajaring

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superuser yarating

```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushiring

```bash
python manage.py runserver
```

Server `http://127.0.0.1:8000/` da ishga tushadi.

## 👥 Test Userlar

Loyihada allaqachon 4 ta test user yaratilgan va to'liq ma'lumotlar bilan to'ldirilgan:

| # | Ism | Username | Email | Telefon | Parol |
|---|-----|----------|-------|---------|-------|
| 1 | Ali Karimov | `ali_karimov` | ali.karimov@example.uz | +998901234567 | `TestPass123!` |
| 2 | Madina Rashidova | `madina_rashidova` | madina.rashidova@example.uz | +998907654321 | `TestPass123!` |
| 3 | Sardor Aliyev | `sardor_aliyev` | sardor.aliyev@example.uz | +998909876543 | `TestPass123!` |
| 4 | Dilnoza Yusupova | `dilnoza_yusupova` | dilnoza.yusupova@example.uz | +998905555555 | `TestPass123!` |

**Barcha test userlar uchun parol:** `TestPass123!`

### Test ma'lumotlar

Har bir test user quyidagilarga ega:
- ✅ To'liq profil (telefon, manzil, bio)
- ✅ 3 ta karta (turli valyutalarda: UZS, USD, EUR)
- ✅ 13 ta kategoriya (5 ta daromad, 8 ta xarajat)
- ✅ 40-60 ta tranzaksiya (so'ngi 60 kun uchun)

Ushbu test userlar orqali darhol API ni sinab ko'rishingiz mumkin!

## API Dokumentatsiya

API dokumentatsiyasini quyidagi manzillarda ko'rishingiz mumkin:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Django Admin**: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication

- `POST /api/accounts/register/` - Ro'yxatdan o'tish
- `POST /api/accounts/login/` - Login (JWT token olish)
- `POST /api/accounts/token/refresh/` - Token yangilash
- `GET /api/accounts/profile/` - Profil ma'lumoti
- `PUT /api/accounts/profile/update/` - Profil yangilash
- `POST /api/accounts/change-password/` - Parol o'zgartirish

### Cards

- `GET /api/cards/` - Barcha kartalar
- `POST /api/cards/` - Yangi karta yaratish
- `GET /api/cards/{id}/` - Bitta kartani ko'rish
- `PUT/PATCH /api/cards/{id}/` - Kartani yangilash
- `DELETE /api/cards/{id}/` - Kartani o'chirish
- `GET /api/cards/{id}/stats/` - Karta statistikasi

### Transactions

- `GET /api/transactions/` - Barcha tranzaksiyalar
- `POST /api/transactions/` - Yangi tranzaksiya yaratish
- `GET /api/transactions/{id}/` - Bitta tranzaksiyani ko'rish
- `PUT/PATCH /api/transactions/{id}/` - Tranzaksiyani yangilash
- `DELETE /api/transactions/{id}/` - Tranzaksiyani o'chirish
- `GET /api/transactions/stats/` - Umumiy statistika

### Categories

- `GET /api/transactions/categories/` - Barcha kategoriyalar
- `POST /api/transactions/categories/` - Yangi kategoriya yaratish
- `GET /api/transactions/categories/{id}/` - Bitta kategoriyani ko'rish
- `PUT/PATCH /api/transactions/categories/{id}/` - Kategoriyani yangilash
- `DELETE /api/transactions/categories/{id}/` - Kategoriyani o'chirish
- `GET /api/transactions/categories/stats/` - Kategoriya statistikasi

## Foydalanish Misollari

### 1. Ro'yxatdan o'tish

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ali_karimov",
    "password": "TestPass123!"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Karta yaratish

```bash
curl -X POST http://127.0.0.1:8000/api/cards/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Uzcard",
    "card_type": "debit",
    "currency": "UZS",
    "balance": 1000000,
    "bank_name": "Xalq Bank",
    "color": "#3498db"
  }'
```

### 4. Tranzaksiya yaratish

```bash
curl -X POST http://127.0.0.1:8000/api/transactions/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "expense",
    "amount": 50000,
    "currency": "UZS",
    "category": 1,
    "card": 1,
    "description": "Supermarket xarid",
    "date": "2025-01-19T10:30:00Z"
  }'
```

### 5. Statistika olish

```bash
curl -X GET "http://127.0.0.1:8000/api/transactions/stats/?currency=UZS" \
  -H "Authorization: Bearer <access_token>"
```

## Filtrlash va Qidiruv

### Cards

```bash
# Card type bo'yicha filtrlash
GET /api/cards/?card_type=debit

# Valyuta bo'yicha filtrlash
GET /api/cards/?currency=USD

# Faol kartalar
GET /api/cards/?is_active=true

# Qidirish (name, bank_name, card_number)
GET /api/cards/?search=uzcard

# Tartiblash
GET /api/cards/?ordering=-balance
```

### Transactions

```bash
# Transaction type bo'yicha
GET /api/transactions/?transaction_type=income

# Valyuta bo'yicha
GET /api/transactions/?currency=USD

# Kategoriya bo'yicha
GET /api/transactions/?category=1

# Karta bo'yicha
GET /api/transactions/?card=1

# Sana oralig'i
GET /api/transactions/?date_from=2025-01-01&date_to=2025-01-31

# Qidirish (description)
GET /api/transactions/?search=supermarket

# Tartiblash
GET /api/transactions/?ordering=-amount
```

## Model Strukturasi

### User & Profile

- Standart Django User modeli
- Profile modeli: phone, birth_date, address, bio, avatar

### Card

- name, card_type, currency, card_number
- balance, credit_limit, bank_name, color
- is_active, description

### Category

- name, transaction_type, icon, color
- User yaratilganda avtomatik default kategoriyalar yaratiladi

### Transaction

- transaction_type, amount, currency
- category, card, description, date
- Tranzaksiya yaratilganda/o'chirilganda karta balansi avtomatik yangilanadi

## Xavfsizlik

- JWT token autentifikatsiya
- Password validation
- CORS sozlamalari
- User-specific data filtration (har bir user faqat o'z ma'lumotlarini ko'radi)

## Development

### Test yaratish

```bash
python manage.py test
```

### Yangi migratsiya yaratish

```bash
python manage.py makemigrations
python manage.py migrate
```

### Static fayllarni to'plash

```bash
python manage.py collectstatic
```

## Production

Production muhitda quyidagilarni o'zgartiring:

1. `settings.py` da `DEBUG = False`
2. `SECRET_KEY` ni muhofaza qiling
3. `ALLOWED_HOSTS` ni to'g'ri sozlang
4. PostgreSQL yoki MySQL dan foydalaning
5. Gunicorn yoki uWSGI server ishlatilsin
6. Nginx yoki Apache reverse proxy o'rnating
7. HTTPS ishlatilsin
8. CORS sozlamalarini cheklang

## Murojaat

Savollar yoki muammolar bo'lsa, issue ochishingiz mumkin.

## Litsenziya

MIT License