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
    print("🔄 Đang tiến hành quét và cập nhật dữ liệu từ ksxd.vn...")
    knowledge = "=== HỆ THỐNG DỮ LIỆU KIẾN THỨC NỀN CỦA WEBSITE KSXD.VN ===\n"
    
    # Các quy tắc cốt lõi cố định của anh Pháp
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
            print("✅ Đã kết nối sitemap thành công. Đang trích xuất link bài viết...")
            soup = BeautifulSoup(sitemap_response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')][:7]
            
            for url in urls:
                try:
                    page_response = requests.get(url, headers=headers, timeout=5)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        title = page_soup.find('title').text.strip() if page_soup.find('title') else "Bài viết không tiêu đề"
                        paragraphs = [p.text.strip() for p in page_soup.find_all('p') if p.text.strip()]
                        content = " ".join(paragraphs)[:1200]
                        
                        knowledge += f"\n[BÀI VIẾT]: {title}\n[ĐƯỜNG DẪN]: {url}\n[NỘI DUNG]: {content}\n-----------------------------\n"
                except Exception as e:
                    print(f"❌ Lỗi khi đọc nội dung tại link {url}: {e}")
        else:
            print("⚠️ Không tìm thấy hoặc lỗi sitemap, tự động chuyển sang đọc dữ liệu trang chủ...")
            homepage_res = requests.get(WEBSITE_URL, headers=headers, timeout=10)
            homepage_soup = BeautifulSoup(homepage_res.content, 'html.parser')
            knowledge += f"\n[TRANG CHỦ TỔNG HỢP]:\n{homepage_soup.get_text()[:4000]}"
            
    except Exception as e:
        print(f"❌ Lỗi tổng thể trong quá trình cào web: {e}")
        knowledge += "\n(Hệ thống gặp lỗi kết nối internet với website, tạm thời sử dụng kiến thức kỹ thuật gốc ở trên)."
        
    return knowledge

def ask_gemini_with_context(user_question):
    context = get_knowledge_base()
    
    # Thiết lập cấu trúc Prompt cô lập câu hỏi và ra lệnh nghiêm ngặt
    prompt = f"""
    Bạn là một chuyên gia và là Trợ lý ảo thông minh đại diện cho website chuyên ngành xây dựng ksxd.vn.
    Nhiệm vụ duy nhất của bạn là giải đáp câu hỏi của người dùng dựa trên thông tin được cung cấp trong phần DỮ LIỆU KIẾN THỨC dưới đây.

    ⚠️ QUY TẮC BẮT BUỘC:
    1. KHÔNG ĐƯỢC lặp lại, sao chép hoặc trích dẫn lại nguyên văn câu hỏi của người dùng dưới mọi hình thức.
    2. Tập trung trả lời thẳng vào bản chất câu hỏi một cách ngắn gọn, mạch lạc, chính xác theo tư duy kỹ sư.
    3. Nếu trong phần DỮ LIỆU KIẾN THỨC có chứa đường dẫn (Link) phù hợp với câu hỏi, hãy đính kèm link đó vào câu trả lời để người dùng bấm vào xem.
    4. Nếu câu hỏi nằm ngoài phạm vi thông tin được cung cấp, hãy lịch sự từ chối và hướng dẫn họ truy cập trực tiếp website ksxd.vn để tra cứu thêm.

    --- BẮT ĐẦU DỮ LIỆU KIẾN THỨC ĐƯỢC CẤP ---
    {context}
    --- KẾT THÚC DỮ LIỆU KIẾN THỨC ĐƯỢC CẤP ---

    [CÂU HỎI CỦA NGƯỜI DÙNG]:
    "{user_question}"

    [CÂU TRẢ LỜI CỦA TRỢ LÝ]:
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
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return "🤖 Hiện tại hệ thống kết nối AI đang bận xử lý dữ liệu. Anh/em vui lòng gửi lại câu hỏi sau vài giây nhé!"

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

# --- KÍCH HOẠT CHẠY SONG SONG CẢ WEB LẪN BOT ---
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("🤖 Bot ksxd.vn trực tuyến và sẵn sàng phục vụ 24/7...")
    bot.infinity_polling()
