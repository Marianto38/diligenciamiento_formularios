"""
Llenado de formularios PDF de The Club.
Reemplaza: número de unidad, nombre del dueño y fechas de firma.
El resto del contenido (solicitantes, etc.) se mantiene del template.
"""

import io
import os
import fitz  # pymupdf

# Configuración por formulario
_FORMS = {
    'hk1': {
        'pdf':               'The Club- House Keeping Application 1.pdf',
        'unit_content':      '1616',
        'owner_annotation':  'WILSON CARDONA',   # contenido de la anotación a reemplazar
        'date_redact_left':  (90,  246, 180, 278),
        'date_redact_right': (310, 246, 400, 278),
        'date_pt_left':      (109, 268),
        'date_pt_right':     (329, 268),
    },
    'hk2': {
        'pdf':               'The Club- House Keeping Application.pdf',
        'unit_content':      '1616',
        'owner_annotation':  'Wilson Cardona',
        'date_redact_left':  (90,  246, 180, 278),
        'date_redact_right': (310, 246, 400, 278),
        'date_pt_left':      (109, 268),
        'date_pt_right':     (329, 268),
    },
    'pm1': {
        'pdf':               'The Club- Property Manager Application 1.pdf',
        'unit_content':      '1616',
        'owner_annotation':  None,               # el nombre está en el stream, no en anotación
        'owner_redact':      (162, 248, 290, 278),
        'owner_insert':      (171, 270),
        'date_redact_left':  (100, 252, 178, 278),
        'date_redact_right': (320, 252, 398, 278),
        'date_pt_left':      (115, 271),
        'date_pt_right':     (330, 271),
    },
    'pm2': {
        'pdf':               'The Club- Property Manager Application 2.pdf',
        'unit_content':      '1616',
        'owner_annotation':  None,
        'owner_redact':      (172, 249, 285, 276),
        'owner_insert':      (181, 269),
        'date_redact_left':  (100, 252, 178, 278),
        'date_redact_right': (320, 252, 398, 278),
        'date_pt_left':      (115, 271),
        'date_pt_right':     (330, 271),
    },
}


def llenar_club_form(form_id: str, datos: dict, base_dir: str) -> bytes:
    cfg = _FORMS[form_id]
    pdf_path = os.path.join(base_dir, cfg['pdf'])

    nombre = datos['nombre']
    unidad = datos['unidad']
    partes  = datos['fecha_corta'].split('/')
    fecha   = f"{int(partes[0])}/{partes[1]}/{partes[2]}"   # M/DD/YYYY sin cero inicial

    doc    = fitz.open(pdf_path)
    page1  = doc[0]
    page2  = doc[1]

    # ── Página 1: unidad (anotación) ─────────────────────────────────────────
    all_annots = list(page1.annots())
    unit_rect  = None

    for a in all_annots:
        c = a.info.get('content', '')
        if c == cfg['unit_content']:
            unit_rect = fitz.Rect(a.rect)

    targets = {cfg['unit_content']}
    if cfg['owner_annotation']:
        targets.add(cfg['owner_annotation'])

    for a in reversed(all_annots):
        if a.info.get('content', '') in targets:
            page1.delete_annot(a)

    # Nueva anotación de unidad (rect expandido para números más largos)
    if unit_rect is None:
        unit_rect = fitz.Rect(297, 190, 340, 210)
    unit_rect = fitz.Rect(unit_rect.x0, unit_rect.y0,
                          max(unit_rect.x1, unit_rect.x0 + 70), unit_rect.y1)
    page1.add_freetext_annot(unit_rect, unidad,
                             fontsize=14, fontname='helv',
                             text_color=(0, 0, 0), fill_color=(1, 1, 1),
                             border_color=None)

    # ── Página 1: nombre del dueño ────────────────────────────────────────────
    if cfg['owner_annotation']:
        # Era anotación → ya eliminada arriba, solo agregar la nueva
        # Usar rect del hk2 original como fallback
        name_rect = fitz.Rect(177, 255, 330, 276)
        page1.add_freetext_annot(name_rect, nombre,
                                 fontsize=11, fontname='helv',
                                 text_color=(0, 0, 0), fill_color=(1, 1, 1),
                                 border_color=None)
    else:
        # Está en el stream → redactar y reinsertar
        page1.add_redact_annot(fitz.Rect(*cfg['owner_redact']), fill=(1, 1, 1))
        page1.apply_redactions()
        page1.insert_text(fitz.Point(*cfg['owner_insert']), nombre,
                          fontsize=11, color=(0, 0, 0))

    # ── Página 2: fechas de firma ─────────────────────────────────────────────
    page2.add_redact_annot(fitz.Rect(*cfg['date_redact_left']),  fill=(1, 1, 1))
    page2.add_redact_annot(fitz.Rect(*cfg['date_redact_right']), fill=(1, 1, 1))
    page2.apply_redactions()

    page2.insert_text(fitz.Point(*cfg['date_pt_left']),  fecha, fontsize=11, color=(0, 0, 0))
    page2.insert_text(fitz.Point(*cfg['date_pt_right']), fecha, fontsize=11, color=(0, 0, 0))

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()
