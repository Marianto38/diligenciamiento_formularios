"""
Módulo para llenar el PDF de Owners Orientation Package de The Crosby.
"""

import os
import io

MESES_EN = {
    '01': 'January',  '02': 'February', '03': 'March',    '04': 'April',
    '05': 'May',      '06': 'June',     '07': 'July',     '08': 'August',
    '09': 'September','10': 'October',  '11': 'November', '12': 'December',
}

def derivar_fechas(fecha_corta: str) -> dict:
    """
    Recibe fecha en formato MM/DD/YYYY y retorna todos los campos de fecha.
    """
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

    def campo(page, desc, lbb, ebb, text, font_size=fs):
        return {
            "page_number": page,
            "description": desc,
            "label_bounding_box": lbb,
            "entry_bounding_box": ebb,
            "entry_text": {"text": text, "font_size": font_size},
        }

    fields = []

    # ── PÁGINA 1 ─────────────────────────────────────────────────────────────
    fields.append(campo(1, "Owner name",  [36,163,42,174],  [44,163,178,174],  D["nombre"]))
    fields.append(campo(1, "Unit number", [219,163,246,174],[248,163,310,174], D["unidad"]))

    form_rows = [234.5,246.6,258.9,271.1,284.3,296.6,308.7,320.8,333.0,345.2,357.3,369.5,381.6]
    for i, y in enumerate(form_rows):
        t, b = y-4, y+5
        fields.append(campo(1, f"F{i+1} rcv",  [54,t,310,b], [315,t,362,b], "FG",                    sm))
        fields.append(campo(1, f"F{i+1} date", [365,t,432,b],[434,t,540,b], D["fecha_corta_yy"],      sm))

    for qty, rcvd, owner, yr, row in [("1","1","1",461.9,"Mob"),("3","3","3",473.3,"Mail"),("1","1","1",484.8,"Acc")]:
        t, b = yr-4, yr+5
        fields.append(campo(1, f"{row} Qty",  [108,t,355,b],[360,t,390,b], qty,   sm))
        fields.append(campo(1, f"{row} Rcvd", [392,t,430,b],[434,t,466,b], rcvd,  sm))
        fields.append(campo(1, f"{row} Own",  [468,t,502,b],[506,t,528,b], owner, sm))

    fields.append(campo(1, "Deed name", [36,514,138,526],[140,514,400,526], D["nombre"]))

    # ── PÁGINA 2 ─────────────────────────────────────────────────────────────
    fields.append(campo(2, "Unit number",  [36,148,91,159],  [92,148,167,159],  D["unidad"]))
    fields.append(campo(2, "Owner name",   [170,148,268,159],[270,148,538,159], D["nombre"]))
    fields.append(campo(2, "Cell phone",   [36,160,91,171],  [92,160,215,171],  D["telefono"]))
    fields.append(campo(2, "Email 1",      [36,185,98,196],  [99,185,340,196],  D["email1"]))
    fields.append(campo(2, "Corp No",      [216,237,251,248],[253,238,261,247], "X",          7))
    fields.append(campo(2, "Secondary",    [360,237,415,248],[417,238,424,247], "X",          7))
    fields.append(campo(2, "Emerg name",   [36,336,118,349], [119,336,318,349], D["contacto_emerg"]))
    fields.append(campo(2, "Emerg tel",    [324,336,369,349],[371,336,540,349], D["tel_emerg"]))
    if D.get("llave1"): fields.append(campo(2, "Llave 1", [36,596,45,609],  [47,596,318,609],  D["llave1"]))
    if D.get("llave2"): fields.append(campo(2, "Llave 2", [320,596,332,609],[334,596,540,609], D["llave2"]))
    if D.get("llave3"): fields.append(campo(2, "Llave 3", [36,621,45,634],  [47,621,318,634],  D["llave3"]))
    if D.get("llave4"): fields.append(campo(2, "Llave 4", [320,621,332,634],[334,621,540,634], D["llave4"]))
    fields.append(campo(2, "NO check",     [36,676,46,688],  [47,676,57,688],   "X",          7))

    # ── PÁGINA 3 ─────────────────────────────────────────────────────────────
    fields.append(campo(3, "Unit#",        [36,144,66,157],  [68,144,144,157],  D["unidad"]))
    fields.append(campo(3, "Owner",        [216,144,316,157],[318,144,525,157], D["nombre"]))
    fields.append(campo(3, "Name Printed", [288,643,351,656],[353,643,535,656], D["nombre"]))
    fields.append(campo(3, "Unit# sig",    [288,682,346,695],[349,682,540,695], D["unidad"]))

    # ── PÁGINA 4 ─────────────────────────────────────────────────────────────
    fields.append(campo(4, "Exec day",     [399,148,416,162],[416,148,443,162], D["fecha_dia"],  sm))
    fields.append(campo(4, "Exec month",   [461,148,470,162],[470,148,560,162], D["fecha_mes"],  sm))
    fields.append(campo(4, "Owner inline", [374,162,396,176],[396,162,577,176], D["nombre"]))
    fields.append(campo(4, "Unit inline",  [193,176,218,190],[218,176,268,190], D["unidad"],     sm))
    fields.append(campo(4, "Sign day",     [36,493,87,506],  [88,493,115,506],  D["fecha_dia"],  sm))
    fields.append(campo(4, "Sign month",   [117,493,145,506],[147,493,268,506], D["fecha_mes"],  sm))
    fields.append(campo(4, "Name Printed", [288,562,351,575],[353,562,535,575], D["nombre"]))
    fields.append(campo(4, "Unit# sig",    [288,595,346,608],[349,595,442,608], D["unidad"]))

    # ── PÁGINA 5 ─────────────────────────────────────────────────────────────
    fields.append(campo(5, "Unit# top",    [200,141,273,153],[273,141,320,153], D["unidad"]))

    # ── PÁGINA 6 ─────────────────────────────────────────────────────────────
    fields.append(campo(6, "IWe name",     [36,194,57,208],  [59,194,242,208],  D["nombre"]))
    fields.append(campo(6, "IWe unit",    [313,194,321,208],[321,194,357,208], D["unidad"]))
    fields.append(campo(6, "Sign day",     [36,291,90,304],  [92,291,112,304],  D["fecha_dia"],      sm))
    fields.append(campo(6, "Sign month",   [115,291,142,304],[144,291,280,304], D["fecha_mes_anio"], sm))
    fields.append(campo(6, "Name Printed", [288,401,351,414],[353,401,535,414], D["nombre"]))
    fields.append(campo(6, "Unit# sig",    [288,440,346,453],[349,440,496,453], D["unidad"]))

    # ── PÁGINA 7 ─────────────────────────────────────────────────────────────
    fields.append(campo(7, "Resident name",[36,168,111,181], [113,168,288,181], D["nombre"]))
    fields.append(campo(7, "Unit#",        [324,168,345,181],[358,168,415,181], D["unidad"]))

    # ── PÁGINA 8 ─────────────────────────────────────────────────────────────
    fields.append(campo(8, "Date",         [36,141,58,154],  [60,141,150,154],  D["fecha_corta_yy"], sm))
    fields.append(campo(8, "Unit#",        [152,141,172,154],[174,141,252,154], D["unidad"]))
    fields.append(campo(8, "Owner name",   [254,141,322,154],[324,141,483,154], D["nombre"]))
    fields.append(campo(8, "Name Printed", [299,641,362,654],[365,641,540,654], D["nombre"]))
    fields.append(campo(8, "Unit# sig",    [299,680,357,693],[360,680,507,693], D["unidad"]))

    # ── PÁGINA 9 ─────────────────────────────────────────────────────────────
    fields.append(campo(9, "Sign day",     [36,602,88,615],  [90,602,111,615],  D["fecha_dia"],      sm))
    fields.append(campo(9, "Sign month",   [114,602,142,615],[144,602,262,615], D["fecha_mes_anio"], sm))
    fields.append(campo(9, "Name Printed", [288,671,351,684],[353,671,541,684], D["nombre"]))
    fields.append(campo(9, "Unit# sig",    [288,710,346,723],[349,710,497,723], D["unidad"]))

    # ── PÁGINA 10 ────────────────────────────────────────────────────────────
    fields.append(campo(10,"Unit# top",    [36,148,62,161],  [64,148,128,161],  D["unidad"]))
    fields.append(campo(10,"Date top",     [324,148,350,161],[352,148,492,161], D["fecha_corta"]))
    fields.append(campo(10,"Owner name",   [36,189,118,202], [120,189,326,202], D["nombre"]))
    fields.append(campo(10,"Sign day",     [36,492,88,505],  [90,492,111,505],  D["fecha_dia"],      sm))
    fields.append(campo(10,"Sign month",   [114,492,142,505],[144,492,300,505], D["fecha_mes_anio"], sm))
    fields.append(campo(10,"Name Printed", [288,572,351,585],[353,572,541,585], D["nombre"]))
    fields.append(campo(10,"Unit# sig",    [288,611,346,624],[349,611,497,624], D["unidad"]))

    # ── PÁGINA 11 ────────────────────────────────────────────────────────────
    fields.append(campo(11,"Unit# top",    [36,134,66,147],  [68,134,125,147],  D["unidad"]))
    fields.append(campo(11,"Owner top",    [127,134,149,147],[240,134,540,147], D["nombre"]))
    fields.append(campo(11,"Date sig",     [288,403,322,414],[325,403,468,414], D["fecha_corta"]))

    # ── PÁGINA 12 ────────────────────────────────────────────────────────────
    fields.append(campo(12,"Resident name",[36,305,41,316],  [45,305,211,316],  D["nombre"]))
    fields.append(campo(12,"Unit# inline", [264,305,284,316],[286,305,338,316], D["unidad"]))
    fields.append(campo(12,"Sign day",     [36,374,86,385],  [88,374,114,385],  D["fecha_dia"],      sm))
    fields.append(campo(12,"Sign month",   [117,374,144,385],[146,374,316,385], D["fecha_mes_anio"], sm))
    fields.append(campo(12,"Name Printed", [288,473,351,486],[353,473,535,486], D["nombre"]))
    fields.append(campo(12,"Unit# sig",    [288,513,346,526],[349,513,496,526], D["unidad"]))

    # ── PÁGINA 13 ────────────────────────────────────────────────────────────
    fields.append(campo(13,"Day",          [363,141,384,154],[386,141,400,154], D["fecha_dia"],  sm))
    fields.append(campo(13,"Month",        [469,141,481,154],[483,141,565,154], D["fecha_mes"],  sm))
    fields.append(campo(13,"Unit# inline", [306,154,326,167],[329,154,387,167], D["unidad"]))
    fields.append(campo(13,"Sign day",     [36,575,172,587], [174,575,201,587], D["fecha_dia"],  sm))
    fields.append(campo(13,"Sign month",   [204,575,230,587],[233,575,341,587], D["fecha_mes"],  sm))
    fields.append(campo(13,"Name Printed", [288,638,351,651],[353,638,535,651], D["nombre"]))
    fields.append(campo(13,"Unit# sig",    [288,677,346,690],[349,677,491,690], D["unidad"]))

    # ── PÁGINA 14 ────────────────────────────────────────────────────────────
    fields.append(campo(14,"Sign day",     [36,388,88,401],  [90,388,111,401],  D["fecha_dia"],  sm))
    fields.append(campo(14,"Sign month",   [114,388,142,401],[144,388,290,401], D["fecha_mes"],  sm))
    fields.append(campo(14,"Name Printed", [288,540,351,553],[353,540,535,553], D["nombre"]))
    fields.append(campo(14,"Unit# sig",    [288,579,346,592],[349,579,496,592], D["unidad"]))

    # ── PÁGINA 15 ────────────────────────────────────────────────────────────
    fields.append(campo(15,"Owner name top",[36,136,117,149],[118,136,289,149], D["nombre"]))
    fields.append(campo(15,"Unit# top",    [292,136,312,149],[314,136,363,149], D["unidad"]))
    fields.append(campo(15,"Conv Date",    [367,136,469,149],[471,136,576,149], D["fecha_corta"]))
    fields.append(campo(15,"Day inline",   [200,164,215,177],[217,164,249,177], D["fecha_dia"],  sm))
    fields.append(campo(15,"Month inline", [252,164,278,177],[280,164,358,177], D["fecha_mes"],  sm))
    fields.append(campo(15,"Year inline",  [361,164,399,177],[401,164,418,177], D["anio_corto"], sm))

    # ── PÁGINA 16 ────────────────────────────────────────────────────────────
    fields.append(campo(16,"Sign day",     [36,310,87,323],  [88,310,121,323],  D["fecha_dia"],      sm))
    fields.append(campo(16,"Sign month",   [141,310,152,323],[153,310,248,323], D["fecha_mes"],      sm))
    fields.append(campo(16,"Sign year",    [251,310,271,323],[271,310,292,323], D["anio_corto"],     sm))
    fields.append(campo(16,"Owner name",   [36,378,130,391], [132,378,280,391], D["nombre"]))
    fields.append(campo(16,"Unit#",        [36,422,128,435], [130,422,195,435], D["unidad"]))

    # ── PÁGINA 17 ────────────────────────────────────────────────────────────
    fields.append(campo(17,"Unit Address", [36,167,100,180], [102,167,314,180], D["unidad"]))
    fields.append(campo(17,"Owner name 1", [36,216,170,229], [172,216,335,229], D["nombre"]))
    fields.append(campo(17,"Date sig 1",   [389,469,413,482],[415,469,530,482], D["fecha_corta"]))

    return fields


def llenar_pdf(datos: dict, pdf_original_path: str) -> bytes:
    """
    Llena el PDF y retorna los bytes del PDF resultante.
    """
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import FreeText

    fechas = derivar_fechas(datos["fecha_corta"])
    D = {**datos, **fechas}

    reader = PdfReader(pdf_original_path)
    writer = PdfWriter()
    writer.append(reader)

    dims = {}
    for i, page in enumerate(reader.pages):
        dims[i + 1] = (float(page.mediabox.width), float(page.mediabox.height))

    for campo in construir_campos(D):
        texto = campo["entry_text"]["text"]
        if not texto:
            continue

        pg = campo["page_number"]
        pdf_w, pdf_h = dims[pg]
        ebb = campo["entry_bounding_box"]
        font_size = str(campo["entry_text"]["font_size"]) + "pt"

        left   = ebb[0]
        right  = ebb[2]
        top    = pdf_h - ebb[1] - 6
        bottom = pdf_h - ebb[3] - 6

        annotation = FreeText(
            text=texto,
            rect=(left, bottom, right, top),
            font="Arial",
            font_size=font_size,
            font_color="000000",
            border_color=None,
            background_color=None,
        )
        writer.add_annotation(page_number=pg - 1, annotation=annotation)

    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    return buf.read()
