"""
vietnamese_topics.py — Danh sách 7 chủ đề Tiếng Việt lớp 4 và kỹ năng cần bao phủ.
"""

VIET_TOPICS: list[dict] = [
    {
        "id": "V1",
        "name": "Tập đọc — Đọc hiểu",
        "description": "Tìm ý chính, nhân vật, thái độ tác giả, chi tiết quan trọng",
        "skills": [
            "Xác định ý chính của đoạn văn / bài văn",
            "Nhận biết và phân tích nhân vật (tính cách, hành động, lời nói)",
            "Hiểu thái độ, cảm xúc của tác giả qua văn bản",
            "Tìm chi tiết quan trọng để trả lời câu hỏi đọc hiểu",
            "Rút ra bài học hoặc ý nghĩa của câu chuyện",
        ],
    },
    {
        "id": "V2",
        "name": "Từ loại",
        "description": "Danh từ/Động từ/Tính từ/Đại từ — nhận biết, phân loại, đặt câu",
        "skills": [
            "Nhận biết danh từ chung và danh từ riêng; viết hoa danh từ riêng",
            "Nhận biết động từ chỉ hoạt động và trạng thái",
            "Nhận biết tính từ chỉ màu sắc, hình dáng, kích thước, tính chất",
            "Phân biệt đại từ xưng hô (tôi, em, chúng tôi, họ...)",
            "Đặt câu sử dụng đúng từ loại theo yêu cầu",
        ],
    },
    {
        "id": "V3",
        "name": "Cấu tạo từ",
        "description": "Từ đơn, từ ghép (tổng hợp/phân loại), từ láy (âm/vần/tiếng)",
        "skills": [
            "Phân biệt từ đơn (1 tiếng có nghĩa) và từ phức (2+ tiếng)",
            "Phân biệt từ ghép tổng hợp và từ ghép phân loại",
            "Nhận biết từ láy âm, từ láy vần, từ láy tiếng",
            "Giải nghĩa từ ghép và từ láy thông dụng",
            "Tìm từ cùng cấu tạo theo mẫu cho sẵn",
        ],
    },
    {
        "id": "V4",
        "name": "Cấu tạo câu",
        "description": "Chủ ngữ–Vị ngữ–Trạng ngữ; câu kể/hỏi/cảm/khiến; dấu câu",
        "skills": [
            "Xác định chủ ngữ (Ai? Cái gì? Con gì?) trong câu",
            "Xác định vị ngữ (làm gì? thế nào? là gì?) trong câu",
            "Thêm trạng ngữ chỉ thời gian, nơi chốn, nguyên nhân vào câu",
            "Phân biệt câu kể, câu hỏi, câu cảm, câu khiến và dấu câu tương ứng",
            "Đặt câu theo mẫu và sửa câu sai thành phần",
        ],
    },
    {
        "id": "V5",
        "name": "Chính tả",
        "description": "Phân biệt l/n, r/d/gi, s/x, ch/tr; viết hoa danh từ riêng",
        "skills": [
            "Phân biệt cách viết l/n ở đầu từ (l: lá, lúa; n: nước, núi)",
            "Phân biệt r/d/gi (r: rừng, rau; d: dừa, dâu; gi: giày, giỏi)",
            "Phân biệt s/x (s: sông, sao; x: xuân, xanh)",
            "Phân biệt ch/tr (ch: chim, chợ; tr: trăng, trường)",
            "Quy tắc viết hoa tên người, tên địa lý Việt Nam và nước ngoài",
        ],
    },
    {
        "id": "V6",
        "name": "Văn kể chuyện",
        "description": "Cấu trúc 3 phần, xây dựng nhân vật, diễn biến, kết thúc",
        "skills": [
            "Viết mở bài trực tiếp và mở bài gián tiếp",
            "Xây dựng diễn biến câu chuyện có đầu—giữa—cuối rõ ràng",
            "Miêu tả nhân vật qua ngoại hình, lời nói, hành động",
            "Viết kết bài mở rộng và kết bài không mở rộng",
            "Dùng lời dẫn chuyện và lời đối thoại phù hợp",
        ],
    },
    {
        "id": "V7",
        "name": "Văn miêu tả",
        "description": "Tả đồ vật/cây cối/con vật; trình tự quan sát; dùng so sánh, nhân hóa",
        "skills": [
            "Tả đồ vật theo trình tự: tổng thể → từng bộ phận → công dụng",
            "Tả cây cối theo mùa hoặc từng bộ phận (rễ, thân, cành, lá, hoa, quả)",
            "Tả con vật qua ngoại hình và hoạt động đặc trưng",
            "Sử dụng biện pháp so sánh để câu văn sinh động, cụ thể",
            "Sử dụng biện pháp nhân hóa để đồ vật/cây/con vật trở nên gần gũi",
        ],
    },
]


def get_viet_topic_by_id(topic_id: str) -> dict | None:
    """Tìm chủ đề Tiếng Việt theo ID (V1–V7)."""
    for t in VIET_TOPICS:
        if t["id"] == topic_id:
            return t
    return None
