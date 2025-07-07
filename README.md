# 🌐 Multi-Platform Social Media Poster

A **Python + Streamlit** based tool that allows users to **create, preview, schedule, and publish posts** to **Instagram, Facebook, Twitter (X), and LinkedIn** from a single platform.

## 🚀 Features

- 📝 Compose posts with emoji support
- 🔖 Select post type: Update, Promotion, Event, Announcement
- 🖼️ Upload images (required for Instagram, optional for others)
- ⏱️ Schedule posts for a future date and time
- 🔐 Securely input API keys and credentials
- 👁️ Real-time post preview
- 📤 Post to **multiple platforms at once**

---

## 🛠️ Tech Stack

| Technology     | Purpose                         |
|----------------|----------------------------------|
| `Python`       | Core logic & scripting          |
| `Streamlit`    | Front-end web interface         |
| `instagrapi`   | Instagram automation            |
| `facebook graph API` | Facebook page posting     |
| `tweepy`       | Twitter posting via API         |
| `linkedin_api` | LinkedIn post sharing           |
| `PIL`          | Image handling and preview      |
| `datetime`     | Scheduling logic                |
| `threading`    | Delayed execution for scheduled posts |
| `os`           | File handling                   |

---

## 📸 UI Screenshots

| Post Creation | Scheduling | Preview |
|---------------|------------|---------|
| ![compose](screenshots/compose.png) | ![schedule](screenshots/schedule.png) | ![preview](screenshots/preview.png) |

---

## 🔐 Platform-Specific Credentials

| Platform  | Authentication Method |
|-----------|------------------------|
| Instagram | Username + Password (via `instagrapi`) |
| Facebook  | Page Access Token + Page ID |
| Twitter   | API Key, API Secret, Access Token, Access Token Secret |
| LinkedIn  | Email + Password (via `linkedin_api`) |

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/multi-platform-poster.git
cd multi-platform-poster
pip install -r requirements.txt
streamlit run app.py
