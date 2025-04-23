# 📲 WhatsappAutoSender

**WhatsappAutoSender** is a **Streamlit-based** bulk messaging tool that helps you send **personalized WhatsApp messages** and **images** using **WhatsApp Web**. Perfect for marketing, event announcements, or friendly reminders—no coding or API needed!

---

## ✨ Features

- 🔁 Send **bulk personalized messages**
- 🖼️ Attach **images** with messages
- 📊 Manage contacts with an **Excel file**
- ⚡ See **real-time progress**
- 🧩 Use **{{Name}}** in messages to personalize
- 🌐 Works with **WhatsApp Web** (no API or approval needed)

---

## ✅ Requirements

Before you start, make sure you have:

- **Python 3.6+**
- A valid **WhatsApp account**
- A web browser (Google Chrome recommended)
- An **Excel file** with:
  - `Name` column
  - `Phone Number` column (with or without country code – `+91` is added automatically if missing)

---

## 🛠️ How to Install & Run (Super Simple)

### 1. Download the Project

```bash
git clone https://github.com/yourusername/WhatsappAutoSender.git
cd WhatsappAutoSender
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install All Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

This will open the app in your **web browser**.

---

## 📁 Example Excel Format

| Name      | Phone Number  |
|-----------|---------------|
| Alice     | 9876543210    |
| Bob       | +919876543210 |

---

## 🚀 Now You're Ready!

- Upload your Excel file
- Write your message like:
  ```
  Hello {{Name}}, don't miss our event today!
  ```
- Optionally upload an image
- Click **Send** and watch the magic happen on WhatsApp Web!

---
