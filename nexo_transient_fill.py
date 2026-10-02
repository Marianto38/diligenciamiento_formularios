"""
Módulo para llenar el PDF de Nexo Residences — Transient Rental Application.

Igual que el Owner Orientation Packet, este PDF tiene campos de formulario
reales (AcroForm widgets), así que se llenan por nombre de campo. La sección
"FOR ASSOCIATION USE ONLY" (página 5) y las firmas físicas se dejan en blanco.
"""

import io


def construir_mapa_campos(D):
    """Campos de tipo Text que se llenan vía widget.field_value (nombre exacto)."""
    mapa = {
        # ── PÁGINA 2 — Encabezado ────────────────────────────────────────────
        'UNIT Row1':                                D['unidad'],
        'OWNER NAMERow1':                           D['nombre'],
        'APPLICATION DATERow1':                     D['fecha_corta'],

        # ── PÁGINA 4 — 1. Unit Owner Information ────────────────────────────
        'UNIT OWNER 1 NAME':                        D['nombre'],
        'EMAIL ADDRESS':                            D['email1'],
        'MOBILE PHONE':                             D['telefono'],

        # ── PÁGINA 4 — 2. Rental Details ─────────────────────────────────────
        'UNIT NUMBER':                              D['unidad'],
        'PLANNED RENTAL START DATE':                D['fecha_inicio_renta'],

        # ── PÁGINA 10 — Owner Acknowledgment (firma) ─────────────────────────
        'UNIT OWNER  PRINT NAMERow1':                D['nombre'],
        'DATERow1':                                  D['fecha_corta'],
    }

    # Campos opcionales — solo se agregan si el usuario los diligenció.
    opcionales = {
        'COMPANY NAME':                              D.get('mgmt_nombre'),
        'EMAIL ADDRESS_3':                           D.get('mgmt_email'),
        'CONTACT NAME':                              D.get('mgmt_contacto'),
        'PHONE':                                     D.get('mgmt_telefono'),
        'FULL NAME  RENTAL MANAGEMENT COMPANY':      D.get('contacto247_nombre'),
        'EMAIL ADDRESS_4':                           D.get('contacto247_email'),
        'PRIMARY PHONE':                             D.get('contacto247_telefono'),
        'AFTERHOURS PHONE':                          D.get('contacto247_afterhours'),
    }
    for campo, valor in opcionales.items():
        if valor:
            mapa[campo] = valor

    return mapa


# Nombre de campo de checkbox visible -> nombre del campo "espejo" duplicado
# que ocupa el mismo lugar en el PDF (quirk del formulario original).
_MANAGING_ENTITY_CHECKBOXES = {
    'AvantStay':     'Check Box28',
    'SelfManaged':   'Check Box29',
    'Other':         'Check Box30',
}


def construir_checkboxes(D):
    """Devuelve el set de nombres de checkbox (+ su duplicado) que deben marcarse."""
    marcar = set()
    campo = _MANAGING_ENTITY_CHECKBOXES.get(D.get('tipo_gestion'))
    if campo:
        marcar.add(campo)
        marcar.add(_MANAGING_ENTITY_CHECKBOXES[D['tipo_gestion']])
    return marcar


def llenar_pdf(datos: dict, pdf_original_path: str) -> bytes:
    import fitz

    D = dict(datos)
    mapa_campos = construir_mapa_campos(D)
    checkboxes = construir_checkboxes(D)

    doc = fitz.open(pdf_original_path)

    for page in doc:
        for widget in page.widgets() or []:
            nombre_campo = widget.field_name

            if nombre_campo in mapa_campos:
                widget.field_value = mapa_campos[nombre_campo]
                widget.text_fontsize = 10
                widget.update()
            elif nombre_campo in checkboxes:
                widget.field_value = widget.on_state()
                widget.update()

    buf = io.BytesIO()
    doc.save(buf, deflate=True, garbage=4, clean=True)
    buf.seek(0)
    return buf.read()
