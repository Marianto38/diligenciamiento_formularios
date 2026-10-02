# PDF Filler — Formularios de Propietarios

Aplicación web para generar automáticamente formularios en PDF para múltiples edificios.

## Formularios disponibles

| Edificio | Formulario | Estado |
|---|---|---|
| The Crosby | Owners Orientation Package | ✅ Disponible |
| The Club | House Keeping Application | ✅ Disponible |
| 501 First | Owners Orientation Package | — En desarrollo |
| District 225 | Owners Orientation Package | — En desarrollo |
| Nexo Residences | Owner Orientation Packet | ✅ Disponible |

---

## Puesta en marcha

### Requisitos previos

- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)

---

### Paso 1 — Instalar dependencias (solo la primera vez)

**Python:**
```bash
pip install -r requirements.txt
```

**Node (frontend):**
```bash
cd frontend
npm install
cd ..
```

---

### Paso 2 — Compilar el frontend (solo la primera vez, o al modificar `frontend/`)

```bash
cd frontend
npm run build
cd ..
```

Esto genera la carpeta `public/` que Flask sirve como interfaz web.

---

### Paso 3 — Levantar el servidor

```bash
python server.py
```

Abrir en el navegador: [http://localhost:5050](http://localhost:5050)

Para usar un puerto distinto:
```bash
set PORT=8080 && python server.py   # Windows
PORT=8080 python server.py          # Mac / Linux
```

---

## Modo desarrollo (hot-reload)

Útil cuando se están modificando archivos del frontend. Requiere dos terminales abiertas:

**Terminal 1 — Backend:**
```bash
python server.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Abrir en: [http://localhost:5173](http://localhost:5173)
_(las llamadas a `/api` se redirigen automáticamente a Flask en el puerto 5050)_

---

## Uso

1. Selecciona el edificio y el formulario en la pantalla de inicio
2. Completa los campos requeridos
3. Haz clic en **Generar PDF** — el archivo se descarga automáticamente

### The Crosby — Owners Orientation Package
Campos: nombre, unidad, fecha (MM/DD/YYYY), teléfono, email, contacto de emergencia, portadores de llave (opcional).
Archivo: `The_Crosby_[UNIDAD]_[NOMBRE]_filled.pdf`

### The Club — House Keeping Application
Campos: nombre del dueño, unidad, fecha de firma (MM/DD/YYYY).
El resto del formulario (solicitante, co-solicitante) se mantiene del template.
Archivo: `TheClub_[UNIDAD]_[NOMBRE]_HouseKeeping.pdf`

---

## Estructura del proyecto

```
crosby-pdf/
├── server.py                          # Servidor Flask (puerto 5050)
├── crosby_fill.py                     # Lógica de llenado — The Crosby
├── the_club_fill.py                   # Lógica de llenado — The Club
├── requirements.txt                   # Dependencias Python
├── frontend/                          # App React + Vite
│   ├── vite.config.js                 # build.outDir → ../public
│   └── src/
│       ├── App.jsx
│       └── pages/
│           ├── Home.jsx
│           ├── CrosbyForm.jsx
│           └── ClubHouseKeepingForm.jsx
├── public/                            # Build del frontend (servido por Flask)
├── The Crosby- Owners Orientation Pkg 9-24-25.pdf
└── The Club- House Keeping Application.pdf
```

## Stack

- **Backend:** Python · Flask · pymupdf
- **Frontend:** React · Vite
- **PDF:** pypdf (The Crosby) · pymupdf (The Club)
