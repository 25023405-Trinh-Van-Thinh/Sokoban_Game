# Nguồn và kiểm tra

## Nguồn khôi phục

Thư mục: https://drive.google.com/drive/folders/1c8S_T3WaOgSnKMm5ZF3mhqrvqRdfMMKG

+- state.pdf: https://drive.google.com/file/d/1JWQ50-51BuUidp13pmt6BKKgLrbWoqJp/view
- sokoban.pdf: https://drive.google.com/file/d/1XzSF3YLzf7o_gXyRXQFw_JmzqB3sikJc/view
- solution.pdf: https://drive.google.com/file/d/1VPnF_AY-r8IyHVam_JwevqE3s693dzx-/view
- validation.pdf: https://drive.google.com/file/d/1Aps6AWoaIpxKhyA1xGHY98RDh6YXcNwh/view
- test_framework.pdf: https://drive.google.com/file/d/1aHIcuDbR4_vcGt4Y5Lx_iG7H8DKSXdD5/view
- public_test.pdf: https://drive.google.com/file/d/1tG9wh9P7zlLJt9-Y9OTUFPHM1mRsMPLH/view
- autograder.pdf: https://drive.google.com/file/d/1mQlx2sG1np_D_OwslCsMC4JpyyTM6EXL/view
- README.pdf: https://drive.google.com/file/d/1-I2_Itbz2mwTKkXo0OoFlKqWvjgAi9qa/view

## Phạm vi thay đổi

- Khôi phục Python từ PDF, không có file .py gốc để so sánh byte-for-byte.
- Sửa xuống dòng giữa chuỗi, biểu thức điều kiện và độ thụt đầu dòng.
- Chuẩn hóa đoạn utf-8 bị ngắt dòng trong autograder.
- public_test.pdf được đặt tên public_tests.py để khớp import của bộ chạy.
- Giữ 20 cấu hình PROBLEMS, các điều kiện luật chơi và nội dung assert theo PDF.
- Thêm chú thích tiếng Việt cho mọi class/hàm và thuộc tính do dự án định nghĩa.
- Thêm demo_logic.py và README hướng dẫn; demo chỉ chọn một bước để minh họa.
- solve vẫn ném NotImplementedError đúng như tài liệu gốc; không bổ sung solver.
- Các bản sao PDF trùng tên trên Drive không được đưa lặp vào gói.

## Kiểm tra đã thực hiện

- Biên dịch cú pháp toàn bộ các file Python: đạt.
- 7 kiểm tra test_framework: đạt 7/7.
- demo_logic: đạt đích sau 1 bước; parent đúng; đầu vào giữ nguyên; validator chấp nhận.
- autograder với tùy chọn JSON: chạy được, báo 0/3 như dự kiến vì solve chưa cài.
- Không khẳng định đã giải 20 bàn hoặc vượt qua test ẩn.

Người học nên đọc README.md trước rồi mở từng file .py để xem giải thích tại chỗ.
