"""
Módulo para llenar el PDF de District 225 Miami — Owners Orientation Package.
Sigue el mismo patrón que crosby_fill.py / nomad_fill.py: estampa texto sobre
el PDF escaneado original en coordenadas fijas (bounding boxes), derivadas por
análisis de píxeles de las líneas en blanco del formulario original.
"""

import io

MESES_EN = {
    '01': 'January',  '02': 'February', '03': 'March',    '04': 'April',
    '05': 'May',      '06': 'June',     '07': 'July',     '08': 'August',
    '09': 'September','10': 'October',  '11': 'November', '12': 'December',
}


def derivar_fechas(fecha_corta: str) -> dict:
    partes = fecha_corta.split('/')
    mes_num, dia, anio = partes[0], partes[1], partes[2]
    mes_nombre = MESES_EN.get(mes_num, mes_num)
    anio_corto = anio[2:]
    return {
        'fecha_corta':    fecha_corta,
        'fecha_dia':      dia,
        'fecha_mes':      mes_nombre,
        'fecha_mes_anio': f'{mes_nombre} {anio}',
        'anio_corto':     anio_corto,
        'fecha_corta_yy': f'{mes_num}/{dia}/{anio_corto}',
    }


def construir_campos(D):
    fs, sm = 9, 8

    def c(page, desc, ebb, text, font_size=fs):
        return {
            "page_number": page,
            "description": desc,
            "entry_bounding_box": ebb,
            "entry_text": {"text": text, "font_size": font_size},
        }

    fields = []

    # ── PÁGINA 1 — Acknowledgement of Receipt ──────────────────────────────
    fields.append(c(1, "Owner name", [44, 93, 176, 105],  D["nombre"]))
    fields.append(c(1, "Unit #",     [252, 93, 302, 105], D["unidad"], sm))

    iniciales = ''.join(p[0].upper() for p in D["nombre"].split() if p)
    row_y0 = 168.5
    row_step = 14.15
    for i in range(15):
        y1 = row_y0 + i * row_step
        y0 = y1 - 10
        fields.append(c(1, f"F{i+1} rcv",  [358, y0, 390, y1], iniciales,          sm))
        fields.append(c(1, f"F{i+1} date", [466, y0, 497, y1], D["fecha_corta_yy"], sm))

    fields.append(c(1, "Deed Name",     [162, 521, 480, 533], D["nombre"]))
    fields.append(c(1, "Recipient sig", [206, 547, 391, 559], D["nombre"]))
    fields.append(c(1, "Recipient date",[457, 547, 538, 559], D["fecha_corta_yy"], sm))

    # ── PÁGINA 2 — Confidential Owner Information Sheet ────────────────────
    # (El bloque del Propietario 1 no tiene fila de Nombre propia en el
    # original — empieza directo en la fila de teléfonos.)
    fields.append(c(2, "Owner1 Primary Phone", [55, 76, 180, 88],  D["telefono"]))
    fields.append(c(2, "Owner1 Email",         [442, 76, 566, 88], D["email1"], sm))
    fields.append(c(2, "Emergency Contact",    [145, 332, 330, 344], D["contacto_emerg"]))
    fields.append(c(2, "Emergency Tel",        [385, 332, 566, 344], D["tel_emerg"], sm))

    # ── PÁGINA 3 — Unit Access Authorization ────────────────────────────────
    fields.append(c(3, "Unit #",     [108, 95, 217, 107],  D["unidad"]))
    fields.append(c(3, "Owner name", [312, 95, 566, 107],  D["nombre"]))
    fields.append(c(3, "Signed day", [110, 594, 300, 606], D["fecha_corta_yy"], sm))
    fields.append(c(3, "Signature",  [90, 618, 300, 630],  D["nombre"]))

    # ── PÁGINA 4 — Parcel Receipt Authorization ─────────────────────────────
    fields.append(c(4, "Signed day",     [116, 414, 248, 426], D["fecha_corta_yy"], sm))
    fields.append(c(4, "Name Printed",   [140, 481, 251, 493], D["nombre"]))
    fields.append(c(4, "Signature",      [120, 508, 247, 520], D["nombre"]))
    fields.append(c(4, "Unit Number",    [135, 535, 230, 547], D["unidad"]))

    # ── PÁGINA 7 — Move In / Move Out and Deliveries Policy (2 columnas) ────
    fields.append(c(7, "Signed day",   [141, 600, 246, 612],  D["fecha_corta_yy"], sm))
    fields.append(c(7, "Name Printed", [420, 668, 566, 680],  D["nombre"]))
    fields.append(c(7, "Unit Number",  [420, 721, 566, 733],  D["unidad"]))

    # ── PÁGINA 8 — Key & Access Device Release Authorization ────────────────
    fields.append(c(8, "Unit #",         [100, 107, 280, 119], D["unidad"]))
    fields.append(c(8, "Date",           [385, 107, 566, 119], D["fecha_corta_yy"], sm))
    fields.append(c(8, "Unit Owner Name",[131, 147, 480, 159], D["nombre"]))
    fields.append(c(8, "Signed day",     [135, 432, 250, 444], D["fecha_corta_yy"], sm))
    fields.append(c(8, "Name Printed",   [100, 513, 246, 525], D["nombre"]))
    fields.append(c(8, "Signature",      [88, 540, 180, 552],  D["nombre"]))
    fields.append(c(8, "Unit Number",    [98, 567, 304, 579],  D["unidad"]))

    # ── PÁGINA 9 — Developer Customer Service Key Release ───────────────────
    fields.append(c(9, "Unit #",     [62, 130, 122, 142],  D["unidad"]))
    fields.append(c(9, "Unit Owner", [205, 130, 388, 142], D["nombre"]))
    fields.append(c(9, "Top sig",    [34, 376, 153, 388], D["nombre"], sm))
    fields.append(c(9, "Top date",   [361, 377, 464, 389],D["fecha_corta_yy"], sm))

    # ── PÁGINA 15 — Payment of Assessments ───────────────────────────────────
    fields.append(c(15, "Unit Owner Name", [128, 110, 405, 122], D["nombre"]))
    fields.append(c(15, "Date",            [65, 143, 198, 155],  D["fecha_corta_yy"], sm))
    fields.append(c(15, "Unit",            [230, 143, 405, 155], D["unidad"], sm))

    # ── PÁGINA 17 — Acknowledgement of Transient Rental Requirements ────────
    fields.append(c(17, "Name Printed", [102, 710, 246, 722], D["nombre"]))
    fields.append(c(17, "Unit",         [508, 710, 572, 722], D["unidad"], sm))

    return fields


def llenar_pdf(datos: dict, pdf_original_path: str) -> bytes:
    import fitz

    fechas = derivar_fechas(datos["fecha_corta"])
    D = {**datos, **fechas}

    doc = fitz.open(pdf_original_path)

    for campo in construir_campos(D):
        texto = campo["entry_text"]["text"]
        if not texto:
            continue

        pg = campo["page_number"]
        if pg > len(doc):
            continue
        page = doc[pg - 1]
        ebb = campo["entry_bounding_box"]
        font_size = campo["entry_text"]["font_size"]

        x0, y_bot = ebb[0] + 1, ebb[3] - 1

        page.insert_text(
            point=(x0, y_bot),
            text=texto,
            fontsize=font_size,
            color=(0, 0, 0),
            fontname="helv",
        )

    buf = io.BytesIO()
    doc.save(buf, deflate=True, garbage=4, clean=True)
    buf.seek(0)
    return buf.read()
