"""
topics.py — Danh sách 7 chủ đề toán lớp 4 và kiến thức cần bao phủ.
"""

TOPICS: list[dict] = [
    {
        "id": "T1",
        "name": "Số tự nhiên",
        "description": "Đọc/viết số đến 1 000 000, so sánh, làm tròn số",
        "knowledge": [
            "Đọc và viết số tự nhiên đến 1 000 000",
            "Xác định giá trị theo vị trí hàng của chữ số",
            "So sánh và sắp xếp các số tự nhiên",
            "Làm tròn số đến hàng chục, hàng trăm, hàng nghìn",
        ],
    },
    {
        "id": "T2",
        "name": "Bốn phép tính số tự nhiên",
        "description": "Cộng/Trừ/Nhân/Chia; thứ tự phép tính; biểu thức",
        "knowledge": [
            "Cộng và trừ số có đến 6 chữ số",
            "Nhân số có nhiều chữ số với số có 1–2 chữ số",
            "Chia cho số có 1–2 chữ số (chia hết và chia có dư)",
            "Thứ tự thực hiện các phép tính trong biểu thức có ngoặc",
            "Tính chất giao hoán, kết hợp của phép cộng và phép nhân",
        ],
    },
    {
        "id": "T3",
        "name": "Phân số — Khái niệm & tính chất",
        "description": "Rút gọn, quy đồng, so sánh phân số",
        "knowledge": [
            "Khái niệm phân số: tử số và mẫu số",
            "Phân số bằng nhau",
            "Rút gọn phân số về dạng tối giản",
            "Quy đồng mẫu số hai phân số",
            "So sánh phân số cùng mẫu và khác mẫu",
        ],
    },
    {
        "id": "T4",
        "name": "Bốn phép tính phân số",
        "description": "Cộng/Trừ/Nhân/Chia phân số; hỗn số",
        "knowledge": [
            "Cộng và trừ phân số cùng mẫu số",
            "Cộng và trừ phân số khác mẫu số",
            "Nhân hai phân số",
            "Chia hai phân số (lấy nghịch đảo)",
            "Hỗn số: chuyển đổi giữa hỗn số và phân số",
        ],
    },
    {
        "id": "T5",
        "name": "Hình học",
        "description": "Góc, hình bình hành, hình thoi, hình thang — chu vi & diện tích",
        "knowledge": [
            "Nhận biết góc nhọn, góc vuông, góc tù, góc bẹt",
            "Hai đường thẳng vuông góc và song song",
            "Hình bình hành: chu vi và diện tích (đáy × chiều cao)",
            "Hình thoi: chu vi và diện tích (tích hai đường chéo ÷ 2)",
            "Hình thang: diện tích ((đáy lớn + đáy nhỏ) × chiều cao ÷ 2)",
        ],
    },
    {
        "id": "T6",
        "name": "Đo lường",
        "description": "Quy đổi đơn vị độ dài, diện tích, khối lượng, thời gian",
        "knowledge": [
            "Quy đổi đơn vị đo độ dài: km, m, dm, cm, mm",
            "Đơn vị đo diện tích: km², ha, m², dm², cm²",
            "Đơn vị đo khối lượng: tấn, tạ, yến, kg, g",
            "Đơn vị đo thời gian: thế kỷ, năm, tháng, tuần, ngày, giờ, phút, giây",
        ],
    },
    {
        "id": "T7",
        "name": "Toán có lời văn",
        "description": "Tổng–Hiệu, Tổng–Tỉ, trung bình cộng, bài toán thực tế",
        "knowledge": [
            "Tìm hai số khi biết tổng và hiệu của hai số đó",
            "Tìm hai số khi biết tổng và tỉ số của hai số đó",
            "Tính trung bình cộng của nhiều số",
            "Bài toán thực tế kết hợp nhiều phép tính",
        ],
    },
]


def get_topic_by_id(topic_id: str) -> dict | None:
    """Tìm chủ đề theo ID (T1..T7)."""
    return next((t for t in TOPICS if t["id"] == topic_id), None)
