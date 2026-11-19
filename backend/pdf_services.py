from fastapi import FastAPI, UploadFile, File
import pymupdf
import os

def pdf_processing(file_path):
    doc=pymupdf.open(file_path)
    metadata=doc.metadata
    total_pages=len(doc)
    pages=[]
    for page_num,page in enumerate(doc):
        text=page.get_text()
        pages.append({
            "page_number":page_num+1,
            "text":text,
            "width":page.rect.width,
            "height":page.rect.height
        })
    result={
        "metadata":metadata,
        "total_pages":total_pages,
        "pages":pages
    }
    doc.close()
    return result

def extract_imgs(file_path,output_dir="extracted_images"):
    os.makedirs(output_dir,exist_ok=True)
    doc=pymupdf.open(file_path)
    extract_imgs=[]
    for page_num,page in enumerate(doc):
        images=page.get_images(full=True)
        for img_index,img_info in enumerate(images):
            xref=img_info[0]
            image_data=doc.extract_image(xref)
            image_bytes=image_data["image"]
            extension=image_data["ext"]
            image_name=(
                f"page_{page_num+1}_"
                f"image_{img_index+1}.{extension}"
            )
            img_path=os.path.json(
                output_dir,
                image_name
            )
            with open(img_path,"wb") as image_file:
                image_file.write(image_bytes)
            extract_imgs.append({
                "page_number": page_num + 1,
                "image_path": img_path,
                "extension": extension,
                "width": image_data["width"],
                "height": image_data["height"]
            })
        doc.close()
        return extract_imgs


def extract_txt_coords(file_path):
    doc=pymupdf.open(file_path)
    extracted_data=[]
    for page_num,page in enumerate(doc):
        page_data=page.get_text("dict")
        for block in page_data["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    extracted_data.append({
                        "page_number":page_num+1,
                        "text":span["text"],
                        "bbox":span["bbox"],
                        "font":span["font"],
                        "size":span["size"]
                    })
    doc.close()
    return extracted_data

def render_pdf_pages(file_path,output_dir="rendered_pages"):
    os.makedirs(output_dir,exist_ok=True)
    doc=pymupdf.open(file_path)
    for page_num,page in enumerate(doc):
        pix=page.get_pixmap(
            matrix=pymupdf.Matrix(2,2),
            alpha=False
        )
        output_path=os.path.join(
            output_dir,
            f"page_{page_num+1}.png"
        )
        pix.save(output_path)
    doc.close()