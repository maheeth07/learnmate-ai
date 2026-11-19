
from pathlib import Path
from pdf_services import pdf_processing

# Get backend directory
BASE_DIR = Path(__file__).resolve().parent

# PDF file location
file_path = BASE_DIR / "pdfs" / "RES_UNIT_5_intoduction.pdf"

# Process PDF
result = pdf_processing(str(file_path))

# Display metadata
print("\n========== PDF METADATA ==========")
print(result["metadata"])

# Display total pages
print("\n========== TOTAL PAGES ==========")
print(result["total_pages"])

# Display first page text
print("\n========== FIRST PAGE CONTENT ==========")


print("\n========== ALL PDF PAGES ==========")

for page in result["pages"]:

    print(f"\n{'=' * 20}")
    print(f"PAGE {page['page_number']}")
    print(f"{'=' * 20}")

    print(page["text"])
