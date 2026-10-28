"""Ví dụ bổ sung: một lần đẩy; không phải thuật toán giải hay bài nộp."""
from sokoban import SokobanState, sokoban_goal_state
from validation import signature, validate_solution


def main():
    """Tạo bàn nhỏ, chọn bước phải, in đường đi và xác minh; trả None.

    initial là nút đầu; before lưu chữ ký để kiểm tra không sửa đầu vào.
    successors là các nút kế; final là nút sau bước 0 right.
    valid/detail là bool và thông báo kiểm chứng từ validation.
    """
    initial = SokobanState(
        "START", 0, None, 4, 3, ((0, 1),),
        frozenset({(1, 1)}), frozenset({(2, 1)}), frozenset())
    before = signature(initial)
    successors = initial.successors()
    print("Các hành động hợp lệ:", [s.action for s in successors])
    final = next(s for s in successors if s.action == "0 right")
    final.print_path()
    valid, detail = validate_solution(initial, final)
    print("Đạt đích:", sokoban_goal_state(final))
    print("Số bước:", final.gval)
    print("Parent đúng:", final.parent is initial)
    print("Đầu vào giữ nguyên:", signature(initial) == before)
    print("Kiểm tra:", valid, detail)


if __name__ == "__main__":
    main()
