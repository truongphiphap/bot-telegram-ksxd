import telebot
from google import genai
import requests
import time
import os
from flask import Flask, request

# --- CẤU HÌNH CONFIG BOT TELEGRAM & AI ---
TELEGRAM_TOKEN = "8683129988:AAFiRv0_v6qinrCLsFJcGshgLMygAJEvJv8"
GEMINI_API_KEY = "AIzaSyAZOtXiANWEiZ8CNvrXOQbTkwJZfStaJcU"

# Khởi tạo Bot và AI Client (threaded=False bảo vệ tài nguyên gói free)
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# --- KHỞI TẠO WEB FLASK ĐỂ CHẠY WEBHOOK & CHỐNG NGỦ ĐÔNG ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Hệ thống AI Chuyên Gia Tổng Hợp KSXD.VN đang online bằng cơ chế Webhook!"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def receive_updates():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Lỗi định dạng dữ liệu', 403

# --- BỘ NÃO KIẾN THỨC TOÀN DIỆN TỪ HỆ THỐNG GIAO DIỆN & SEO KSXD.VN ---
def get_knowledge_base():
    knowledge = """
    === HỆ THỐNG CƠ SỞ DỮ LIỆU TÀI NGUYÊN NỀN TẢNG KỸ SƯ SỐ 4.0: KSXD.VN ===
    Sáng lập, quản lý và lập trình bởi: Kỹ sư Trương Phi Pháp (Thương hiệu TPP MasterPro).
    Slogan nền tảng: "Giải phóng sức lao động với kho Lisp CAD siêu tốc, file tính Excel và tài liệu biện pháp thi công được chắt lọc kỹ lưỡng dành riêng cho kỹ sư Việt."
    Chỉ số hệ thống: Tối ưu 70% thời gian làm việc của kỹ sư, hơn 100+ tiện ích hỗ trợ, hơn 200+ kỹ sư xây dựng tin dùng thường xuyên.

    [THÔNG TIN LIÊN HỆ CHÍNH THỨC & CÁC NHÓM CỘNG ĐỒNG]:
    - Hotline / Số Zalo hỗ trợ kỹ thuật: 092 3333 365 (Hỗ trợ tư vấn mua Lisp bản quyền, cài đặt lỗi).
    - Email liên hệ công việc: contact@ksxd.vn
    - Địa chỉ: Kỹ sư xây dựng, Việt Nam.
    - Nhóm Cộng đồng Facebook: https://www.facebook.com/groups/civil.engineer.vn (Nơi anh em giao lưu, đóng góp tài liệu).
    - Kênh YouTube chính thức: https://www.youtube.com/@TruongPhiPhap/ (Xem video hướng dẫn thao tác lệnh CAD, Lisp thực tế).
    - Kênh TikTok chia sẻ: https://www.tiktok.com/@nguoithoxay (Chia sẻ kiến thức thực chiến hiện trường).

    [DANH MỤC 1: KHO LISP CAD MIỄN PHÍ - ĐỒNG GÓP TỪ CỘNG ĐỒNG (URL: https://ksxd.vn/Lispcad-free)]
    Bộ sưu tập Lisp CAD cực hay được KSXD tổng hợp từ nhiều nguồn trên Internet để chia sẻ miễn phí đến anh em:
    1. Mã Lisp 'TCD-TDT' - Lisp Tính chiều dài và diện tích (Cập nhật: 12/04/2026 bởi Admin): Tối ưu giúp tính nhanh mét vuông (diện tích Hatch/Polyline) và tổng mét dài (đường thẳng, đường cong gộp) phục vụ bóc tách khối lượng hoàn công, vật tư sơn nước, trần sàn.
    2. Mã Lisp 'YQArch-autocad' - Bộ công cụ YQArch của các pháp sư Trung Hoa (Cập nhật: 15/04/2026 bởi Admin. Link: https://ksxd.vn/Lispcad-free/YQArch-autocad): Plugin hỗ trợ tăng tốc độ vẽ kiến trúc, kết cấu lên gấp 3 lần.
    3. Mã Lisp '3' - Lisp tự động dim kích thước Auto Dim (Cập nhật: 18/04/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/auto-dim): Dim kích thước nhanh gọn, đường nét đồng bộ cho các bản vẽ chi tiết cấu kiện phức tạp.
    4. Mã Lisp '4' - Lisp chơi game Caro và Cờ tướng trên CAD (Cập nhật: 20/04/2026 bởi đóng góp của NhatHuynhQS. Link: https://ksxd.vn/lispcad-free/game-autocad): Mini game giải trí nhẹ nhàng ngay trên nền tảng AutoCAD sau những giờ vẽ căng thẳng.
    5. Mã Lisp '5' - Lisp Trích chi tiết bản vẽ (Cập nhật: 22/04/2026 bởi NhatHuynh QS. Link: https://ksxd.vn/lispcad-free/trich-chi-tiet-bv): Khoanh vùng tự động phóng to trích xuất cấu kiện làm shop drawing.
    6. Mã Lisp '6' - Lisp cắt chân dim + làm bằng đầu dim CD-DB (Cập nhật: 25/04/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/cd-db): Giúp bản vẽ AutoCAD gọn gàng, chuyên nghiệp, cân bằng các đường dim.
    7. Mã Lisp '7' - Lisp tự động đánh số thứ tự theo bước nhảy (Cập nhật: 28/04/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/danh-so-thu-tu): Đánh số nhanh cho hệ trục, mặt bằng móng, định vị cọc, hệ dầm chỉ với vài click chuột.
    8. Mã Lisp '8' - Lisp tính tổng dim SumDim (Cập nhật: 29/04/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/sumdim): Pick hàng loạt các đoạn Dim và xuất tổng DIM trực tiếp ra màn hình CAD để tính tổng mét dài nhanh.
    9. Mã Lisp '9' - Lisp thống kê text, thống kê block (Cập nhật: 30/04/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/tkt-tkb): Đếm chính xác số lượng block cấu kiện, thiết bị, tự động xuất bảng thống kê ra màn hình CAD.
    10. Mã Lisp '10' - Lisp thống kê hình học TKHH (Cập nhật: 01/05/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/tkhh): Đếm và thống kê diện tích các hình phẳng kín như hộp gen, cổ cột, tính toán số lần xuất hiện của hình đó.
    11. Mã Lisp '11' - Lisp Máy in ảo in hàng loạt bản vẽ sang 1 file PDF - Lệnh 'PRT' (Cập nhật: 02/05/2026 bởi Admin. Link: https://ksxd.vn/lispcad-free/xuat-pdf-hang-loat-tren-cad): Tự động nhận diện khung bản vẽ (Block khung tên hoặc Rectangle), xuất hàng loạt ra PDF chuẩn khổ giấy và gộp tất cả thành một file duy nhất theo đúng thứ tự bản vẽ.
    12. Mã Lisp '12' - Lisp chuyển bảng Excel sang AutoCAD (Cập nhật: 02/05/2026 bởi NhatHuynh QS. Link: https://ksxd.vn/lispcad-free/table-excel-to-cad): Đưa bảng tính từ Excel vào AutoCAD giữ nguyên định dạng, liên kết dữ liệu hai chiều mượt mà.

    [DANH MỤC 2: KHO LISP CAD BẢN QUYỀN CHUYÊN SÂU - VĨNH VIỄN THEO MÁY (URL: https://ksxd.vn/lispcad-co-phi)]
    Bộ công cụ cao cấp thiết kế cho kỹ sư chuyên nghiệp, cam kết hỗ trợ cập nhật lâu dài và hướng dẫn chi tiết 24/7. Định giá: LIÊN HỆ HOTLINE/ZALO 092 3333 365 ĐỂ NHẬN BÁO GIÁ GIỮA CÁC GÓI.
    1. Mã công cụ 'BPCP' - Bộ biện pháp cốp pha (Xếp hạng 1 - HOT / BESTSELLER. Link: https://ksxd.vn/lispcad-co-phi/bienphap-copha): Tự động hóa vẽ biện pháp thi công cốp pha móng, cột, vách, dầm sàn; vẽ mặt bằng và mặt cắt hệ giáo chống giằng (giáo nêm, ringlock) và xuất bảng thống kê vật tư thiết bị.
       * QUY TẮC RẢI CÂY CHỐNG BẮT BUỘC: Hệ thống rải cây chống cốp pha (formwork support) phải nằm ở phía NGOÀI (exterior) của đường biên hình học (perimeter) cấu kiện biên, tuyệt đối không được rải nhầm vào phía trong lòng cấu kiện.
    2. Mã công cụ '32TOOLS' - Combo 32 công cụ check khối lượng KTKL (Xếp hạng 2 - HOT / BESTSELLER. Link: https://ksxd.vn/lispcad-co-phi/congcu-check-kl): Các công cụ check khối lượng bê tông, cốp pha, xuất báo cáo Excel trực tiếp, đối chiếu được khối lượng đã bốc tách.
       * TÍNH NĂNG ĐỘC QUYỀN 'checkkl': Sử dụng mã định danh Handle ID của cấu kiện tạo liên kết tracing 2 chiều linh hoạt giữa Excel và AutoCAD, giúp kiểm tra chéo sai sót, click dòng khối lượng tự động vẽ tia mạng nhện tìm vị trí cấu kiện trong CAD, chống bỏ sót khối lượng.
    3. Mã công cụ 'NHOM-ALU' - Tổ hợp cốp pha nhôm cột vách đơn, lõi thang vách podium (Link: https://ksxd.vn/lispcad-co-phi/nhom-vach-loi): Tự động hóa shopdrawing tổ hợp tấm nhôm, thống kê phụ kiện chốt, v góc, thanh la cài cho hệ vách lõi thang máy (Corewall), bể nước, tường một mặt tại các tầng sàn podium chưa điển hình (dùng lệnh W rải tấm rộng 450mm tiêu chuẩn, lệnh WS rải tấm đơn lẻ tùy biến kích thước, tự vẽ mặt cắt vách).
    4. Mã công cụ 'VAN-KHUON' - Rải ván khuôn sàn tự động (Link: https://ksxd.vn/lispcad-co-phi/rai-van): Triển khai shop drawing tự động chia tấm ván khuôn sàn tối ưu diện tích dựa trên kích thước tấm ván phủ phim tiêu chuẩn (2440x1220), kiểm soát thi công theo shop và lập đề nghị cấp phát vật tư chính xác, xuất bảng tính ván nguyên, ván cắt lẻ.
    5. Mã công cụ 'OP-LAT' - Shop drawing Ốp Lát nhanh (Link: https://ksxd.vn/lispcad-co-phi/op-lat): Hỗ trợ nhanh quá trình shop gạch ốp lát sàn, tường, tự động tính toán định lượng gạch nguyên, gạch cắt, giảm thiểu hao hụt vật tư giai đoạn hoàn thiện.
    6. Mã công cụ 'KATA' - Chuyển thép thiết kế về dạng cấu trúc Kata (Link: https://ksxd.vn/lispcad-co-phi/CT-Kata1): Đọc dữ liệu đường Line từ bản vẽ thiết kế cơ sở và tự động chuyển đổi đồng bộ sang định dạng Katapro để phục vụ thống kê khối lượng cốt thép tự động.

    [DANH MỤC 3: KHO FILE EXCEL MẪU CHUẨN - DÙNG THỰC TẾ CÔNG TRƯỜNG (URL: https://ksxd.vn/Excel-free)]
    Biểu mẫu thiết lập sẵn công thức, hàm tính toán nâng cao cho kỹ sư bóc tách, thi công, quản lý:
    1. Mã Excel '11' - Phần mềm bóc tách thép từ PDF sang Excel (Cập nhật: 11/04/2026 bởi Admin): Chuyển đổi thông minh dữ liệu bảng thống kê thép từ bản vẽ dạng PDF sang Excel.
    2. Mã Excel '2' - File Excel Quản Lý Xuất Nhập Tồn Vật Tư Công Trình Tự Động 100% (Cập nhật mới nhất: 14/05/2026 bởi Admin): Quản lý kho nhà thầu phụ (NTP), theo dõi xuất nhập tồn vật tư, vật liệu, báo cáo hao hụt, thất thoát tại công trường cho thủ kho và kỹ sư hiện trường.
    3. Mã Excel '3' - File Excel Tính Tải Trọng Gió Theo Chuẩn TCVN 2737:2023 (Cập nhật: 14/05/2026 bởi Đại Văn Hưng): Công thức lập sẵn tính toán thành phần gió tĩnh, gió động theo chuẩn quy chuẩn mới nhất.
    4. Mã Excel '4' - File Excel Mẫu QS Tổng Hợp Cho Kỹ Sư Mới Vào Nghề (Cập nhật: 14/04/2026 bởi Admin): Đầy đủ diễn giải tất cả các sheet cấu kiện chuẩn chỉ để đo bóc khối lượng công trình.
    5. Mã Excel '5' - Mẫu Excel quản lý thu chi công trường (Cập nhật: 23/04/2026 bởi 1page-xaydung.vn): Theo dõi dòng tiền dự án, quản lý công nợ nhà cung cấp, đội thầu phụ, theo dõi các khoản chi phí hoạt động nội bộ công trường cuối năm.
    6. Mã Excel '6' - File Excel Tính Khối Lượng Bê Tông – Cốp Pha – Cốt Thép (Cập nhật: 26/04/2026 bởi Greencons.vn): Mẫu tích hợp 3 trong 1 giúp bóc tách khối lượng bê tông, ván khuôn và thống kê cốt thép liên kết đồng bộ dữ liệu.
    7. Mã Excel '7' - File Excel Tính Thuế Thu Nhập Cá Nhân TNCN Tự Động 2026 (Cập nhật: 29/04/2026 bởi Nhathuynh QS): Tự động hóa tính lương Net/Gross, nội suy bảng thuế TNCN mới nhất cho ban điều hành cán bộ nhân viên.
    8. Mã Excel '8' - File Mẫu MS Project Tiến Độ Thi Công Nhà Cao Tầng Chuẩn Nhất (Cập nhật: 02/05/2026 bởi KSXD): Biểu mẫu tiến độ thi công phần ngầm, phần thân, đường găng kỹ thuật dây chuyền chuẩn xác.
    9. Mã Excel '9' - File Excel Bảng Tính Cốp Pha Móng, Cột, Dầm, Sàn Tự Động (Cập nhật: 05/05/2026 bởi HBC): Kiểm tra khả năng chịu lực, độ bền, độ võng của đà giáo, ván khuôn theo tiêu chuẩn kỹ thuật thi công.
    10. Mã Excel '10' - File Excel Tổng Hợp Các Hàm Thông Dụng Kèm Ví Dụ Trực Quan (Cập nhật: 08/05/2026 bởi 1google10ketoan): Cẩm nang các hàm VLOOKUP, INDEX, MATCH, SUMPRODUCT thực chiến ngành xây dựng.
    11. Mã Excel '12' - Combo File Excel Báo Cáo Ngày & Quản Lý Hồ Sơ Nghiệm Thu (Cập nhật: 18/05/2026 bởi Nguyễn Văn Vinh + KS CHIÊU + NhatHuynh QS): Tự động hóa lập nhật ký công trình, liên kết tạo danh mục hồ sơ nghiệm thu chất lượng (KCS) phục vụ làm hồ sơ thanh quyết toán.

    [DANH MỤC 4: KHO BẢN VẼ AUTOCAD & HỌC LIỆU MIỄN PHÍ (URL: https://ksxd.vn/autocad-file-free)]
    1. Bản vẽ Sàn Cáp Dự Ứng Lực thực tế (Link: https://ksxd.vn/autocad-file-free/Bptc-san-du-ung-luc).
    2. Thư viện 1000+ Block AutoCAD 2D siêu nhẹ, chuẩn layer (Link: https://ksxd.vn/autocad-file-free/Thu-vien-block).
    3. Trình tự thi công xây tường gạch AAC bê tông khí chưng áp nhẹ chuẩn TCVN (Link: https://ksxd.vn/autocad-file-free/bptc-tuong-acc).
    4. Thư viện Block AutoCAD biện pháp thi công giàn giáo, tổng mặt bằng, đào đất (Link: https://ksxd.vn/autocad-file-free/thu-vien-bien-phap).
    5. Phương pháp siêu đầm nện gia cố nền đất yếu xung kích năng lượng cao (Link: https://ksxd.vn/autocad-file-free/phuong-phap-sieu-dam-nen).
    6. Sổ Tay An Toàn Lao Động & Quy Tắc An Toàn Điện Công Trường (Link: https://ksxd.vn/autocad-file-free/so-tay-an-toan).
    7. Thư viện tải Model 3D quốc tết cực đỉnh cho BIM, kỹ sư cơ khí (Link: https://ksxd.vn/autocad-file-free/web-model-3d).
    """
    return knowledge

# --- THIẾT LẬP LUỒNG TƯ DUY VÀ HƯỚNG DẪN ĐIỀU HƯỚNG LIÊN HỆ CHO AI ---
def ask_gemini_with_context(user_question):
    context = get_knowledge_base()

    prompt = f"""
    Bạn là một kỹ sư xây dựng lão làng, một chuyên gia tối ưu hóa biện pháp và là Trợ lý ảo AI đại diện chính thức cho website ksxd.vn của kỹ sư Trương Phi Pháp.
    Nhiệm vụ của bạn là giải đáp thắc mắc của các anh em kỹ sư, nhà thầu hoặc QS trong nhóm Telegram dựa vào tài liệu "DỮ LIỆU KIẾN THỨC WEBSITE KSXD.VN" dưới đây.

    ⚠️ QUY TẮC PHẢN HỒI (BẮT BUỘC):
    1. Tuyệt đối KHÔNG ĐƯỢC lặp lại câu hỏi của người dùng dưới dạng ví dụ hay nhại lại lời. Trả lời thẳng thừng và chính xác vào câu hỏi.
    2. Sử dụng văn phong của dân công trường: Mạch lạc, thực tế, ngắn gọn, xưng hô là "Em" hoặc "Bot KSXD" và gọi người hỏi là "Anh" hoặc "Anh em kỹ sư".
    3. Khi anh em hỏi về Lisp có phí/bản quyền (như BPCP, 32TOOLS, NHOM-ALU, VAN-KHUON...), hãy luôn nhắc nhở anh em để lại số Zalo để được tư vấn hoặc liên hệ trực tiếp Hotline/Zalo kỹ thuật: 092 3333 365 để nhận báo giá chi tiết.
    4. ĐẶC BIỆT: Khi giới thiệu công cụ, mã sản phẩm hay bài viết nào, bạn BẮT BUỘC phải trích xuất chính xác cái "Link" đi kèm trong phần tài liệu đó và trình bày ở cuối câu trả lời dưới dạng: 
       "🔗 Anh xem hướng dẫn chi tiết và tải tài liệu tại bài viết gốc này nhé: [Dán link gốc vào đây]"
    5. Ở cuối câu trả lời, nếu thấy phù hợp, hãy giới thiệu thêm các kênh truyền thông như nhóm Facebook (https://www.facebook.com/groups/civil.engineer.vn) hoặc YouTube (@TruongPhiPhap) để anh em bấm đăng ký theo dõi.
    6. Nếu câu hỏi hoàn toàn lệch khỏi chủ đề kỹ thuật xây dựng/Lisp CAD/Excel được cung cấp, hãy lịch sự từ chối và hướng dẫn họ truy cập website chính thức https://ksxd.vn để tra cứu thêm.

    --- DỮ LIỆU KIẾN THỨC WEBSITE KSXD.VN ---
    {context}
    --- KẾT THÚC DỮ LIỆU KIẾN THỨC ---

    [CÂU HỎI CỦA THÀNH VIÊN]:
    "{user_question}"

    [CÂU TRẢ LỜI CỦA CHUYÊN GIA KSXD]:
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
            return f"❌ Lỗi kết nối bộ não AI: {str(e)}. Anh em vui lòng gửi lại câu hỏi sau vài giây nhé!"

# --- TIẾP NHẬN TIN NHẮN VÀ PHẢN HỒI ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_text = message.text
    if not user_text:
        return
        
    status_msg = bot.reply_to(message, "🔄 Em đang lục lại sổ tay kiến thức ksxd.vn để trả lời anh, chờ em vài giây nhé...")
    ai_reply = ask_gemini_with_context(user_text)
    bot.reply_to(message, ai_reply)
    
    try:
        bot.delete_message(message.chat.id, status_msg.message_id)
    except:
        pass

# --- KÍCH HOẠT SERVER WEBHOOK ---
if __name__ == "__main__":
    WEBHOOK_URL = "https://bot-telegram-ksxd-1.onrender.com"
    
    print("🔄 Đang cấu hình dọn dẹp và nạp Webhook mới...")
    bot.remove_webhook()
    time.sleep(1)
    
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    print("✅ Hệ thống Webhook chuyên gia tổng hợp đã đăng ký thành công!")
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
