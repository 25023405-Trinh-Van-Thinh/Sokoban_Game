"""Run each public test in a fresh subprocess with a hard timeout."""
import argparse
import ast
import json
from pathlib import Path
import subprocess
import sys

def main():
    """Điểm chạy bộ kiểm tra công khai; trả mã thoát 0 nếu tất cả đạt, ngược lại 1.
parser/args đọc --test và --json. root là thư mục chứa file này.
tree là AST public_tests.py; names là tên test lấy từ class PublicTests.
Đọc AST tránh import mã sinh viên ngay trong tiến trình điều phối.
Mỗi name được chạy bằng sys.executable trong tiến trình riêng, timeout 120s.
run giữ kết quả subprocess; status là PASS/FAIL/TIMEOUT; detail là đầu ra.
results chứa các dict kết quả; passed đếm PASS; payload là dữ liệu JSON.
--test không hợp lệ báo lỗi argparse; --json ghi báo cáo nếu được yêu cầu.
Giới hạn cứng của bộ chạy khác timebound do solver tự quản lý.
Chỉ framework chấm dùng subprocess; bài nộp solution không tạo tiến trình."""
    # Đọc lựa chọn từ terminal; không gọi solve trực tiếp ở đây.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--test', help='One PublicTests method, e.g. test_one_box')
    parser.add_argument('--json', type=Path, help='Optional JSON results file')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    # Phân tích mã nguồn thành cây cú pháp, chưa thực thi nội dung file.
    tree = ast.parse((root / 'public_tests.py').read_text(encoding='utf-8'))
    # cls là nút class, node là hàm con; lọc đúng PublicTests và tiền tố test_.
    names = sorted((node.name for cls in tree.body if isinstance(cls, ast.ClassDef) and cls.name == 'PublicTests' for node in cls.body if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')))
    if args.test:
        if args.test not in names:
            parser.error('Unknown public test: ' + args.test)
        names = [args.test]
    results = []
    for name in names:
        try:
            # Mỗi test dùng tiến trình mới; stdout/stderr được thu để báo lỗi.
            run = subprocess.run([sys.executable, '-m', 'unittest', 'public_tests.PublicTests.' + name], cwd=root, capture_output=True, text=True, errors='replace', timeout=120)
            status = 'PASS' if run.returncode == 0 else 'FAIL'
            detail = run.stdout + run.stderr
        except subprocess.TimeoutExpired:
            status, detail = ('TIMEOUT', 'Exceeded public test safety limit (120 seconds).')
        results.append(dict(test=name, status=status, detail=detail))
        print('{} {}'.format(status, name))
        if status != 'PASS':
            print(detail.strip())
    passed = sum((item['status'] == 'PASS' for item in results))
    payload = dict(kind='public_feedback_only', passed=passed, total=len(results), results=results)
    # Chỉ ghi báo cáo khi người chạy truyền đường dẫn --json.
    if args.json:
        args.json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    print('\nPublic feedback: {}/{}. This is NOT the official grade.'.format(passed, len(results)))
    return 0 if passed == len(results) else 1
if __name__ == '__main__':
    sys.exit(main())
