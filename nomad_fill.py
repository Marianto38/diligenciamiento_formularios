"""
Módulo para llenar el PDF de Nomad Residences Wynwood Orientation Package.
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

    def c(page, desc, lbb, ebb, text, font_size=fs):
        return {
            "page_number": page,
            "description": desc,
            "label_bounding_box": lbb,
            "entry_bounding_box": ebb,
            "entry_text": {"text": text, "font_size": font_size},
        }

    fields = []

    # ── PÁGINA 1 — Acknowledgment ──────────────────────────────────────────────
    fields.append(c(1, "Owner name",    [36, 174, 43, 188],  [46, 174, 195, 188],  D["nombre"]))
    fields.append(c(1, "Unit #",        [243,174, 267,188],  [272,174, 348, 188],  D["unidad"]))
    fields.append(c(1, "Deed Name",     [36, 499, 157,513],  [158,499, 430, 513],  D["nombre"]))

    iniciales = ''.join(p[0].upper() for p in D["nombre"].split() if p)
    form_rows_y = [247, 260, 272, 284, 296, 309, 321, 333, 346, 358, 371, 383, 395]
    for i, cy in enumerate(form_rows_y):
        y0, y1 = cy - 5, cy + 5
        fields.append(c(1, f"F{i+1} rcv",  [280,y0,314,y1], [315,y0,370,y1], iniciales,          sm))
        fields.append(c(1, f"F{i+1} date", [370,y0,431,y1], [432,y0,540,y1], D["fecha_corta_yy"], sm))

    # ── PÁGINA 2 — Unit Owner Information ─────────────────────────────────────
    fields.append(c(2, "Unit Number",   [36, 157, 103,171],  [106,157, 183, 171],  D["unidad"]))
    fields.append(c(2, "Owner Name",    [184,157, 254,171],  [257,157, 520, 171],  D["nombre"]))
    fields.append(c(2, "Cell Phone",    [36, 184, 100,197],  [100,184, 215, 197],  D["telefono"]))
    fields.append(c(2, "Email",         [36, 210, 110,224],  [111,210, 374, 224],  D["email1"]))
    fields.append(c(2, "Emerg Contact", [36, 399, 133,413],  [133,399, 320, 413],  D["contacto_emerg"]))
    fields.append(c(2, "Emerg Tel",     [324,399, 378,413],  [378,399, 540, 413],  D["tel_emerg"]))

    # ── PÁGINA 3 — Unit Access Authorization ──────────────────────────────────
    fields.append(c(3, "Unit #",        [36, 149, 73, 164],  [75, 149, 165, 164],  D["unidad"]))
    fields.append(c(3, "Owner name",    [216,149, 338,164],  [339,149, 567, 164],  D["nombre"]))
    fields.append(c(3, "Name Printed",  [288,686, 386,700],  [396,686, 583, 700],  D["nombre"]))
    fields.append(c(3, "Unit Number",   [288,726, 393,741],  [394,726, 556, 741],  D["unidad"]))

    # ── PÁGINA 4 — Parcel Receipt Authorization ───────────────────────────────
    fields.append(c(4, "Day",           [467,140, 487,155],  [487,140, 518, 155],  D["fecha_dia"],      sm))
    fields.append(c(4, "Month",         [36, 154, 49, 169],  [50, 154, 143, 169],  D["fecha_mes"],      sm))
    fields.append(c(4, "Owner name",    [36, 169, 36, 183],  [36, 169, 234, 183],  D["nombre"]))
    fields.append(c(4, "Unit #",        [423,169, 456,183],  [457,169, 510, 183],  D["unidad"],         sm))
    fields.append(c(4, "Sign day",      [36, 544, 95, 559],  [96, 544, 126, 559],  D["fecha_dia"],      sm))
    fields.append(c(4, "Sign month",    [128,544, 164,559],  [165,544, 296, 559],  D["fecha_mes_anio"], sm))
    fields.append(c(4, "Name Printed",  [288,628, 386,643],  [397,628, 583, 643],  D["nombre"]))
    fields.append(c(4, "Unit Number",   [288,669, 393,683],  [394,669, 556, 683],  D["unidad"]))

    # ── PÁGINA 6 — Warranty and Appliance Manual Acknowledgement ──────────────
    fields.append(c(6, "Owner name",    [36, 200, 70, 215],  [71, 200, 271, 215],  D["nombre"]))
    fields.append(c(6, "Unit #",        [359,200, 367,215],  [367,200, 408, 215],  D["unidad"],         sm))
    fields.append(c(6, "Sign day",      [36, 301, 95, 316],  [96, 301, 126, 316],  D["fecha_dia"],      sm))
    fields.append(c(6, "Sign month",    [128,301, 164,316],  [165,301, 284, 316],  D["fecha_mes_anio"], sm))
    fields.append(c(6, "Name Printed",  [318,442, 396,457],  [397,442, 583, 457],  D["nombre"]))
    fields.append(c(6, "Unit Number",   [318,483, 393,498],  [394,483, 556, 498],  D["unidad"]))

    # ── PÁGINA 7 — Vehicle Registration Form ──────────────────────────────────
    fields.append(c(7, "Owner Name",    [36, 182, 108,197],  [109,182, 258, 197],  D["nombre"]))
    fields.append(c(7, "Unit #",        [288,182, 324,197],  [325,182, 397, 197],  D["unidad"]))

    # ── PÁGINA 8 — Pet Registration Form ──────────────────────────────────────
    fields.append(c(8, "Date",          [36, 145, 63, 160],  [64, 145, 151, 160],  D["fecha_corta_yy"], sm))
    fields.append(c(8, "Unit",          [144,145, 180,160],  [181,145, 286, 160],  D["unidad"],         sm))
    fields.append(c(8, "Owner Name",    [288,145, 375,160],  [377,145, 550, 160],  D["nombre"]))
    fields.append(c(8, "Sign day",      [36, 641, 95, 656],  [96, 641, 126, 656],  D["fecha_dia"],      sm))
    fields.append(c(8, "Sign month",    [128,641, 164,656],  [165,641, 314, 656],  D["fecha_mes_anio"], sm))
    fields.append(c(8, "Name Printed",  [318,695, 396,710],  [397,695, 583, 710],  D["nombre"]))
    fields.append(c(8, "Unit Number",   [318,736, 393,751],  [394,736, 556, 751],  D["unidad"]))

    # ── PÁGINA 10 — Key & Access Device Release Authorization ─────────────────
    fields.append(c(10,"Unit #",        [36, 152, 71, 167],  [72, 152, 144, 167],  D["unidad"]))
    fields.append(c(10,"Date",          [360,152, 391,167],  [391,152, 548, 167],  D["fecha_corta_yy"], sm))
    fields.append(c(10,"Owner Name",    [36, 196, 138,211],  [139,196, 367, 211],  D["nombre"]))
    fields.append(c(10,"Sign day",      [36, 412, 95, 427],  [96, 412, 126, 427],  D["fecha_dia"],      sm))
    fields.append(c(10,"Sign month",    [128,412, 164,427],  [165,412, 296, 427],  D["fecha_mes_anio"], sm))
    fields.append(c(10,"Name Printed",  [318,650, 396,665],  [397,650, 583, 665],  D["nombre"]))
    fields.append(c(10,"Unit Number",   [318,691, 393,706],  [394,691, 556, 706],  D["unidad"]))

    # ── PÁGINA 11 — Developer Customer Service Access Release ─────────────────
    fields.append(c(11,"Unit #",        [36, 166, 75, 179],  [76, 166, 180, 179],  D["unidad"]))
    fields.append(c(11,"Owner name",    [108,166, 192,179],  [193,166, 400, 179],  D["nombre"]))

    # ── PÁGINA 12 — Key Policy ────────────────────────────────────────────────
    fields.append(c(12,"Resident name", [36, 300, 46, 315],  [47, 300, 229, 315],  D["nombre"]))
    fields.append(c(12,"Unit #",        [290,300, 321,315],  [322,300, 375, 315],  D["unidad"]))
    fields.append(c(12,"Sign day",      [36, 372, 95, 387],  [96, 372, 126, 387],  D["fecha_dia"],      sm))
    fields.append(c(12,"Sign month",    [128,372, 164,387],  [165,372, 350, 387],  D["fecha_mes_anio"], sm))
    fields.append(c(12,"Name Printed",  [318,655, 396,670],  [397,655, 583, 670],  D["nombre"]))
    fields.append(c(12,"Unit Number",   [318,696, 393,711],  [394,696, 556, 711],  D["unidad"]))

    # ── PÁGINA 13 — Release, Identification and Hold Harmless ─────────────────
    fields.append(c(13,"Day header",    [444,144, 451,155],  [452,144, 476, 155],  D["fecha_dia"],      sm))
    fields.append(c(13,"Month header",  [36, 155, 42, 166],  [42, 155, 126, 166],  D["fecha_mes"],      sm))
    fields.append(c(13,"Unit #",        [420,155, 446,166],  [446,155, 505, 166],  D["unidad"],         sm))
    fields.append(c(13,"Sign day",      [36, 618, 217,631],  [218,618, 245, 631],  D["fecha_dia"],      sm))
    fields.append(c(13,"Sign month",    [248,618, 280,631],  [281,618, 391, 631],  D["fecha_mes_anio"], sm))
    fields.append(c(13,"Name Printed",  [318,684, 396,699],  [397,684, 583, 699],  D["nombre"]))
    fields.append(c(13,"Unit Number",   [318,725, 393,740],  [394,725, 556, 740],  D["unidad"]))

    # ── PÁGINA 14 — Protection of Association Property ────────────────────────
    fields.append(c(14,"Sign day",      [36, 436, 95, 451],  [96, 436, 126, 451],  D["fecha_dia"],      sm))
    fields.append(c(14,"Sign month",    [128,436, 164,451],  [165,436, 344, 451],  D["fecha_mes_anio"], sm))
    fields.append(c(14,"Name Printed",  [318,589, 396,603],  [397,589, 583, 603],  D["nombre"]))
    fields.append(c(14,"Unit Number",   [318,629, 393,644],  [394,629, 556, 644],  D["unidad"]))

    # ── PÁGINA 15 — Electric Transfer Acknowledgment ──────────────────────────
    fields.append(c(15,"Owner Name",    [36, 155, 135,169],  [136,155, 347, 169],  D["nombre"]))
    fields.append(c(15,"Unit",          [349,155, 375,169],  [376,155, 467, 169],  D["unidad"]))
    fields.append(c(15,"Conv Date",     [535,155, 564,169],  [564,155, 612, 169],  D["fecha_corta"],    sm))
    fields.append(c(15,"Day",           [210,198, 262,213],  [262,198, 297, 213],  D["fecha_dia"],      sm))
    fields.append(c(15,"Month",         [301,198, 337,213],  [337,198, 421, 213],  D["fecha_mes"],      sm))
    fields.append(c(15,"Year",          [431,198, 449,213],  [449,198, 472, 213],  D["anio_corto"],     sm))
    fields.append(c(15,"Unit inline",   [245,212, 271,227],  [323,212, 356, 227],  D["unidad"],         sm))

    # ── PÁGINA 17 — Acknowledgement of Rules and Regulations ──────────────────
    unit_addr = f"Unit {D['unidad']}, 2700 NW 2nd Ave, Miami, FL 33127"
    fields.append(c(17,"Unit Address",  [36, 170, 103,183],  [104,170, 390, 183],  unit_addr,           sm))
    fields.append(c(17,"Owner Name 1",  [36, 220, 176,234],  [177,220, 396, 234],  D["nombre"]))

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
