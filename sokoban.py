"""Mô hình và luật Sokoban; dùng StateSpace trong state.py.

solution.py sẽ dùng successors để tìm kiếm; validation.py dùng lại luật này
để kiểm tra từng bước. Không có thuật toán giải tự động trong module này.
"""
from state import StateSpace


class SokobanState(StateSpace):
    """Một ảnh chụp bàn chơi, kèm thông tin đường đi kế thừa từ StateSpace.

    Tọa độ (x, y): x tăng sang phải, y tăng xuống dưới, bắt đầu từ 0.
    Các cấu hình hợp lệ do framework cung cấp; constructor không tự kiểm tra
    tọa độ, kiểu dữ liệu hay việc các đối tượng chồng lên nhau.
    """

    def __init__(self, action, gval, parent, width, height, robots,
                 boxes, storage, obstacles):
        """Nhận thông tin nút và bàn chơi; lưu các giá trị, không tìm đường.

        robots là tuple tọa độ có thứ tự (chỉ số chính là danh tính robot).
        boxes/storage/obstacles là frozenset tọa độ không có thứ tự.
        """
        StateSpace.__init__(self, action, gval, parent)
        self.width = width  # Số cột bên trong, không tính viền tường khi in.
        self.height = height  # Số hàng bên trong.
        self.robots = robots  # robots[i] là vị trí robot i.
        self.boxes = boxes  # Vị trí thùng đang thay đổi qua các bước.
        self.storage = storage  # Các ô đích cố định; có thể dư ô đích.
        self.obstacles = obstacles  # Vật cản cố định nằm bên trong bàn.

    def successors(self):
        """Trả list mọi nút kế hợp lệ; mỗi nút tương ứng MỘT robot đi MỘT ô.

        Thử từng robot theo bốn hướng. Loại bước ra ngoài, gặp tường/robot.
        Nếu gặp thùng, kiểm tra thêm ô sau thùng. Chỉ tạo nút khi hợp lệ.
        Không sửa self: sao chép robots/boxes trước khi thay đổi.
        """
        successors = []  # Danh sách kết quả; không phải lời giải nhiều bước.
        transition_cost = 1  # Đi bộ hay đẩy đều có cùng chi phí.
        for robot in range(0, len(self.robots)):
            for direction in (UP, RIGHT, DOWN, LEFT):
                new_location = direction.move(self.robots[robot])
                # Tạm bỏ robot đang đi để kiểm tra va chạm với robot còn lại.
                new_robots = list(self.robots)
                new_robots.remove(self.robots[robot])
                new_robots = tuple(new_robots)
                new_boxes = set(self.boxes)  # Bản sao có thể thêm/xóa phần tử.
                if new_location[0] < 0 or new_location[0] >= self.width:
                    continue
                if new_location[1] < 0 or new_location[1] >= self.height:
                    continue
                if new_location in self.obstacles:
                    continue
                if new_location in new_robots:
                    continue

                if new_location in self.boxes:
                    new_box_location = direction.move(new_location)
                    # Không kéo thùng; không đẩy ra biên hay đẩy hai thùng.
                    if new_box_location[0] < 0 or new_box_location[0] >= self.width:
                        continue
                    if new_box_location[1] < 0 or new_box_location[1] >= self.height:
                        continue
                    if new_box_location in self.obstacles:
                        continue
                    if new_box_location in new_robots:
                        continue
                    if new_box_location in new_boxes:
                        continue
                    new_boxes.remove(new_location)
                    new_boxes.add(new_box_location)

                # Khôi phục đủ robot và giữ nguyên thứ tự danh tính của chúng.
                new_robots = list(self.robots)
                new_robots[robot] = new_location
                new_robots = tuple(new_robots)
                new_state = SokobanState(
                    str(robot) + " " + direction.name,
                    self.gval + transition_cost, self, self.width, self.height,
                    new_robots, frozenset(new_boxes), self.storage, self.obstacles)
                # parent=self nối nút mới với đường đi đã có.
                successors.append(new_state)
        return successors

    def hashable_state(self):
        """Trả (robots, boxes) để nhận ra cấu hình đã gặp trong CÙNG map.

        Không đưa gval/parent/index vào khóa: cùng bàn có thể tới từ nhiều
        đường. Không dùng chung bảng visited cho các map khác nhau.
        """
        return (self.robots, self.boxes)

    def state_string(self):
        """Trả chuỗi bàn chơi có viền và xuống dòng, không tự in.

        '.' đích; '#' tường; '$' thùng; '*' thùng trên đích;
        a,b,... robot; A,B,... robot trên đích; khoảng trắng là ô trống.
        Danh sách map truy cập theo [y][x], khác thứ tự tọa độ (x,y).
        """
        map = []  # Biến cục bộ trong mã gốc, che tên hàm built-in map.
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row += [' ']
            map += [row]
        for storage_point in self.storage:
            map[storage_point[1]][storage_point[0]] = '.'
        for obstacle in self.obstacles:
            map[obstacle[1]][obstacle[0]] = '#'
        for i, robot in enumerate(self.robots):
            if robot in self.storage:
                map[robot[1]][robot[0]] = chr(ord('A') + i)
            else:
                map[robot[1]][robot[0]] = chr(ord('a') + i)
        for box in self.boxes:
            if box in self.storage:
                map[box[1]][box[0]] = '*'
            else:
                map[box[1]][box[0]] = '$'
        # Viền chỉ phục vụ hiển thị; kiểm tra biên đã nằm trong successors.
        for y in range(0, self.height):
            map[y] = ['#'] + map[y]
            map[y] = map[y] + ['#']
        map = ['#' * (self.width + 2)] + map
        map = map + ['#' * (self.width + 2)]
        s = ''
        for row in map:
            for char in row:
                s += char
            s += '\n'
        return s

    def print_state(self):
        """In action và bàn chơi ra terminal, trả None; print_path gọi hàm này."""
        print("ACTION was " + self.action)
        print(self.state_string())


def sokoban_goal_state(state):
    """Nhận SokobanState, trả bool: tất cả thùng nằm trong storage.

    Không yêu cầu mọi ô đích được lấp, không xét vị trí robot, không xác minh
    đường đi. Vì thế validation.py còn phải kiểm tra chuỗi parent.
    """
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


# 20 bàn thực hành từ PDF gốc; chỉ số 0..19, không phải test ẩn.
# Mỗi bàn: action, gval, parent, width, height, robots, boxes, storage, obstacles.
PROBLEMS = (
    SokobanState("START", 0, None, 5, 5, # dimensions
                 ((2, 1), (2, 3)), #robots
                 frozenset(((1, 1), (1, 3), (3, 1), (3, 3))), #boxes
                  frozenset(((0, 0), (0, 4), (4, 0), (4, 4))), #storage
                  frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3,
4))) #obstacles
                 ),
    SokobanState("START", 0, None, 5, 5, # dimensions
                 ((2, 1), (2, 3)), #robots
                 frozenset(((1, 1),)), #boxes
                 frozenset(((0, 0),)), #storage
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3,
4))) #obstacles
                 ),
    SokobanState("START", 0, None, 5, 5, # dimensions
                 ((2, 2),), #robots
                 frozenset(((1, 1), (1, 3), (3, 1), (3, 3))), #boxes
                 frozenset(((0, 0), (0, 4), (4, 0), (4, 4))), #storage
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3,
4))) #obstacles
                 ),
    SokobanState("START", 0, None, 6, 4, # dimensions
                 ((2, 1), (2, 2)), #robots
                 frozenset(((1, 1), (4, 2))), #boxes
                 frozenset(((2, 1), (2, 2))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 4, # dimensions
                 ((2, 1), (2, 2)), #robots
                 frozenset(((4, 2),)), #boxes
                 frozenset(((2, 1),)), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 5, 5, # dimensions
                 ((4, 0), (4, 4)), #robots
                 frozenset(((3, 1), (3, 2), (3, 3))), #boxes
                 frozenset(((0, 0), (0, 2), (0, 4))), #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))) #obstacles
                 ),
    SokobanState("START", 0, None, 5, 5, # dimensions
                 ((4, 0), (4, 4)), #robots
                 frozenset(((3, 1), (3, 2))), #boxes
                 frozenset(((0, 0), (0, 2))), #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))) #obstacles
                 ),
    SokobanState("START", 0, None, 5, 5, # dimensions
                 ((4, 0),), #robots
                 frozenset(((3, 1), (3, 2), (3, 3))), #boxes
                 frozenset(((0, 0), (0, 2), (0, 4))), #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))) #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((0, 0), (0, 2), (0, 4)), #robots
                 frozenset(((1, 0), (1, 2), (1, 4))), #boxes
                 frozenset(((5, 0), (5, 2), (0, 5))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((0, 0), (0, 2), (0, 4), (5, 5)), #robots
                 frozenset(((1, 0), (4, 1), (1, 2), (4, 3), (1, 4), (4,
5))), #boxes
                 frozenset(((5, 0), (0, 1), (5, 2), (0, 3), (5, 4), (0,
5))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((5, 5), (5, 4), (4, 5)), #robots
                 frozenset(((3, 1), (2, 2), (1, 4), (3, 4))), #boxes
                 frozenset(((0, 0), (0, 1), (1, 0), (1, 1))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((5, 5), (5, 4), (4, 5)), #robots
                 frozenset(((3, 1), (1, 4), (3, 4))), #boxes
                 frozenset(((0, 0), (0, 1), (1, 0))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((5, 5), (5, 4), (4, 5)), #robots
                 frozenset(((3, 1), (2, 2), (1, 4))), #boxes
                 frozenset(((0, 0), (0, 1), (1, 0))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((5, 5), (5, 4)), #robots
                 frozenset(((3, 1), (1, 4), (3, 4))), #boxes
                 frozenset(((0, 0), (0, 1), (1, 0))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 6, 6, # dimensions
                 ((5, 5), (5, 4)), #robots
                 frozenset(((3, 1), (2, 2), (1, 4))), #boxes
                 frozenset(((0, 0), (0, 1), (1, 0))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 8, 8, # dimensions
                 ((0, 5), (1, 6), (2, 7)), #robots
                 frozenset(((5, 6), (4, 5), (6, 2), (5, 2), (4, 6))),
#boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0,
2))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 8, 8, # dimensions
                 ((0, 5), (1, 6), (2, 7)), #robots
                 frozenset(((6, 2), (5, 6), (4, 4), (6, 3))), #boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0,
2))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 8, 8, # dimensions
                 ((0, 5), (1, 6), (2, 7)), #robots
                 frozenset(((5, 4), (5, 5), (6, 3), (4, 2), (6, 5), (5,
3))), #boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0,
2))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 8, 8, # dimensions
                 ((0, 5), (1, 6), (2, 7)), #robots
                 frozenset(((6, 6), (5, 6), (6, 2), (4, 3), (5, 1), (6,
5))), #boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0,
2))), #storage
                 frozenset() #obstacles
                 ),
    SokobanState("START", 0, None, 8, 8, # dimensions
                 ((0, 5), (1, 6), (2, 7)), #robots
                 frozenset(((6, 6), (4, 5), (4, 1), (4, 3), (5, 2), (5,
3))), #boxes
                 frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0,
2))), #storage
                 frozenset() #obstacles
                 )
    )




class Direction:
    """Biểu diễn hướng; successors dùng move và name để tạo trạng thái con."""

    def __init__(self, name, delta):
        """Nhận tên hướng và độ lệch (dx, dy); chỉ lưu dữ liệu, trả None."""
        self.name = name  # Chuỗi up/right/down/left để tạo nhãn action.
        self.delta = delta  # Tuple độ lệch tọa độ cho một bước.

    def __hash__(self):
        """Trả hash của tên để dùng trong set/dict, không quyết định luật đi.

        Lớp gốc không định nghĩa __eq__: hai đối tượng cùng tên chưa chắc bằng
        nhau. Không sửa name sau khi đã dùng đối tượng làm khóa.
        """
        return hash(self.name)

    def __str__(self):
        """Trả tên khi gọi str(direction) hoặc print(direction)."""
        return str(self.name)

    def __repr__(self):
        """Trả tên khi xem đối tượng trong list/tuple hoặc trình gỡ lỗi."""
        return self.__str__()

    def move(self, location):
        """Nhận (x,y), trả (x+dx,y+dy); không kiểm tra biên, tường hay thùng.

        Ví dụ RIGHT.move((1,1)) trả (2,1). successors chịu trách nhiệm
        xác định tọa độ mới có thực sự đi được hay không.
        """
        return (location[0] + self.delta[0], location[1] + self.delta[1])


# Hằng dùng chung: tọa độ y tăng xuống dưới.
UP = Direction("up", (0, -1))  # Lên: giảm y.
RIGHT = Direction("right", (1, 0))  # Phải: tăng x.
DOWN = Direction("down", (0, 1))  # Xuống: tăng y.
LEFT = Direction("left", (-1, 0))  # Trái: giảm x.
