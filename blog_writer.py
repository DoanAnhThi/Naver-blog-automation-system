import os
from dotenv import load_dotenv
import openai

# Load API key từ file .env
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = openai.OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o"

SEO_PROMPT = '''
Bạn là một chuyên gia viết blog chuẩn SEO. Hãy viết một bài blog tối ưu SEO với cấu trúc sau, dựa trên từ khóa: "{keyword}".

Yêu cầu:
- Tất cả viết bằng tiếng Hàn
- Tiêu đề hấp dẫn, chứa từ khóa.
- Mở bài (ít nhất 300 ký tự, chứa từ khóa tự nhiên).
- Thân bài (ít nhất 300 ký tự, trình bày chi tiết, có thể chia ý rõ ràng, chứa từ khóa tự nhiên).
- Kết luận (ít nhất 300 ký tự, tổng kết và kêu gọi hành động, chứa từ khóa tự nhiên).
- Thẻ tag: 5 thẻ liên quan, phân tách bằng dấu phẩy.

**Chỉ trả về JSON thuần túy, không có giải thích, không có markdown, không có ký tự thừa.**
Định dạng:
{{
  "title": "...",
  "intro": "...",
  "body": "...",
  "conclusion": "...",
  "tags": "..."
}}
'''


def generate_blog_content(keyword: str) -> dict:
    prompt = SEO_PROMPT.format(keyword=keyword)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Bạn là một chuyên gia viết blog chuẩn SEO."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    # Lấy nội dung trả về
    content = response.choices[0].message.content
    # Nếu là JSON, chuyển thành dict
    import json
    try:
        result = json.loads(content)
    except Exception:
        # Nếu không phải JSON chuẩn, trả về raw
        result = {"raw": content}
    return result
