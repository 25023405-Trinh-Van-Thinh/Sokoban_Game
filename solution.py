"""Điểm vào của bài làm: public_tests.py gọi solve trong module này.

Bản PDF gốc chỉ có khung hàm. Bản chú thích giữ nguyên hành vi đó.
"""


def solve(initial_state, timebound=120):
    """Nơi sinh viên cài thuật toán tìm lời giải Sokoban.

    initial_state: SokobanState hợp lệ, gval=0 và parent=None theo đề.
    timebound: ngân sách giây, mặc định 120; không phải số bước.
    Kết quả cần cài: nút đích với chuỗi parent/action/gval hợp lệ; hoặc đúng
    giá trị False khi không tìm được lời giải trong giới hạn.

    Gợi ý logic: quản lý tập nút chờ, lấy một nút, kiểm tra đích, gọi
    successors(), dùng hashable_state() tránh lặp, rồi tiếp tục.
    Phải theo dõi thời gian; không sửa initial_state. Nếu ban đầu đã là
    đích có thể trả chính nó. Trường hợp chưa giải và timebound=0 trả False.

    HIỆN TẠI: chưa có thuật toán, luôn ném NotImplementedError như PDF.
    Đây là chỗ cần hoàn thiện; chú thích không phải mã thực thi.
    """
    raise NotImplementedError("Implement your Sokoban solver")
