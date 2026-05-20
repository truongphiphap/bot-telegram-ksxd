import telebot
from google import genai
from google.genai import types
import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask
from threading import Thread

# --- PHẦN KHỞI TẠO WEB MỒI ĐỂ GIỮ GÓI FREE TRÊN RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ksxd.vn đang chạy online 24/7!"

def run_flask():
    # Render sẽ tự động cấp một cổng thông qua biến môi trường PORT, mặc định là 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- PHẦN CONFIG BOT TELEGRAM & AI ---
TELEGRAM_TOKEN = "8683129988:AAFiRv0_v6qinrCLsFJcGshgLMygAJEvJv8"
GEMINI_API_KEY = "AIzaSyB2m-FuYAyHdx7n0JPgM4hbWCGTBQCjNUg"
WEBSITE_URL = "https://ksxd.vn"
SITEMAP_URL = "https://ksxd.vn/sitemap.xml"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def get_knowledge_base():
    print("🔄 Đang cào dữ liệu mới nhất từ ksxd.vn...")
    knowledge = "DỮ LIỆU KIẾN THỨC CẬP NHẬT TỪ WEBSITE KSXD.VN:\n"
    knowledge += """
    - Logic rải cây chống (chống formwork): Luôn luôn rải ở phía ngoài (exterior) của đường biên hình học, không rải phía trong.
    - Công cụ KTKL (Quantity Survey): Hỗ trợ kiểm tra, tính toán khối lượng và tracing 2 chiều giữa Excel và AutoCAD thông qua mã Handle ID của cấu kiện.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        sitemap_response = requests.get(SITEMAP_URL, headers=headers, timeout=10)
        if sitemap_response.status_code == 200:
            soup = BeautifulSoup(sitemap_response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')][:7]
            for url in urls:
                try:
                    page_response = requests.get(url, headers=headers, timeout=5)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        title = page_soup.find('title').text if page_soup.find('title') else ""
                        paragraphs = [p.text for p in page_soup.find_all('p')]
                        content = " ".join(paragraphs)[:1000]
                        knowledge += f"\n--- Bài viết: {title} (Link: {url}) ---\nNội dung: {content}\n"
                except Exception as e:
                    print(f"Lỗi link {url}: {e}")
        else:
            homepage_res = requests.get(WEBSITE_URL, headers=headers, timeout=10)
            homepage_soup = BeautifulSoup(homepage_res.content, 'html.parser')
            knowledge += homepage_soup.get_text()[:4000]
    except Exception as e:
        knowledge += "\n(Không kết nối được website, sử dụng kiến thức gốc)."
    return knowledge

def ask_gemini_with_context(user_question):
    context = get_knowledge_base()
    prompt = f"""
    Bạn là một trợ lý ảo thông minh của cộng đồng kỹ sư xây dựng ksxd.vn.
    Hãy dựa vào dữ liệu kiến thức được cập nhật trực tiếp từ website dưới đây để trả lời câu hỏi của người dùng một cách ngắn gọn, chuyên nghiệp và thực tế.
    Ưu tiên cung cấp link bài viết tương ứng có trong dữ liệu kiến thức để người dùng click vào xem.
    Nếu câu hỏi không liên quan đến kiến thức được cung cấp, hãy lịch sự từ chối và hướng dẫn họ truy cập website ksxd.vn để tìm hiểu thêm.

    DỮ LIỆU KIẾN THỨC WEB:
    {context}

    CÂU HỎI CỦA NGƯỜI DÙNG:
    {user_question}
    
    CÂU TRẢ LỜI CỦA BẠN:
    """
    max_retries = 3
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return "🤖 Hiện tại hệ thống phản hồi từ ksxd.vn đang bận một chút do nghẽn mạng. Anh/em vui lòng thử lại câu hỏi sau vài giây nhé!"

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    status_msg = bot.reply_to(message, "🔄 Bot đang kiểm tra dữ liệu mới nhất trên ksxd.vn để trả lời, chờ em tí nhé...")
    ai_reply = ask_gemini_with_context(user_text)
    bot.reply_to(message, ai_reply)
    try:
        bot.delete_message(message.chat.id, status_msg.message_id)
    except:
        pass

# --- KÍCH HOẠT CHẠY SONG SONG CẢ WEB LẪN BOT ---
if __name__ == "__main__":
    # Chạy Web mồi ở một luồng riêng (Thread) để Render không báo lỗi Port
    t = Thread(target=run_flask)
    t.start()
    
    # Chạy bot Telegram ở luồng chính
    print("🤖 Bot ksxd.vn trực tuyến 24/7...")
    bot.infinity_polling()
