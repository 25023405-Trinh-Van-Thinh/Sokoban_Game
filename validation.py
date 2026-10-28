"""Independent path validation for public and instructor tests."""
from sokoban import SokobanState, sokoban_goal_state

def signature(state):
    """Nhận một trạng thái, trả tuple gồm kích thước, robot, thùng, đích, vật cản.
Khác hashable_state, chữ ký này so sánh cả bản đồ; bỏ action/gval/parent.
Dùng để phát hiện đầu vào bị sửa và so sánh từng bước khi xác minh."""
    return (state.width, state.height, state.robots, state.boxes, state.storage, state.obstacles)

def validate_solution(initial, final):
    """Nhận initial và final; trả (bool, thông báo), không tìm lời giải.
1. final phải là SokobanState. 2. Lần ngược parent, chặn sai kiểu/vòng lặp.
3. Đảo chain về chiều đầu-cuối, đối chiếu nút đầu với initial.
4. Mỗi cặp nút phải tăng gval đúng 1 và khớp một successor hợp lệ.
5. Nút cuối phải đạt đích. Chỉ đặt thùng lên đích bằng tay không đủ.
chain: danh sách nút; seen: id đối tượng đã đi qua để phát hiện vòng.
current: nút đang lần; previous/following: hai nút kề nhau.
candidate: bước hợp lệ sinh lại từ previous. Việc sinh lại làm bộ đếm
StateSpace.n tăng, nhưng không sửa cấu hình initial hay final."""
    if not isinstance(final, SokobanState):
        return (False, 'Expected a SokobanState solution')
    # chain lưu đường đi ngược; seen lưu định danh đối tượng, không phải khóa bàn.
    chain, seen = ([], set())
    current = final
    while current is not None:
        if not isinstance(current, SokobanState) or id(current) in seen:
            return (False, 'Invalid or cyclic parent chain')
        # Đánh dấu trước khi chuyển sang cha để chặn vòng trỏ.
        seen.add(id(current))
        chain.append(current)
        current = current.parent
    # Chuyển từ cuối-đầu sang đầu-cuối để kiểm tra từng bước tiến.
    chain.reverse()
    if signature(chain[0]) != signature(initial) or chain[0].gval != initial.gval:
        return (False, 'Path does not start at the supplied initial state')
    # zip ghép (nút 0,nút 1), (nút 1,nút 2), ...
    for previous, following in zip(chain, chain[1:]):
        if following.gval != previous.gval + 1:
            return (False, 'Incorrect path cost')
        # any chỉ cần một bước được luật chơi sinh ra khớp với bước khai báo.
        if not any((candidate.action == following.action and signature(candidate) == signature(following) for candidate in previous.successors())):
            return (False, 'Illegal transition')
    if not sokoban_goal_state(final):
        return (False, 'Final state is not a goal')
    return (True, 'Valid solution')
