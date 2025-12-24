import pymupdf
import os

"""
PDF 파일을 텍스트 파일로 변환하는 예제 코드입니다.
pymupdf 라이브러리를 사용하여 PDF 파일의 모든 페이지에서 텍스트를 추출하고,
추출된 텍스트를 하나의 텍스트 파일로 저장합니다.
"""
def pymupdf1():
    path = "./CH/chapter4/data/"
    pdf_file_name = "KCI_FI003103066.pdf"
    pdf_file_path = os.path.join(path, pdf_file_name)
    doc = pymupdf.open(pdf_file_path)
    text = ""

    for page in doc: # 문서 페이지 순회
        text += page.get_text() # 페이지의 텍스트 추출 및 누적

    output_txt_path = os.path.join(path, os.path.splitext(pdf_file_name)[0] + ".txt")

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(text)

"""
PDF 파일을 텍스트 파일로 변환하는 예제 코드입니다.
(헤더, 푸터 제외한 본문 텍스트만 추출)
"""
def pymupdf2():
    path = "./CH/chapter4/data/"
    pdf_file_name = "KCI_FI003103066.pdf"
    pdf_file_path = os.path.join(path, pdf_file_name)
    doc = pymupdf.open(pdf_file_path)

    header_footer_height = 80  # 헤더 및 푸터 높이 설정
    text = ""

    for page in doc: # 문서 페이지 순회
        page_rect = page.rect # 페이지의 크기 가져오기

        # 헤더와 푸터를 제외한 본문 텍스트 추출
        body = page.get_text(clip=(0, header_footer_height, page_rect.width, page_rect.height - header_footer_height))
        text += body

    output_txt_path = os.path.join(path, os.path.splitext(pdf_file_name)[0] + "s.txt")

    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    pymupdf1()
    pymupdf2()