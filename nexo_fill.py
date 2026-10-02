"""
Módulo para llenar el PDF de Nexo Residences — New Owner Orientation Packet.

A diferencia de los otros edificios, este PDF tiene campos de formulario reales
(AcroForm widgets), así que se llenan por nombre de campo en vez de coordenadas.
Las firmas físicas y los campos opcionales (co-dueño, residentes, visitantes,
vehículos, mascotas, personas autorizadas, cantidades de llaves) se dejan en
blanco para completarse a mano.
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
    anio_sufijo = anio[3:] if anio.startswith('202') else anio[2:]
    return {
        'fecha_corta':  fecha_corta,
        'fecha_dia':    str(int(dia)),
        'fecha_mes':    mes_nombre,
        'anio':         anio,
        'anio_sufijo':  anio_sufijo,
    }


def construir_mapa_campos(D):
    """Campos de tipo Text/CheckBox que se llenan vía widget.field_value (nombre exacto)."""
    return {
        # ── PÁGINA 3 — Unit Owner Information ──────────────────────────────
        'UNIT NUMBERRow1':                              D['unidad'],
        'OWNER 1  FULL LEGAL NAMERow1':                 D['nombre'],
        'EMAIL ADDRESSRow1':                             D['email1'],
        'PHONE NUMBERRow1':                              D['telefono'],
        'EMERGENCY CONTACT 1  FULL NAMERow1':           D['contacto_emerg'],
        'PRIMARY PHONERow1':                             D['tel_emerg'],
        'UNIT OWNER  PRINT NAMERow1':                    D['nombre'],
        'DATERow1':                                      D['fecha_corta'],

        # ── PÁGINA 6 — Vehicles & Authorized Custodian (firma) ─────────────
        'UNIT OWNER  PRINT NAMERow1_2':                  D['nombre'],
        'DATERow1_3':                                    D['fecha_corta'],

        # ── PÁGINA 9 — Pet Registration (firma) ─────────────────────────────
        'UNIT NUMBERRow1_2':                             D['unidad'],
        'UNIT OWNER  PRINT NAMERow1_3':                  D['nombre'],
        'DATERow1_5':                                    D['fecha_corta'],

        # ── PÁGINA 10 — Bicycle Registration (firma) ────────────────────────
        'UNIT OWNER  PRINT NAMERow1_4':                  D['nombre'],
        'DATERow1_7':                                    D['fecha_corta'],

        # ── PÁGINA 12 — Moving Van / Truck Parking (firma) ──────────────────
        'UNIT OWNER  PRINT NAMERow1_5':                  D['nombre'],
        'DATERow1_9':                                    D['fecha_corta'],

        # ── PÁGINA 13 — Deliveries & Package Receipt (texto narrativo) ──────
        'This Release Indemnity and Hold Harmless Agreement Release is executed on this': D['fecha_dia'],
        'day of':                                        D['fecha_mes'],
        'andor Permitted User':                          D['nombre'],
        'of Unit Number':                                D['unidad'],

        # ── PÁGINA 14 — (texto narrativo + firma) ───────────────────────────
        'day of_2':                                      D['fecha_dia'],
        '2026':                                           D['fecha_mes'],
        'UNIT OWNER  PRINT NAMERow1_6':                  D['nombre'],
        'DATERow1_11':                                   D['fecha_corta'],

        # ── PÁGINA 15 — Fitness & Pool Waiver (texto narrativo) ─────────────
        '2026  by':                                       f"{D['fecha_mes']} {D['fecha_dia']}",
        'Unit Owner in favor of the Released Parties as hereinafter defined on': D['nombre'],

        # ── PÁGINA 16 — (firma) ──────────────────────────────────────────────
        'UNIT OWNER  PRINT NAMERow1_7':                  D['nombre'],
        'DATERow1_13':                                   D['fecha_corta'],

        # ── PÁGINA 17 — Contractor Release (texto narrativo) ────────────────
        'day':                                            D['fecha_dia'],
        'undefined_4':                                    D['fecha_mes'],
        'who reside at Unit':                             D['nombre'],
        'in Nexo Residences':                             D['unidad'],

        # ── PÁGINA 18 — (firma) ──────────────────────────────────────────────
        'UNIT OWNER  PRINT NAMERow1_8':                  D['nombre'],
        'DATERow1_15':                                   D['fecha_corta'],

        # ── PÁGINA 19 — Voting Certificate (texto narrativo + firma) ────────
        'day of_3':                                       D['fecha_mes'],
        '202':                                            D['anio_sufijo'],
        'Print Name':                                     D['nombre'],

        # ── PÁGINA 20 — Electric Transfer Acknowledgement ───────────────────
        'day of_4':                                       D['fecha_dia'],
        '202_2':                                          D['fecha_mes'],
        'as':                                              D['nombre'],
        'in Nexo Residences Condominium Association the Condominium concerning the': D['unidad'],
        'UNIT OWNER  PRINT NAMERow1_9':                  D['nombre'],
        'DATERow1_17':                                   D['fecha_corta'],

        # ── PÁGINA 22 — Authorized Persons (texto narrativo + firma) ────────
        'day of_5':                                       D['fecha_mes'],
        '202_3':                                          D['anio_sufijo'],
        'UNIT OWNER  PRINT NAMERow1_10':                 D['nombre'],
        'DATERow1_19':                                   D['fecha_corta'],

        # ── PÁGINA 23 — Keys, Forms & Information Receipt (firma) ──────────
        'UNIT OWNER  PRINT NAMERow1_11':                 D['nombre'],
        'DATERow1_21':                                   D['fecha_corta'],
    }


def construir_mapa_signature_overlay(D):
    """
    Campos marcados como tipo 'Signature' en el PDF pero usados como blancos de
    texto narrativo (día/unidad). No admiten field_value de forma confiable, así
    que se dibujan directamente sobre la página.
    """
    return {
        # PÁGINA 19 — "...all of the record Owners of UNIT NO. ____"
        'THIS IS TO CERTIFY that the undersigned constituting all of the record Owners of UNIT NO': D['unidad'],
        # PÁGINA 22 — "Signed this: ____ day of ..."
        'Signed this': D['fecha_dia'],
    }


def llenar_pdf(datos: dict, pdf_original_path: str) -> bytes:
    import fitz

    fechas = derivar_fechas(datos['fecha_corta'])
    D = {**datos, **fechas}

    mapa_campos = construir_mapa_campos(D)
    mapa_overlay = construir_mapa_signature_overlay(D)

    doc = fitz.open(pdf_original_path)

    for page in doc:
        for widget in page.widgets() or []:
            nombre_campo = widget.field_name

            if nombre_campo in mapa_campos:
                widget.field_value = mapa_campos[nombre_campo]
                widget.text_fontsize = 10
                widget.update()
            elif nombre_campo in mapa_overlay:
                texto = mapa_overlay[nombre_campo]
                r = widget.rect
                page.insert_text(
                    point=(r.x0 + 2, r.y1 - 3),
                    text=texto,
                    fontsize=9,
                    color=(0, 0, 0),
                    fontname='helv',
                )

    buf = io.BytesIO()
    doc.save(buf, deflate=True, garbage=4, clean=True)
    buf.seek(0)
    return buf.read()
