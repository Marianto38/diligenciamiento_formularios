import fitz
import io
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "72 PARK", "LICENCIA BTR")

# ─── helpers ────────────────────────────────────────────────────────────────

def _redact_insert(page, rects_texts, fontsize=10):
    """Redact a list of (rect, text) pairs then insert text at each position."""
    for rect, text, insert_pt in rects_texts:
        page.add_redact_annot(fitz.Rect(*rect), fill=(1, 1, 1))
    page.apply_redactions()
    for rect, text, insert_pt in rects_texts:
        if text:
            page.insert_text(fitz.Point(*insert_pt), text,
                             fontname="helv", fontsize=fontsize, color=(0, 0, 0))


# ─── Form 10 — BTR Application ──────────────────────────────────────────────

def llenar_form10(datos, base_dir=BASE_DIR):
    llc    = datos["llc_nombre"]
    unidad = datos["unidad"]
    ein    = datos["ein"]
    fecha  = datos.get("fecha_aplicacion", "").strip()

    path = os.path.join(base_dir, "10- BTR-Application 72 PARK 1406.pdf")
    doc  = fitz.open(path)

    # ── Page 1 ──────────────────────────────────────────────────────────────
    p1 = doc[0]
    cert_use = datos.get('cert_use', '').strip()

    fields_p1 = [
        # (redact_rect,              text,                                         insert_point)
        ([390, 125, 485, 137],  fecha,                                        (391, 135)),   # Application Date
        ([33,  346, 300, 361],  llc,                                          (34,  359)),   # Business Name
        ([33,  378, 345, 394],  f"580 72 ST, MIAMI BEACH, FL 33141 unit {unidad}", (34, 392)), # Business Location
        ([33,  429, 300, 443],  llc,                                          (34,  441)),   # Owner/Principal
        ([33,  462, 210, 476],  ein,                                          (34,  474)),   # Federal ID
    ]
    if cert_use:
        fields_p1.append(([132, 125, 243, 137], cert_use, (133, 135)))        # Certificate of Use

    _redact_insert(p1, fields_p1, fontsize=10)

    # ── Page 2 ──────────────────────────────────────────────────────────────
    p2 = doc[1]

    # Remove existing date annotation
    for annot in list(p2.annots()):
        p2.delete_annot(annot)

    _redact_insert(p2, [
        ([33, 581, 260, 595], llc,   (34,  591)),   # Print Name
        ([487, 578, 528, 591], fecha, (488, 588)),   # Date
    ], fontsize=10)

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()


# ─── Form 11 / 11.2 — Resort Tax Registration ───────────────────────────────

_BLANK_FORM11 = "11- RESORT-TAX-REGISTRATION-FORM- EN BLANCO.pdf"

def _set_widget(page, field_name, value):
    for w in page.widgets():
        if w.field_name == field_name:
            w.field_value = str(value) if value else ''
            w.update()
            return


def _llenar_resort_tax(datos, members_slice, all_members, base_dir):
    llc       = datos['llc_nombre']
    ein       = datos['ein']
    fl_tax    = datos['fl_sales_tax']
    fecha_ini = datos.get('fecha_inicio', '').strip()

    primary_phone = all_members[0]['telefono'] if all_members else ''

    # Pad slice to 3 positions
    ms = [members_slice[i] if i < len(members_slice) else None for i in range(3)]

    path = os.path.join(base_dir, _BLANK_FORM11)
    doc  = fitz.open(path)
    page = doc[0]

    # Section 1 — Business Start Date
    _set_widget(page, '1  BUSINESS START DATE', fecha_ini)

    # Section 5 — Business Information
    _set_widget(page, 'NAME',         llc)
    _set_widget(page, 'ADDRESS',      '580 72nd Street, Miami Beach')
    _set_widget(page, 'CITY STATEZIP', 'Florida 33141, United States')
    _set_widget(page, 'PHONE NUMBER', primary_phone)
    _set_widget(page, 'FL SALES TAX', fl_tax)
    _set_widget(page, 'FED ID',       ein)

    # Section 6 — Operator slot (left)
    m0 = ms[0]
    csz0 = f"{m0['ciudad']}, {m0['estado']} {m0['zip']}" if m0 else ''
    _set_widget(page, 'NAME_2',          m0['nombre']    if m0 else '')
    _set_widget(page, 'ADDRESS_2',       m0['direccion'] if m0 else '')
    _set_widget(page, 'CITY STATEZIP_2', csz0)
    _set_widget(page, 'PHONE NUMBER_2',  m0['telefono']  if m0 else '')
    _set_widget(page, 'EMAIL',           m0['email']     if m0 else '')
    _set_widget(page, 'DRIVERS LICENSE', m0['dl_numero'] if m0 else '')

    # Section 7 — Operator slot (right top)
    m1 = ms[1]
    csz1 = f"{m1['ciudad']}, {m1['estado']} {m1['zip']}" if m1 else ''
    _set_widget(page, 'NAME_3',          m1['nombre']    if m1 else '')
    _set_widget(page, 'ADDRESS_3',       m1['direccion'] if m1 else '')
    _set_widget(page, 'CITY STATEZIP_3', csz1)
    _set_widget(page, 'PHONE NUMBER_3',  m1['telefono']  if m1 else '')
    _set_widget(page, 'EMAIL_2',         m1['email']     if m1 else '')
    _set_widget(page, 'DRIVERS LICENSE_2', m1['dl_numero'] if m1 else '')

    # Section 8 — Operator slot (right bottom)
    m2 = ms[2]
    csz2 = f"{m2['ciudad']}, {m2['estado']} {m2['zip']}" if m2 else ''
    _set_widget(page, 'NAME_4',          m2['nombre']    if m2 else '')
    _set_widget(page, 'ADDRESS_4',       m2['direccion'] if m2 else '')
    _set_widget(page, 'CITY STATEZIP_4', csz2)
    _set_widget(page, 'PHONE NUMBER_4',  m2['telefono']  if m2 else '')
    _set_widget(page, 'EMAIL_3',         m2['email']     if m2 else '')
    _set_widget(page, 'DRIVERS LICENSE_3', m2['dl_numero'] if m2 else '')

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()


def llenar_form11(datos, base_dir=BASE_DIR):
    all_members = datos.get('members', [])
    return _llenar_resort_tax(datos, all_members[0:3], all_members, base_dir)


def llenar_form11_2(datos, base_dir=BASE_DIR):
    all_members = datos.get('members', [])
    return _llenar_resort_tax(datos, all_members[3:6], all_members, base_dir)


# ─── Form 12 — Short-Term Rental Acknowledgment & Disclosure Letter ─────────

def llenar_form12(datos, base_dir=BASE_DIR):
    llc       = datos['llc_nombre']
    unidad    = datos['unidad']
    members   = datos.get('members', [])
    rep_names = ' - '.join(m['nombre'] for m in members)

    path = os.path.join(base_dir,
        "12- TERM RENTAL ACKNOWLEDGMENT & DISCLOSURE LETTER 72 PARK 1406 all.pdf")
    doc  = fitz.open(path)
    page = doc[0]

    # Redact all variable areas at once
    page.add_redact_annot(fitz.Rect(165, 130, 400, 144), fill=(1, 1, 1))  # Property Owner value
    page.add_redact_annot(fitz.Rect(216, 143, 538, 158), fill=(1, 1, 1))  # Auth Rep value (line 1, after label)
    page.add_redact_annot(fitz.Rect(72,  157, 538, 174), fill=(1, 1, 1))  # Auth Rep continuation (line 2 from x=72)
    page.add_redact_annot(fitz.Rect(172, 173, 536, 187), fill=(1, 1, 1))  # Property Address value
    page.add_redact_annot(fitz.Rect(72,  259, 536, 319), fill=(1, 1, 1))  # Body paragraph names
    page.add_redact_annot(fitz.Rect(72,  477, 536, 508), fill=(1, 1, 1))  # Signature names
    page.apply_redactions()

    fs = 10

    page.insert_text((166, 142), llc, fontname='helv', fontsize=fs, color=(0, 0, 0))

    page.insert_textbox(fitz.Rect(216, 144, 536, 172), rep_names,
                        fontname='helv', fontsize=fs, color=(0, 0, 0), align=0)

    page.insert_text((173, 184), f"580 72ND STREET - UNIT {unidad}",
                     fontname='helv', fontsize=fs, color=(0, 0, 0))

    body = (f"{rep_names} As the authorized representative of {llc}, I acknowledge "
            f"that the use of the above-mentioned residential property as a short-term "
            f"rental may result in the loss of the homestead exemption under Florida law.")
    page.insert_textbox(fitz.Rect(72, 260, 536, 318), body,
                        fontname='helv', fontsize=fs, color=(0, 0, 0), align=0)

    page.insert_textbox(fitz.Rect(72, 478, 536, 507), rep_names,
                        fontname='helv', fontsize=fs, color=(0, 0, 0), align=0)

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()


# ─── Form 13 — Short Term Rental Affidavit ──────────────────────────────────

def llenar_form13(datos, base_dir=BASE_DIR):
    unidad  = datos['unidad']
    fecha   = datos.get('fecha_aplicacion', '').strip()
    members = datos.get('members', [])
    owner   = members[0]['nombre'] if members else ''

    path = os.path.join(base_dir,
        "13- Short Term Rental Affidavit Form - 72 PARK 1406 - ALP (1).pdf")
    doc  = fitz.open(path)

    # ── Page 1 ──────────────────────────────────────────────────────────────
    p1 = doc[0]

    # Replace property address annotation
    for annot in list(p1.annots()):
        if annot.type[0] == 2:
            p1.delete_annot(annot)

    p1.add_freetext_annot(
        fitz.Rect(134, 133, 438, 150),
        f"580 72 ST, UNIT {unidad} MIAMI BEACH, FL 33141",
        fontname='Helv', fontsize=10,
        fill_color=(1, 1, 1), text_color=(0, 0, 0),
    )

    # Date (optional)
    if fecha:
        p1.add_redact_annot(fitz.Rect(73, 113, 473, 132), fill=(1, 1, 1))
        p1.apply_redactions()
        p1.insert_text((74, 129), fecha, fontname='helv', fontsize=11, color=(0, 0, 0))

    # ── Page 2 ──────────────────────────────────────────────────────────────
    p2 = doc[1]

    # Replace owner annotation (keep empty notary annotations)
    for annot in list(p2.annots()):
        if annot.type[0] == 2 and annot.info.get('content', '').strip():
            p2.delete_annot(annot)

    if owner:
        p2.add_freetext_annot(
            fitz.Rect(93, 274, 441, 291),
            owner,
            fontname='Helv', fontsize=10,
            fill_color=(1, 1, 1), text_color=(0, 0, 0),
        )

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()


# ─── Form 14 — Short-Term Rental Platform Listing ───────────────────────────

def llenar_form14(datos, base_dir=BASE_DIR):
    llc       = datos['llc_nombre']
    unidad    = datos['unidad']
    members   = datos.get('members', [])
    rep_names = ' - '.join(m['nombre'] for m in members)

    path = os.path.join(base_dir,
        "14- Short-Term Rental Platform Listing - 72 PARK 1406 all.pdf")
    doc  = fitz.open(path)
    page = doc[0]

    # Remove existing empty annotation
    for annot in list(page.annots()):
        page.delete_annot(annot)

    page.add_redact_annot(fitz.Rect(162,  98, 400, 112), fill=(1, 1, 1))  # Property Owner value
    page.add_redact_annot(fitz.Rect(216, 111, 542, 126), fill=(1, 1, 1))  # Auth Rep value (line 1, after label)
    page.add_redact_annot(fitz.Rect(72,  125, 542, 141), fill=(1, 1, 1))  # Auth Rep continuation (line 2 from x=72)
    page.add_redact_annot(fitz.Rect(172, 141, 536, 156), fill=(1, 1, 1))  # Property Address value
    page.add_redact_annot(fitz.Rect(72,  716, 536, 747), fill=(1, 1, 1))  # Signature names
    page.apply_redactions()

    fs = 10

    page.insert_text((163, 110), llc, fontname='helv', fontsize=fs, color=(0, 0, 0))

    page.insert_textbox(fitz.Rect(216, 112, 536, 140), rep_names,
                        fontname='helv', fontsize=fs, color=(0, 0, 0), align=0)

    page.insert_text((173, 153), f"580 72ND STREET - UNIT {unidad}",
                     fontname='helv', fontsize=fs, color=(0, 0, 0))

    page.insert_textbox(fitz.Rect(72, 717, 536, 746), rep_names,
                        fontname='helv', fontsize=fs, color=(0, 0, 0), align=0)

    out = io.BytesIO()
    doc.save(out)
    doc.close()
    return out.getvalue()
