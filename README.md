# 📲 WhatsappAutoSender

**WhatsappAutoSender** is a Streamlit-based bulk messaging tool for WhatsApp that allows you to send **personalized messages** and **images** to multiple contacts using WhatsApp Web. Ideal for marketing campaigns, event announcements, reminders, and more.

---

## ✨ Features

- 🔁 Send bulk **personalized** WhatsApp messages
- 🖼️ Supports **image attachments**
- 📊 **Excel-based contact management** (Name & Phone Number)
- ⚡ Real-time **progress tracking**
- 🧩 Message **template support** using `{{Name}}` for personalization
- 🌐 **WhatsApp Web** integration (no API required)

---

## ✅ Prerequisites

- Python 3.6+
- A valid WhatsApp account
- A web browser (Google Chrome recommended)
- WhatsApp Web access
- Excel file containing:
  - `Name` column
  - `Phone Number` column (with or without country code; app adds `+91` prefix if needed)

---

## 🛠️ Installation

### 1. Clone the Repository

````bash
git clone https://github.com/yourusername/WhatsappAutoSender.git
cd WhatsappAutoSender

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
````
