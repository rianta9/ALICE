class Constant:
    LANGUAGE = 'vi'
    HELP = """
    ======================================================
                       Cách Sử Dụng

    1. Mở chức năng nhận dạng giọng nói
    Cú pháp: mở nhận dạng giọng nói
    ------
    2. Tắt chức năng nhận dạng giọng nói
    Cú pháp: tắt nhận dạng giọng nói
    ------
    3. Training
    Cú pháp: trả lời reply1 hoặc reply2 hoặc reply...
    Ví dụ: khi Alice yêu cầu train dữ liệu cho message: i love you
    Cú pháp để training: trả lời i love you too hoặc i don't care
    => Ý nghĩa: Thêm ba câu trả lời: i love you, i don't care 
    vào danh sách câu trả lời cho tin nhắn i love you
    ------
    4. Thoát
    Cú pháp: [bye, goodbye, bye bye, tạm biệt]
    ------------------
    5. Mở một bài hát bất kỳ
    Cú pháp: [mở nhạc, play music, bật nhạc, open music]
    ------
    6. Đổi bài hát
    Cú pháp: [chuyển bài, next music, đổi bài hát, bật bài khác, bài hát khác]
    ------
    7. Mở một bài hát theo tên
    Cú pháp: 
     + mở bài hát {tên bài hát}
     + bật bài hát {tên bài hát}
    ------
    8. Mở online một bài hát theo tên
    Cú pháp: 
     + mở online bài hát {tên bài hát}
     + bật online bài hát {tên bài hát}
    ------
    9. Tìm bài hát theo từ khoá
    Cú pháp: tìm bài hát {một đoạn trong lời bài hát}
    Ví dụ: 
     + tìm bài hát Ngọn cỏ ven đường thôi mà làm sao với được mây
    ------
    10. Mở online 1 playlist theo chủ đề
    Cú pháp: 
     + music chủ đề {tên chủ đề}
     + mở nhạc theo chủ đề {tên chủ đề}
    Chủ đề: [ngẫu nhiên, bất kỳ, hot vpop, hot kpop, hot cpop, hot âu mỹ, hot rap, 
    hot dance, hot edm, hot bolero, lãng mạn, buồn, cà phê, chơi game, Acoustic, 
    bất hủ việt, bất hủ âu mỹ, tình yêu, không lời]
    Ví dụ:
     + music chủ đề ngẫu nhiên
     + mở nhạc theo chủ đề acoustic
    ------
    11. Chuyển sang một playlist nhạc khác
    Cú pháp: next playlist
    ------
    12. Tìm lời của một bài hát
    Cú pháp: 
     + lời bài hát {tên bài hát}
     + tìm lời bài hát {tên bài hát}
    ------------------
    13. Tìm kiếm thông tin thời tiết
    Cú pháp: thời tiết {ngày} {ở địa điểm} {thế nào}
    Ví dụ: 
     + thời tiết hôm nay thế nào
     + thời tiết thứ bảy ở Huế thế nào
    ------------------
    14. Tìm kiếm lịch chiếu phim
    Cú pháp: 
     + lịch chiếu phim {rạp chiếu} {địa điểm}
     + lịch chiếu phim {rạp chiếu} {địa điểm} {ngày}
    Ví dụ:
     + Lịch chiếu phim BHD Huế
     + Lịch chiếu phim lotte Hà Nội ngày mai
     + Lịch chiếu phim cinestar Hà Nội ngày 2/9
    ------------------
    15. Tìm kiếm một thông tin bất kỳ bằng trình duyệt
    Cú pháp:
     + tìm kiếm {từ khoá}
     + search {từ khoá}
    Ví dụ:
     + tìm kiếm trung tâm mua sắm gần đây
     + tìm kiếm atm gần đây
     + tìm kiếm thông tin của tesla
     + tìm kiếm cafe muối huế
    ------------------
    16. Tìm kiếm cách làm một thứ gì đó
    Cú pháp:
     + cách làm {từ khoá}
     + cách để {từ khoá}
     + làm sao để {từ khoá}
     + làm cách nào để {từ khoá}
     + cách {từ khoá}
    Ví dụ:
     + cách tỏ tình crush
     + cách nấu cơm
    ------------------
    17. Tìm kiếm thông tin bất kỳ
    Cú pháp:
     + {từ khoá} là gì
     + {từ khoá} là ai
     + thông tin của {từ khoá}
     + định nghĩa {từ khoá}
     + khái niệm {từ khoá}
    Ví dụ:
     + tình yêu là gì
     + bill gates là ai
    ------------------
    18. Mở một ứng dụng, phần mềm bất kỳ
    Cú pháp:
     + mở {phần mềm}
    Phần mềm hỗ trợ: google chrome, notepad, paint, cmd, calculator, task manager, 
    word, powerpoint, excel, mail, file explorer
    Master có thể vào file bookmark để lưu thêm các ứng dụng, phần mềm có trong hệ thống!
    ------------------
    19. Dịch sang tiếng anh
    Cú pháp:
     + dịch từ {từ}
     + dịch câu {câu}
    Ví dụ:
     + dịch từ love
     + dịch câu i love you
    ------------------
    20. Mở một trang web nào đó
    Cú pháp:
     + mở {tên trang web}
    Trang web hỗ trợ: facebook, youtube, google, phim mới, zing mp3, gmail...
    Master có thể vào file bookmark để lưu thêm các trang web hay dùng!
    ------------------
    21. Trò chuyện xàm xí
    Chỉ là trò chuyện xàm xí mà thôi ^^
    ======================================================
    """
    MUSIC_PATH = 'E:/Musics'
    CHROME_DRIVER = r'C:\Users\hoang\.wdm\drivers\chromedriver\win32\87.0.4280.88\chromedriver.exe'
    MAIL_ADDRESS = 'frozenkizz12@gmail.com'
    MAIL_PASS = 'abcxyz'
