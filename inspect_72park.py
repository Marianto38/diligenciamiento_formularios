import fitz
import os

BASE = r"C:\Users\DELL\OneDrive\Documents\proyectos\crosby-pdf\72 PARK\LICENCIA BTR"

files = {
    "10": "10- BTR-Application 72 PARK 1406.pdf",
    "11": "11- RESORT-TAX-REGISTRATION-FORM- 72 PARK 1406 - BAMD LLC.pdf",
    "11_2": "11.2- RESORT-TAX-REGISTRATION-FORM- 72 PARK 1406 - BAMD LLC.pdf",
    "12": "12- TERM RENTAL ACKNOWLEDGMENT & DISCLOSURE LETTER 72 PARK 1406 all.pdf",
    "13": "13- Short Term Rental Affidavit Form - 72 PARK 1406 - ALP (1).pdf",
    "14": "14- Short-Term Rental Platform Listing - 72 PARK 1406 all.pdf",
}

for key, filename in files.items():
    path = os.path.join(BASE, filename)
    doc = fitz.open(path)
    print(f"\n{'='*60}")
    print(f"FORM {key}: {filename}")
    print(f"Pages: {len(doc)}, Size p0: {doc[0].rect}")

    for pg_num, page in enumerate(doc):
        print(f"\n  --- Page {pg_num+1} ---")
        # All text blocks with coordinates
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b["type"] == 0:
                for line in b["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            r = span["bbox"]
                            safe = text.encode('ascii', 'replace').decode('ascii')
                            print(f"    [{r[0]:.0f},{r[1]:.0f},{r[2]:.0f},{r[3]:.0f}] '{safe}'")

        # Annotations
        annots = list(page.annots())
        if annots:
            print(f"  Annotations ({len(annots)}):")
            for a in annots:
                            safe_c = a.info.get('content','')[:80].encode('ascii','replace').decode('ascii')
            print(f"    type={a.type} rect={a.rect} content='{safe_c}'")

    doc.close()
