import telebot
from google import genai
from google.genai import types
import requests
from bs4 import BeautifulSoup
import time

# 1. Cấu hình các Token bảo mật
TELEGRAM_TOKEN = "8683129988:AAFiRv0_v6qinrCLsFJcGshgLMygAJEvJv8"
GEMINI_API_KEY = "AIzaSyB2m-FuYAyHdx7n0JPgM4hbWCGTBQCjNUg"
WEBSITE_URL = "https://ksxd.vn"
SITEMAP_URL = "https://ksxd.vn/sitemap.xml" # Anh kiểm tra lại đường dẫn sitemap thực tế của web nhé

# Khởi tạo Bot Telegram và Client AI
bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Hàm TỰ ĐỘNG CÀO DỮ LIỆU từ website ksxd.vn
def get_knowledge_base():
    print("🔄 Đang cào dữ liệu mới nhất từ ksxd.vn...")
    knowledge = "DỮ LIỆU KIẾN THỨC CẬP NHẬT TỪ WEBSITE KSXD.VN:\n"
    
    # Thêm sẵn các kiến thức cốt lõi/quy tắc ngầm của anh Pháp vào trước
    knowledge += """
    - Logic rải cây chống (chống formwork): Luôn luôn rải ở phía ngoài (exterior) của đường biên hình học, không rải phía trong.
    - Công cụ KTKL (Quantity Survey): Hỗ trợ kiểm tra, tính toán khối lượng và tracing 2 chiều giữa Excel và AutoCAD thông qua mã Handle ID của cấu kiện.
    """
    
    try:
        # Bước A: Đọc sitemap để lấy danh sách các link bài viết mới
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        sitemap_response = requests.get(SITEMAP_URL, headers=headers, timeout=10)
        
        if sitemap_response.status_code == 200:
            soup = BeautifulSoup(sitemap_response.content, 'xml')
            # Lấy tối đa 5-7 đường link mới nhất để tránh quá tải bộ nhớ AI
            urls = [loc.text for loc in soup.find_all('loc')][:7]
            
            # Bước B: Quét qua từng link để cào nội dung chữ (Text)
            for url in urls:
                try:
                    page_response = requests.get(url, headers=headers, timeout=5)
                    if page_response.status_code == 200:
                        page_soup = BeautifulSoup(page_response.content, 'html.parser')
                        
                        # Lấy tiêu đề bài viết
                        title = page_soup.find('title').text if page_soup.find('title') else ""
                        # Lấy toàn bộ các đoạn văn bản chính trong bài viết
                        paragraphs = [p.text for p in page_soup.find_all('p')]
                        content = " ".join(paragraphs)[:1000] # Giới hạn 1000 ký tự mỗi bài cho gọn
                        
                        knowledge += f"\n--- Bài viết: {title} (Link: {url}) ---\nNội dung: {content}\n"
                except Exception as e:
                    print(f"Lỗi khi đọc link {url}: {e}")
        else:
            print("Không đọc được Sitemap, chuyển sang quét trang chủ...")
            # Nếu không có sitemap, tạm thời cào chữ trên trang chủ
            homepage_res = requests.get(WEBSITE_URL, headers=headers, timeout=10)
            homepage_soup = BeautifulSoup(homepage_res.content, 'html.parser')
            knowledge += homepage_soup.get_text()[:4000] # Lấy 4000 ký tự trang chủ
            
    except Exception as e:
        print(f"❌ Lỗi tổng thể khi cào web: {e}")
        knowledge += "\n(Lưu ý: Không kết nối được website, sử dụng kiến thức cũ)."
        
    return knowledge

# 3. Hàm xử lý câu hỏi bằng Gemini AI (Mô hình RAG tự động cập nhật)
def ask_gemini_with_context(user_question):
    # Mỗi lần có người hỏi, bot sẽ chạy hàm cào dữ liệu mới nhất trên web về
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
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return "🤖 Hiện tại hệ thống phản hồi từ ksxd.vn đang bận một chút do nghẽn mạng. Anh/em vui lòng thử lại câu hỏi sau vài giây nhé!"

# 4. Lắng nghe và xử lý tin nhắn từ nhóm Telegram
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

# 5. Kích hoạt Bot
print("🤖 Bot ksxd.vn (Bản cập nhật tự động cào web) đang chạy...")
bot.infinity_polling()