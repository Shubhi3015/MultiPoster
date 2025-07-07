import streamlit as st
import requests
import tweepy
from linkedin_api import Linkedin
from instagrapi import Client
from PIL import Image
from datetime import datetime, timedelta
import threading
import os

st.set_page_config(page_title=" Multi-Platform Poster", layout="centered")

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: #121212;
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
}

section[data-testid="stSidebar"] {
    background-color: #1e1e1e;
    color: #f0f0f0;
    border-right: 1px solid #333;
}

.stButton > button {
    background-color: #1f6feb;
    color: #ffffff;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #1158c7;
}

input, textarea {
    background-color: #2c2c2c !important;
    color: white !important;
    border-radius: 6px;
}

[data-testid="stFileUploader"] {
    background-color: #2c2c2c;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/fluency/100/share-2.png", width=100)
st.sidebar.title("🌐 Social Media Poster")
st.sidebar.write("Post messages to multiple platforms from one place.")
st.sidebar.markdown("---")
platform = st.sidebar.multiselect("Select Platforms", ["Instagram", "Facebook", "Twitter", "LinkedIn"])
st.sidebar.markdown("---")

st.title("📣 Create Your Post")
message = st.text_area("📝 Enter your message")

char_count = len(message)
st.caption(f"🧮 Characters: {char_count}/2200")

emojis = ["😀", "🔥", "📸", "💬", "🎉", "🚀", "📢"]
emoji_choice = st.selectbox("😊 Add an emoji (optional)", ["None"] + emojis)
if emoji_choice != "None":
    message += f" {emoji_choice}"

post_type = st.radio("📌 Post Type", ["Update", "Promotion", "Event", "Announcement"])
if post_type:
    message = f"[{post_type}] {message}"

uploaded_image = st.file_uploader("📷 Upload an image (optional for Instagram/Facebook)", type=["jpg", "png", "jpeg"])
image_path = None
if uploaded_image:
    image_path = f"temp_{uploaded_image.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())

st.markdown("### ⏱️ Schedule Post (Optional)")
schedule_enabled = st.checkbox("Schedule this post for later?")
scheduled_time = None
if schedule_enabled:
    schedule_date = st.date_input("Choose date", value=datetime.now().date())
    schedule_time = st.time_input("Choose time", value=(datetime.now() + timedelta(minutes=1)).time())
    scheduled_time = datetime.combine(schedule_date, schedule_time)

    seconds_left = int((scheduled_time - datetime.now()).total_seconds())
    if seconds_left > 0:
        st.info(f"⏳ Post will go live in {seconds_left // 60} min {seconds_left % 60} sec.")

if "Instagram" in platform:
    with st.expander("📸 Instagram Credentials"):
        insta_user = st.text_input("Instagram Username")
        insta_pass = st.text_input("Instagram Password", type="password")

if "Facebook" in platform:
    with st.expander("📘 Facebook Page Setup"):
        fb_token = st.text_input("Facebook Page Access Token")
        fb_page_id = st.text_input("Facebook Page ID")

if "Twitter" in platform:
    with st.expander("🐦 Twitter API Keys"):
        consumer_key = st.text_input("API Key")
        consumer_secret = st.text_input("API Secret")
        access_token = st.text_input("Access Token")
        access_secret = st.text_input("Access Token Secret")

if "LinkedIn" in platform:
    with st.expander("🔗 LinkedIn Login"):
        li_user = st.text_input("LinkedIn Email")
        li_pass = st.text_input("LinkedIn Password", type="password")

st.subheader("👁️ Preview")
st.info(message)
if image_path:
    st.image(uploaded_image, caption="Uploaded Image", width=300)

def post_to_platforms():
    try:
        st.toast("🔄 Posting in progress...", icon="🔄")
    except:
        st.info("🔄 Posting in progress...")

    
    if "Instagram" in platform and insta_user and insta_pass:
        try:
            insta = Client()
            insta.login(insta_user, insta_pass)
            if image_path:
                insta.photo_upload(image_path, message)
                st.success("✅ Instagram: Posted successfully!")
            else:
                st.warning("Instagram requires an image.")
        except Exception as e:
            st.error(f"Instagram error: {e}")

    
    if "Facebook" in platform and fb_token and fb_page_id:
        try:
            url = f"https://graph.facebook.com/{fb_page_id}/photos" if image_path else f"https://graph.facebook.com/{fb_page_id}/feed"
            data = {'access_token': fb_token, 'message': message}
            files = {'source': open(image_path, 'rb')} if image_path else None
            r = requests.post(url, data=data, files=files)
            if r.ok:
                st.success("✅ Facebook: Posted successfully!")
            else:
                st.error(f"Facebook error: {r.text}")
        except Exception as e:
            st.error(f"Facebook error: {e}")

   
    if "Twitter" in platform and consumer_key and access_token:
        try:
            auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret)
            api = tweepy.API(auth)
            if image_path:
                api.update_with_media(image_path, status=message)
            else:
                api.update_status(message)
            st.success("✅ Twitter: Tweeted successfully!")
        except Exception as e:
            st.error(f"Twitter error: {e}")

   
    if "LinkedIn" in platform and li_user and li_pass:
        try:
            linkedin = Linkedin(li_user, li_pass)
            me = linkedin.get_profile()
            urn = f"urn:li:person:{me['profile_id']}"
            linkedin.post_share(urn=urn, text=message)
            st.success("✅ LinkedIn: Posted successfully!")
        except Exception as e:
            st.error(f"LinkedIn error: {e}")

  
    if image_path and os.path.exists(image_path):
        os.remove(image_path)


if st.button("🚀 Post Now"):
    if not message.strip():
        st.warning("Please enter a message.")
    else:
        if schedule_enabled and scheduled_time:
            delay = (scheduled_time - datetime.now()).total_seconds()
            if delay <= 0:
                st.warning("Please choose a time in the future.")
            else:
                threading.Timer(delay, post_to_platforms).start()
                st.success(f"✅ Post scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            post_to_platforms()
