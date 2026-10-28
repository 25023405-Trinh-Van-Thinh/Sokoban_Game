"""Khung trạng thái dùng chung. sokoban.py kế thừa lớp này để cài luật chơi.

Module này KHÔNG tìm lời giải: nó chỉ lưu thông tin một nút và đường đi.
"""


class StateSpace:
    """Lớp cha quy định giao diện cho các trạng thái trong bài toán tìm kiếm.

    Không dùng abc: vẫn có thể tạo đối tượng, nhưng các hàm chưa được lớp con
    cài đặt sẽ phát sinh NotImplementedError khi gọi.
    """

    n = 0  # Thuộc tính lớp: bộ đếm số trạng thái được tạo trong tiến trình.

    def __init__(self, action, gval, parent):
        """Tạo nút; action là bước vừa thực hiện, gval là chi phí tích lũy.

        parent trỏ đến nút trước; nút đầu dùng action="START", gval=0,
        parent=None. Hàm khởi tạo không trả về một giá trị tường minh.
        """
        self.action = action  # Ví dụ "0 right": robot số 0 đi sang phải.
        self.gval = gval  # Tổng số bước, gồm cả đi bộ và đẩy thùng.
        self.parent = parent  # Tham chiếu để lần ngược đường đi.
        self.index = StateSpace.n  # Mã nút để phân biệt các lần tạo đối tượng.
        StateSpace.n += 1  # Không phải số bước và không phải khóa cấu hình.

    def successors(self):
        """Lớp con phải trả các trạng thái kế hợp lệ với parent/action/gval.

        Gọi trực tiếp hàm lớp cha sẽ báo lỗi; SokobanState ghi đè hàm này.
        """
        raise NotImplementedError

    def hashable_state(self):
        """Lớp con phải trả khóa bất biến để lưu set/dict trong cùng bài toán."""
        raise NotImplementedError

    def print_state(self):
        """Lớp con phải cài cách in một trạng thái; lớp cha chưa biết bàn chơi."""
        raise NotImplementedError

    def print_path(self):
        """In từ nút đầu tới self, trả None; yêu cầu chuỗi parent không có vòng.

        path giữ các nút theo chiều ngược; current lần lượt đi về cha.
        reversed đổi thứ tự in, không thay đổi trạng thái hay chuỗi parent.
        """
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        for item in reversed(path):
            item.print_state()  # Với SokobanState, gọi hàm của lớp con.
