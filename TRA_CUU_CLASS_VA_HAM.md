# Tra cứu toàn bộ class và hàm

Các mô tả dưới đây được trích từ chính mã chú thích. Mở file tại số dòng ghi bên dưới để đọc phần thực thi.

## autograder.py

### main()

Vị trí: autograder.py, dòng 9.

Điểm chạy bộ kiểm tra công khai; trả mã thoát 0 nếu tất cả đạt, ngược lại 1.
parser/args đọc --test và --json. root là thư mục chứa file này.
tree là AST public_tests.py; names là tên test lấy từ class PublicTests.
Đọc AST tránh import mã sinh viên ngay trong tiến trình điều phối.
Mỗi name được chạy bằng sys.executable trong tiến trình riêng, timeout 120s.
run giữ kết quả subprocess; status là PASS/FAIL/TIMEOUT; detail là đầu ra.
results chứa các dict kết quả; passed đếm PASS; payload là dữ liệu JSON.
--test không hợp lệ báo lỗi argparse; --json ghi báo cáo nếu được yêu cầu.
Giới hạn cứng của bộ chạy khác timebound do solver tự quản lý.
Chỉ framework chấm dùng subprocess; bài nộp solution không tạo tiến trình.

## demo_logic.py

### main()

Vị trí: demo_logic.py, dòng 6.

Tạo bàn nhỏ, chọn bước phải, in đường đi và xác minh; trả None.

initial là nút đầu; before lưu chữ ký để kiểm tra không sửa đầu vào.
successors là các nút kế; final là nút sau bước 0 right.
valid/detail là bool và thông báo kiểm chứng từ validation.

## public_tests.py

### simple_state(solved=False)

Vị trí: public_tests.py, dòng 7.

Tạo bàn 4x3 với một robot, một thùng, một đích; trả SokobanState.
solved=False đặt thùng (1,1), solved=True đặt thùng ngay trên đích (2,1).

### PublicTests (class)

Vị trí: public_tests.py, dòng 12.

Ba kiểm tra giao diện solve, không đại diện điểm chính thức.
Không có thuộc tính riêng; self kế thừa các assert của unittest.TestCase.
Các phương thức test trả None khi đạt; lỗi/assert được unittest thu thập.

### PublicTests.test_one_box(self)

Vị trí: public_tests.py, dòng 17.

Gọi solve với ngân sách 120 giây trên bàn cần một lần đẩy.
before lưu cấu hình/action/gval/parent để phát hiện sửa initial.
final phải vượt qua validate_solution; valid là bool, detail là lý do.

### PublicTests.test_initial_goal(self)

Vị trí: public_tests.py, dòng 30.

Bàn đã giải ngay từ đầu: solve phải trả đường đi hợp lệ đến đích.
Có thể trả initial vì chuỗi chỉ gồm một nút đã thỏa điều kiện.

### PublicTests.test_zero_budget(self)

Vị trí: public_tests.py, dòng 39.

Bàn chưa giải và timebound=0: phải trả đúng False.
assertIs kiểm tra định danh nên None hoặc số 0 không thay thế được False.

## sokoban.py

### SokobanState (class)

Vị trí: sokoban.py, dòng 9.

Một ảnh chụp bàn chơi, kèm thông tin đường đi kế thừa từ StateSpace.

Tọa độ (x, y): x tăng sang phải, y tăng xuống dưới, bắt đầu từ 0.
Các cấu hình hợp lệ do framework cung cấp; constructor không tự kiểm tra
tọa độ, kiểu dữ liệu hay việc các đối tượng chồng lên nhau.

### SokobanState.__init__(self, action, gval, parent, width, height, robots, boxes, storage, obstacles)

Vị trí: sokoban.py, dòng 17.

Nhận thông tin nút và bàn chơi; lưu các giá trị, không tìm đường.

robots là tuple tọa độ có thứ tự (chỉ số chính là danh tính robot).
boxes/storage/obstacles là frozenset tọa độ không có thứ tự.

### SokobanState.successors(self)

Vị trí: sokoban.py, dòng 32.

Trả list mọi nút kế hợp lệ; mỗi nút tương ứng MỘT robot đi MỘT ô.

Thử từng robot theo bốn hướng. Loại bước ra ngoài, gặp tường/robot.
Nếu gặp thùng, kiểm tra thêm ô sau thùng. Chỉ tạo nút khi hợp lệ.
Không sửa self: sao chép robots/boxes trước khi thay đổi.

### SokobanState.hashable_state(self)

Vị trí: sokoban.py, dòng 86.

Trả (robots, boxes) để nhận ra cấu hình đã gặp trong CÙNG map.

Không đưa gval/parent/index vào khóa: cùng bàn có thể tới từ nhiều
đường. Không dùng chung bảng visited cho các map khác nhau.

### SokobanState.state_string(self)

Vị trí: sokoban.py, dòng 94.

Trả chuỗi bàn chơi có viền và xuống dòng, không tự in.

'.' đích; '#' tường; '$' thùng; '*' thùng trên đích;
a,b,... robot; A,B,... robot trên đích; khoảng trắng là ô trống.
Danh sách map truy cập theo [y][x], khác thứ tự tọa độ (x,y).

### SokobanState.print_state(self)

Vị trí: sokoban.py, dòng 134.

In action và bàn chơi ra terminal, trả None; print_path gọi hàm này.

### sokoban_goal_state(state)

Vị trí: sokoban.py, dòng 140.

Nhận SokobanState, trả bool: tất cả thùng nằm trong storage.

Không yêu cầu mọi ô đích được lấp, không xét vị trí robot, không xác minh
đường đi. Vì thế validation.py còn phải kiểm tra chuỗi parent.

### Direction (class)

Vị trí: sokoban.py, dòng 294.

Biểu diễn hướng; successors dùng move và name để tạo trạng thái con.

### Direction.__init__(self, name, delta)

Vị trí: sokoban.py, dòng 297.

Nhận tên hướng và độ lệch (dx, dy); chỉ lưu dữ liệu, trả None.

### Direction.__hash__(self)

Vị trí: sokoban.py, dòng 302.

Trả hash của tên để dùng trong set/dict, không quyết định luật đi.

Lớp gốc không định nghĩa __eq__: hai đối tượng cùng tên chưa chắc bằng
nhau. Không sửa name sau khi đã dùng đối tượng làm khóa.

### Direction.__str__(self)

Vị trí: sokoban.py, dòng 310.

Trả tên khi gọi str(direction) hoặc print(direction).

### Direction.__repr__(self)

Vị trí: sokoban.py, dòng 314.

Trả tên khi xem đối tượng trong list/tuple hoặc trình gỡ lỗi.

### Direction.move(self, location)

Vị trí: sokoban.py, dòng 318.

Nhận (x,y), trả (x+dx,y+dy); không kiểm tra biên, tường hay thùng.

Ví dụ RIGHT.move((1,1)) trả (2,1). successors chịu trách nhiệm
xác định tọa độ mới có thực sự đi được hay không.

## solution.py

### solve(initial_state, timebound=120)

Vị trí: solution.py, dòng 7.

Nơi sinh viên cài thuật toán tìm lời giải Sokoban.

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

## state.py

### StateSpace (class)

Vị trí: state.py, dòng 7.

Lớp cha quy định giao diện cho các trạng thái trong bài toán tìm kiếm.

Không dùng abc: vẫn có thể tạo đối tượng, nhưng các hàm chưa được lớp con
cài đặt sẽ phát sinh NotImplementedError khi gọi.

### StateSpace.__init__(self, action, gval, parent)

Vị trí: state.py, dòng 16.

Tạo nút; action là bước vừa thực hiện, gval là chi phí tích lũy.

parent trỏ đến nút trước; nút đầu dùng action="START", gval=0,
parent=None. Hàm khởi tạo không trả về một giá trị tường minh.

### StateSpace.successors(self)

Vị trí: state.py, dòng 28.

Lớp con phải trả các trạng thái kế hợp lệ với parent/action/gval.

Gọi trực tiếp hàm lớp cha sẽ báo lỗi; SokobanState ghi đè hàm này.

### StateSpace.hashable_state(self)

Vị trí: state.py, dòng 35.

Lớp con phải trả khóa bất biến để lưu set/dict trong cùng bài toán.

### StateSpace.print_state(self)

Vị trí: state.py, dòng 39.

Lớp con phải cài cách in một trạng thái; lớp cha chưa biết bàn chơi.

### StateSpace.print_path(self)

Vị trí: state.py, dòng 43.

In từ nút đầu tới self, trả None; yêu cầu chuỗi parent không có vòng.

path giữ các nút theo chiều ngược; current lần lượt đi về cha.
reversed đổi thứ tự in, không thay đổi trạng thái hay chuỗi parent.

## test_framework.py

### board(robots=((0, 1),), boxes=((1, 1),), storage=((2, 1),), obstacles=())

Vị trí: test_framework.py, dòng 7.

Tạo SokobanState 4x3 để kiểm tra luật, trả nút START có gval=0.
robots/boxes/storage/obstacles là các tọa độ có thể truyền đè.
Mặc định robot (0,1), thùng (1,1), đích (2,1): một lần đẩy phải là xong.

### FrameworkTests (class)

Vị trí: test_framework.py, dòng 13.

Bộ unittest kiểm tra framework, không gọi solution.solve.
Không khai báo thuộc tính riêng; self dùng các assert kế thừa TestCase.
Mỗi test trả None khi đạt; assert sai tạo failure để unittest báo lỗi.

### FrameworkTests.test_push_and_cost(self)

Vị trí: test_framework.py, dòng 18.

Sinh bước 0 right, kiểm tra đạt đích, chi phí 1, parent trỏ đúng.
before lưu chữ ký start để chắc chắn successors không sửa đầu vào.
Cuối cùng yêu cầu validate_solution chấp nhận đường đi.

### FrameworkTests.test_no_double_push(self)

Vị trí: test_framework.py, dòng 31.

Đặt hai thùng liền nhau; danh sách hành động không được có 0 right.

### FrameworkTests.test_robot_blocks_push(self)

Vị trí: test_framework.py, dòng 35.

Đặt robot thứ hai sau thùng; robot đầu không được đẩy vào robot đó.

### FrameworkTests.test_obstacle_blocks_push(self)

Vị trí: test_framework.py, dòng 40.

Đặt vật cản sau thùng; loại hành động đẩy phải.

### FrameworkTests.test_multiple_robots_move_one_at_a_time(self)

Vị trí: test_framework.py, dòng 44.

Với mỗi successor, đếm robot đổi vị trí bằng zip; phải đúng 1.
Đồng thời gval của bước đầu phải bằng 1, dù bàn có nhiều robot.

### FrameworkTests.test_state_key_and_storage(self)

Vị trí: test_framework.py, dòng 52.

Kiểm tra khóa là tuple, dư ô đích vẫn thắng, bộ PROBLEMS có 20 bàn.

### FrameworkTests.test_validator_rejects_forgery(self)

Vị trí: test_framework.py, dòng 59.

Thử nút đích giả không nối từ initial, rồi action sai, rồi parent tự trỏ.
Cả ba phải bị từ chối; forged là đối tượng cố tình bị sửa cho test.

## validation.py

### signature(state)

Vị trí: validation.py, dòng 4.

Nhận một trạng thái, trả tuple gồm kích thước, robot, thùng, đích, vật cản.
Khác hashable_state, chữ ký này so sánh cả bản đồ; bỏ action/gval/parent.
Dùng để phát hiện đầu vào bị sửa và so sánh từng bước khi xác minh.

### validate_solution(initial, final)

Vị trí: validation.py, dòng 10.

Nhận initial và final; trả (bool, thông báo), không tìm lời giải.
1. final phải là SokobanState. 2. Lần ngược parent, chặn sai kiểu/vòng lặp.
3. Đảo chain về chiều đầu-cuối, đối chiếu nút đầu với initial.
4. Mỗi cặp nút phải tăng gval đúng 1 và khớp một successor hợp lệ.
5. Nút cuối phải đạt đích. Chỉ đặt thùng lên đích bằng tay không đủ.
chain: danh sách nút; seen: id đối tượng đã đi qua để phát hiện vòng.
current: nút đang lần; previous/following: hai nút kề nhau.
candidate: bước hợp lệ sinh lại từ previous. Việc sinh lại làm bộ đếm
StateSpace.n tăng, nhưng không sửa cấu hình initial hay final.
