import telebot
from google import genai
import requests
from bs4 import BeautifulSoup
import time
import os
from flask import Flask, request

# --- CẤU HÌNH CONFIG BOT TELEGRAM & AI ---
TELEGRAM_TOKEN = "8683129988:AAFiRv0_v6qinrCLsFJcGshgLMygAJEvJv8"
GEMINI_API_KEY = "AIzaSyB2m-FuYAyHdx7n0JPgM4hbWCGTBQCjNUg"
WEBSITE_URL = "https://ksxd.vn"
SITEMAP_URL = "https://ksxd.vn/sitemap.xml"

# Khởi tạo Bot và AI
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False) # Tắt threaded của bot để tránh xung đột luồng
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# --- KHỞI TẠO WEB FLASK (KẾT HỢP WEB HỒI & WEBHOOK) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ksxd.vn đang chạy online bằng cơ chế Webhook!"

# Đường dẫn tiếp nhận tin nhắn từ Telegram bắn về
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def receive_updates():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Lỗi định dạng dữ liệu', 403

# --- CÁC HÀM XỬ LÝ LOGIC BOT ---
def get_knowledge_base():
    print("🔄 Đang tiến hành quét và cập nhật dữ liệu từ ksxd.vn...")
    knowledge = "=== HỆ THỐNG DỮ LIỆU KIẾN THỨC NỀN CỦA WEBSITE KSXD.VN ===\n"
    knowledge += """
    [QUY TẮC PHẦN MỀM & KỸ THUẬT]:
    - Logic rải cây chống (chống formwork): Luôn luôn bắt buộc rải ở phía NGOÀI (exterior) của đường biên hình học, tuyệt đối không rải phía trong.
    - Công cụ KTKL (Quantity Survey): Hỗ trợ kiểm tra, tính toán khối lượng và tracing (truy vết) 2 chiều linh hoạt giữa Excel và AutoCAD thông qua mã định danh duy nhất Handle ID của cấu kiện.
    - Tiện ích khác: Chia sẻ các file mẫu Excel chuyên sâu phục vụ quản lý hồ sơ thanh toán, hồ sơ quyết toán và quản lý công nợ cuối năm cho nhà thầu xây dựng.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        sitemap_response = requests.get(SITEMAP_URL, headers=headers, timeout=10)
        if sitemap_response.status_code == 200:
            soup = BeautifulSoup(sitemap_response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')][:5]
            for url in urls:
                try:
                    page_response = requests.get(url, headers=headers, timeout=5)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        title = page_soup.find('title').text.strip() if page_soup.find('title') else "Bài viết"
                        paragraphs = [p.text.strip() for p in page_soup.find_all('p') if p.text.strip()]
                        content = " ".join(paragraphs)[:800]
                        knowledge += f"\n[BÀI VIẾT]: {title}\n[LINK]: {url}\n[NỘI DUNG]: {content}\n"
                except Exception as e:
                    print(f"Lỗi link {url}: {e}")
        else:
            homepage_res = requests.get(WEBSITE_URL, headers=headers, timeout=10)
            homepage_soup = BeautifulSoup(homepage_res.content, 'html.parser')
            knowledge += f"\n[TRANG CHỦ]:\n{homepage_soup.get_text()[:2000]}"
    except Exception as e:
        print(f"❌ Lỗi cào web: {e}")
    return knowledge

def ask_gemini_with_context(user_question):
    try:
        context = get_knowledge_base()
    except Exception as e:
        context = "Lỗi nạp dữ liệu web, sử dụng cấu trúc gốc."

    prompt = f"""
    Bạn là một trợ lý ảo thông minh của website ksxd.vn.
    Hãy trả lời câu hỏi của người dùng dựa trên thông tin dữ liệu dưới đây. Không lặp lại câu hỏi.

    DỮ LIỆU KIẾN THỨC:
    {context}

    [CÂU HỎI]: "{user_question}"
    [TRẢ LỜI]:
    """
    
    max_retries = 3
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return f"❌ Lỗi kết nối Gemini AI chi tiết: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    if not user_text:
        return
    status_msg = bot.reply_to(message, "🔄 Bot đang kiểm tra dữ liệu mới nhất trên ksxd.vn để trả lời, chờ em tí nhé...")
    ai_reply = ask_gemini_with_context(user_text)
    bot.reply_to(message, ai_reply)
    try:
        bot.delete_message(message.chat.id, status_msg.message_id)
    except:
        pass

# --- KÍCH HOẠT SERVER WEBHOOK ---
if __name__ == "__main__":
    # Tự động đăng ký Webhook với hệ thống Telegram khi khởi động server
    WEBHOOK_URL = "https://bot-telegram-ksxd-1.onrender.com"
    
    print("🔄 Đang xóa kết nối cũ và đăng ký Webhook mới...")
    bot.remove_webhook()
    time.sleep(1)
    
    # Đăng ký link nhận tin nhắn mới
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    print("✅ Đăng ký Webhook thành công!")
    
    # Khởi chạy server web (Render sẽ nuôi luồng này trực tiếp)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
