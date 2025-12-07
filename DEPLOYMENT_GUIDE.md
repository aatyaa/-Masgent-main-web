# 🚀 دليل النشر - للدكتور

## الطريقة 1: نشر على الشبكة المحلية (الأسهل)

### الخطوات:

#### 1. شغّل التطبيق على السيرفر
```bash
cd /storage/home/sii5085/work/webApp/Masgent-main
streamlit run web_app/app.py --server.address 0.0.0.0 --server.port 8501
```

#### 2. اعرف IP Address السيرفر
```bash
hostname -I
```
مثال: `192.168.1.100`

#### 3. الدكتور يفتح من لابتوبه
```
http://192.168.1.100:8501
```

**ملحوظة:** لازم اللابتوب والسيرفر على نفس الشبكة (WiFi/LAN)

---

## الطريقة 2: نشر على الإنترنت (Streamlit Cloud)

### الخطوات:

#### 1. رفع الكود على GitHub
```bash
cd /storage/home/sii5085/work/webApp/Masgent-main
git init
git add .
git commit -m "Masgent Web App"
git remote add origin https://github.com/YOUR_USERNAME/masgent-web.git
git push -u origin main
```

#### 2. نشر على Streamlit Cloud
1. روح على: https://share.streamlit.io
2. سجل دخول بـ GitHub
3. اضغط "New app"
4. اختر الـ repository
5. Main file: `web_app/app.py`
6. اضغط "Deploy"

#### 3. شارك الرابط مع الدكتور
```
https://your-app-name.streamlit.app
```

---

## الطريقة 3: نشر محلي مع Ngrok (للتجربة السريعة)

### الخطوات:

#### 1. ثبت Ngrok
```bash
# Download ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
```

#### 2. شغّل التطبيق
```bash
streamlit run web_app/app.py
```

#### 3. في terminal تاني، شغّل ngrok
```bash
./ngrok http 8501
```

#### 4. انسخ الرابط العام
```
Forwarding: https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

#### 5. ابعت الرابط للدكتور
الدكتور يقدر يفتحه من أي مكان!

---

## 📦 ملف للدكتور (للتثبيت على جهازه)

### إذا الدكتور عايز يثبته على جهازه:

#### 1. أعطيه المجلد كله
```bash
# اعمل zip للمشروع
cd /storage/home/sii5085/work/webApp
zip -r Masgent-Web.zip Masgent-main/
```

#### 2. الدكتور يعمل:
```bash
# فك الضغط
unzip Masgent-Web.zip
cd Masgent-main

# ثبت المكتبات
pip install -r requirements_web.txt
python install_deps.py

# شغّل التطبيق
streamlit run web_app/app.py
```

---

## 🔑 API Keys للدكتور

### أعطيه الـ Keys دي:

**Gemini API Key:**
```
AIzaSyBNdYToSvrloTlNu1SgjD2kwIsx7DZ-3B4
```

**Materials Project API Key:**
```
UG6QzjRKyF5GVXa8gwK40TgKztH3neFD
```

**أو يعمل keys خاصة به:**
- Gemini: https://aistudio.google.com/app/apikey
- MP: https://next-gen.materialsproject.org/api

---

## 📝 تعليمات للدكتور

### ملف نصي بسيط:

```
مرحباً دكتور!

للاستخدام:
1. افتح الرابط: [الرابط هنا]
2. في الـ Sidebar، أدخل Gemini API Key
3. اختر AI Agent mode
4. اسأل أي سؤال!

أمثلة:
- "What is NaCl?"
- "Explain crystal structures"
- "Generate POSCAR for Silicon"

للمساعدة: راجع ملف QUICK_START.md
```

---

## 🎯 الطريقة الموصى بها

### للتجربة السريعة:
**استخدم Ngrok** - سهل وسريع

### للاستخدام الدائم:
**Streamlit Cloud** - مجاني ومستقر

### للشبكة المحلية فقط:
**Local Network** - أسرع وأأمن

---

## ⚠️ ملاحظات مهمة

1. **الأمان**: لا تشارك API keys في أماكن عامة
2. **الحصص**: Gemini له حد مجاني يومي
3. **السرعة**: MP API قد يكون بطيء
4. **الدعم**: AI Agent هو الأسرع والأفضل

---

**اختر الطريقة المناسبة وابدأ! 🚀**
