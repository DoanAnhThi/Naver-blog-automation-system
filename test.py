from blog_writer import generate_blog_content

def main(keyword):
    reply = generate_blog_content(keyword)
    
    # In ra từng phần
    print("\n--- Tiêu đề ---")
    print(reply["title"])

    print("\n--- Mở bài ---")
    print(reply["intro"])

    print("\n--- Thân bài ---")
    print(reply["body"])

    print("\n--- Kết luận ---")
    print(reply["conclusion"])

    print("\n--- Tags ---")
    print(reply["tags"])

if __name__ == '__main__':
    keyword = input('Nhập từ khóa cho bài viết: ')
    main(keyword)
