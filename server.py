"""
PDF Filler — Servidor Flask
Genera PDFs llenados para The Crosby y The Club.
"""

import os
import io
import zipfile
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from crosby_fill import llenar_pdf
from the_club_fill import llenar_club_form
from park72_fill import (
    llenar_form10, llenar_form11, llenar_form11_2,
    llenar_form12, llenar_form13, llenar_form14,
)
from nomad_fill import llenar_pdf as llenar_nomad_pdf
from district225_fill import llenar_pdf as llenar_district225_pdf
from nexo_fill import llenar_pdf as llenar_nexo_pdf

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

CLUB_FORM_LABELS = {
    'hk1': 'HouseKeeping1',
    'hk2': 'HouseKeeping2',
    'pm1': 'PropertyManager1',
    'pm2': 'PropertyManager2',
}

CLUB_VALID_FORMS = set(CLUB_FORM_LABELS.keys())


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/generar', methods=['POST'])
def generar():
    try:
        datos = request.get_json()

        for campo in ['nombre', 'unidad', 'fecha_corta', 'telefono', 'email1', 'contacto_emerg', 'tel_emerg']:
            if not datos.get(campo, '').strip():
                return jsonify({'ok': False, 'error': f'Campo requerido: {campo}'}), 400

        pdf_path = os.path.join(BASE_DIR, 'The Crosby- Owners Orientation Pkg 9-24-25.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({'ok': False, 'error': 'PDF original no encontrado en el servidor'}), 500

        pdf_bytes = llenar_pdf(datos, pdf_path)
        nombre_limpio = datos['nombre'].replace(' ', '_')
        filename = f'The_Crosby_{datos["unidad"]}_{nombre_limpio}_filled.pdf'

        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
                         as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/generar-club', methods=['POST'])
def generar_club():
    try:
        datos = request.get_json()

        for campo in ['nombre', 'unidad', 'fecha_corta']:
            if not datos.get(campo, '').strip():
                return jsonify({'ok': False, 'error': f'Campo requerido: {campo}'}), 400

        nombre_limpio = datos['nombre'].replace(' ', '_')
        unidad = datos['unidad']

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for form_id, label in CLUB_FORM_LABELS.items():
                pdf_bytes = llenar_club_form(form_id, datos, BASE_DIR)
                zf.writestr(f'TheClub_{unidad}_{nombre_limpio}_{label}.pdf', pdf_bytes)

        buf.seek(0)
        filename = f'TheClub_{unidad}_{nombre_limpio}.zip'
        return send_file(buf, mimetype='application/zip',
                         as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/generar-72park', methods=['POST'])
def generar_72park():
    try:
        datos = request.get_json()

        for campo in ['llc_nombre', 'unidad', 'ein', 'fl_sales_tax']:
            if not datos.get(campo, '').strip():
                return jsonify({'ok': False, 'error': f'Campo requerido: {campo}'}), 400

        members = datos.get('members', [])
        if not members:
            return jsonify({'ok': False, 'error': 'Se requiere al menos un miembro'}), 400

        park_dir = os.path.join(BASE_DIR, '72 PARK', 'LICENCIA BTR')
        llc      = datos['llc_nombre'].replace(' ', '_')
        unidad   = datos['unidad']

        members = datos.get('members', [])

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f'10_BTR_Application_{unidad}_{llc}.pdf',       llenar_form10(datos, park_dir))
            zf.writestr(f'11_Resort_Tax_{unidad}_{llc}.pdf',             llenar_form11(datos, park_dir))
            if len(members) > 3:
                zf.writestr(f'11.2_Resort_Tax_extra_{unidad}_{llc}.pdf', llenar_form11_2(datos, park_dir))
            zf.writestr(f'12_Disclosure_Letter_{unidad}_{llc}.pdf',      llenar_form12(datos, park_dir))
            zf.writestr(f'13_Affidavit_{unidad}_{llc}.pdf',              llenar_form13(datos, park_dir))
            zf.writestr(f'14_Platforms_Letter_{unidad}_{llc}.pdf',       llenar_form14(datos, park_dir))

        buf.seek(0)
        filename = f'72PARK_BTR_{unidad}_{llc}.zip'
        return send_file(buf, mimetype='application/zip',
                         as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/generar-nomad', methods=['POST'])
def generar_nomad():
    try:
        datos = request.get_json()

        for campo in ['nombre', 'unidad', 'fecha_corta', 'telefono', 'email1', 'contacto_emerg', 'tel_emerg']:
            if not datos.get(campo, '').strip():
                return jsonify({'ok': False, 'error': f'Campo requerido: {campo}'}), 400

        pdf_path = os.path.join(BASE_DIR, 'NOMAD RESIDENCES WYNWOOD ORIENTATION.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({'ok': False, 'error': 'PDF original no encontrado en el servidor'}), 500

        pdf_bytes = llenar_nomad_pdf(datos, pdf_path)
        nombre_limpio = datos['nombre'].replace(' ', '_')
        filename = f'Nomad_{datos["unidad"]}_{nombre_limpio}_filled.pdf'

        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
                         as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/generar-district225', methods=['POST'])
def generar_district225():
    try:
        datos = request.get_json()

        for campo in ['nombre', 'unidad', 'fecha_corta', 'telefono', 'email1', 'contacto_emerg', 'tel_emerg']:
            if not datos.get(campo, '').strip():
                return jsonify({'ok': False, 'error': f'Campo requerido: {campo}'}), 400

        pdf_path = os.path.join(BASE_DIR, 'Orientation Package.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({'ok': False, 'error': 'PDF original no encontrado en el servidor'}), 500

        pdf_bytes = llenar_district225_pdf(datos, pdf_path)
        nombre_limpio = datos['nombre'].replace(' ', '_')
        filename = f'District225_{datos["unidad"]}_{nombre_limpio}_filled.pdf'

        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
                         as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/api/generar-nexo', methods=['POST'])
def generar_nexo():
    try:
        datos = request.get_json()

        for campo in ['nombre', 'unidad', 'fecha_corta', 'telefono', 'email1', 'contacto_emerg', 'tel_emerg']:
            if not datos.get(campo, '').strip():
                return jsonify({'ok': False, 'error': f'Campo requerido: {campo}'}), 400

        pdf_path = os.path.join(BASE_DIR, 'Nexo Residences - New Owner Packet.pdf')
        if not os.path.exists(pdf_path):
            return jsonify({'ok': False, 'error': 'PDF original no encontrado en el servidor'}), 500

        pdf_bytes = llenar_nexo_pdf(datos, pdf_path)
        nombre_limpio = datos['nombre'].replace(' ', '_')
        filename = f'Nexo_{datos["unidad"]}_{nombre_limpio}_filled.pdf'

        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
                         as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    print(f'Abierto en http://localhost:{port}')
    app.run(port=port, debug=True, use_reloader=False)
