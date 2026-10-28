"""Small API examples only; no prescribed search algorithm."""
import unittest
import solution
from sokoban import SokobanState
from validation import signature, validate_solution

def simple_state(solved=False):
    """Tạo bàn 4x3 với một robot, một thùng, một đích; trả SokobanState.
solved=False đặt thùng (1,1), solved=True đặt thùng ngay trên đích (2,1)."""
    return SokobanState('START', 0, None, 4, 3, ((0, 1),), frozenset([(2, 1) if solved else (1, 1)]), frozenset([(2, 1)]), frozenset())

class PublicTests(unittest.TestCase):
    """Ba kiểm tra giao diện solve, không đại diện điểm chính thức.
Không có thuộc tính riêng; self kế thừa các assert của unittest.TestCase.
Các phương thức test trả None khi đạt; lỗi/assert được unittest thu thập."""

    def test_one_box(self):
        """Gọi solve với ngân sách 120 giây trên bàn cần một lần đẩy.
before lưu cấu hình/action/gval/parent để phát hiện sửa initial.
final phải vượt qua validate_solution; valid là bool, detail là lý do."""
        initial = simple_state()
        # Chụp dữ liệu trước lời gọi để so với trạng thái sau lời gọi.
        before = (signature(initial), initial.action, initial.gval, initial.parent)
        final = solution.solve(initial, timebound=120)
        self.assertEqual((signature(initial), initial.action, initial.gval, initial.parent), before)
        valid, detail = validate_solution(simple_state(), final)
        # Nếu valid=False, unittest hiện detail làm lý do thất bại.
        self.assertTrue(valid, detail)

    def test_initial_goal(self):
        """Bàn đã giải ngay từ đầu: solve phải trả đường đi hợp lệ đến đích.
Có thể trả initial vì chuỗi chỉ gồm một nút đã thỏa điều kiện."""
        initial = simple_state(solved=True)
        final = solution.solve(initial, timebound=120)
        valid, detail = validate_solution(simple_state(solved=True), final)
        # Nếu valid=False, unittest hiện detail làm lý do thất bại.
        self.assertTrue(valid, detail)

    def test_zero_budget(self):
        """Bàn chưa giải và timebound=0: phải trả đúng False.
assertIs kiểm tra định danh nên None hoặc số 0 không thay thế được False."""
        self.assertIs(solution.solve(simple_state(), timebound=0), False)
if __name__ == '__main__':
    unittest.main()
