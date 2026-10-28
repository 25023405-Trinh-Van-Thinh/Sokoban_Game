"""Tests of supplied game mechanics only; no student algorithms
needed."""
import unittest
from sokoban import SokobanState, sokoban_goal_state, PROBLEMS
from validation import validate_solution, signature

def board(robots=((0, 1),), boxes=((1, 1),), storage=((2, 1),), obstacles=()):
    """Tạo SokobanState 4x3 để kiểm tra luật, trả nút START có gval=0.
robots/boxes/storage/obstacles là các tọa độ có thể truyền đè.
Mặc định robot (0,1), thùng (1,1), đích (2,1): một lần đẩy phải là xong."""
    return SokobanState('START', 0, None, 4, 3, robots, frozenset(boxes), frozenset(storage), frozenset(obstacles))

class FrameworkTests(unittest.TestCase):
    """Bộ unittest kiểm tra framework, không gọi solution.solve.
Không khai báo thuộc tính riêng; self dùng các assert kế thừa TestCase.
Mỗi test trả None khi đạt; assert sai tạo failure để unittest báo lỗi."""

    def test_push_and_cost(self):
        """Sinh bước 0 right, kiểm tra đạt đích, chi phí 1, parent trỏ đúng.
before lưu chữ ký start để chắc chắn successors không sửa đầu vào.
Cuối cùng yêu cầu validate_solution chấp nhận đường đi."""
        start = board()
        before = signature(start)
        goal = next((s for s in start.successors() if s.action == '0 right'))
        self.assertTrue(sokoban_goal_state(goal))
        self.assertEqual(goal.gval, 1)
        self.assertIs(goal.parent, start)
        self.assertEqual(signature(start), before)
        self.assertTrue(validate_solution(start, goal)[0])

    def test_no_double_push(self):
        """Đặt hai thùng liền nhau; danh sách hành động không được có 0 right."""
        self.assertNotIn('0 right', [s.action for s in board(boxes=((1, 1), (2, 1))).successors()])

    def test_robot_blocks_push(self):
        """Đặt robot thứ hai sau thùng; robot đầu không được đẩy vào robot đó."""
        start = board(robots=((0, 1), (2, 1)))
        self.assertNotIn('0 right', [s.action for s in start.successors()])

    def test_obstacle_blocks_push(self):
        """Đặt vật cản sau thùng; loại hành động đẩy phải."""
        self.assertNotIn('0 right', [s.action for s in board(obstacles=((2, 1),)).successors()])

    def test_multiple_robots_move_one_at_a_time(self):
        """Với mỗi successor, đếm robot đổi vị trí bằng zip; phải đúng 1.
Đồng thời gval của bước đầu phải bằng 1, dù bàn có nhiều robot."""
        start = board(robots=((0, 1), (3, 2)))
        for successor in start.successors():
            self.assertEqual(sum((a != b for a, b in zip(start.robots, successor.robots))), 1)
            self.assertEqual(successor.gval, 1)

    def test_state_key_and_storage(self):
        """Kiểm tra khóa là tuple, dư ô đích vẫn thắng, bộ PROBLEMS có 20 bàn."""
        start = board(boxes=((2, 1),), storage=((2, 1), (3, 2)))
        self.assertIsInstance(start.hashable_state(), tuple)
        self.assertTrue(sokoban_goal_state(start))
        self.assertEqual(len(PROBLEMS), 20)

    def test_validator_rejects_forgery(self):
        """Thử nút đích giả không nối từ initial, rồi action sai, rồi parent tự trỏ.
Cả ba phải bị từ chối; forged là đối tượng cố tình bị sửa cho test."""
        initial, forged = (board(), board(boxes=((2, 1),)))
        self.assertFalse(validate_solution(initial, forged)[0])
        forged.parent, forged.gval, forged.action = (initial, 1, 'illegal')
        self.assertFalse(validate_solution(initial, forged)[0])
        forged.parent = forged
        self.assertFalse(validate_solution(initial, forged)[0])
if __name__ == '__main__':
    unittest.main()
