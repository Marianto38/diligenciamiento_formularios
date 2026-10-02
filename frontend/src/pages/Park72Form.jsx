import { useState } from 'react'
import { API_BASE } from '../apiBase'

const MEMBER_DEFAULT = {
  nombre:    '',
  direccion: '',
  ciudad:    '',
  estado:    '',
  zip:       '',
  telefono:  '',
  email:     '',
  dl_numero: '',
}

const DEFAULTS = {
  llc_nombre:       '',
  unidad:           '',
  ein:              '',
  fl_sales_tax:     '',
  fecha_aplicacion: '',
  fecha_inicio:     '',
  cert_use:         '',
}

const DATE_RE = /^\d{2}\/\d{2}\/\d{4}$/

export default function Park72Form({ building, form, onBack }) {
  const [data, setData]       = useState(DEFAULTS)
  const [members, setMembers] = useState([{ ...MEMBER_DEFAULT }])
  const [status, setStatus]   = useState(null)
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setData((d) => ({ ...d, [field]: e.target.value }))

  const setMember = (i, field) => (e) => {
    setMembers((ms) => ms.map((m, idx) => idx === i ? { ...m, [field]: e.target.value } : m))
  }

  const addMember = () => setMembers((ms) => [...ms, { ...MEMBER_DEFAULT }])

  const removeMember = (i) => {
    if (members.length === 1) return
    setMembers((ms) => ms.filter((_, idx) => idx !== i))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setStatus(null)

    if (data.fecha_aplicacion && !DATE_RE.test(data.fecha_aplicacion)) {
      setStatus({ type: 'error', msg: 'Fecha de aplicación debe estar en formato MM/DD/YYYY' })
      return
    }
    if (data.fecha_inicio && !DATE_RE.test(data.fecha_inicio)) {
      setStatus({ type: 'error', msg: 'Fecha de inicio debe estar en formato MM/DD/YYYY' })
      return
    }

    setLoading(true)
    setStatus({ type: 'loading', msg: 'Generando documentos…' })

    try {
      const res = await fetch(`${API_BASE}/api/generar-72park`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...data, members }),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Error del servidor')
      }

      const blob = await res.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href     = url
      a.download = `72PARK_BTR_${data.unidad}_${data.llc_nombre.replace(/\s+/g, '_')}.zip`
      a.click()
      URL.revokeObjectURL(url)
      setStatus({ type: 'success', msg: 'ZIP generado y descargado correctamente.' })
    } catch (err) {
      setStatus({ type: 'error', msg: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={s.page}>
      <div style={s.card}>
        <button onClick={onBack} style={s.back}>← Volver</button>

        <div style={s.header}>
          <h1 style={s.title}>{building.name}</h1>
          <p style={s.subtitle}>{form.label}</p>
        </div>

        <form onSubmit={handleSubmit}>

          {/* ── Negocio ─────────────────────────────────────────────────── */}
          <div style={s.sectionTitle}>Información del negocio</div>
          <div style={s.grid}>
            <Field label="Nombre del LLC" required>
              <input style={s.input} value={data.llc_nombre} onChange={set('llc_nombre')}
                placeholder="BAMD LLC" required />
            </Field>
            <Field label="Unidad" required>
              <input style={s.input} value={data.unidad} onChange={set('unidad')}
                placeholder="1406" required />
            </Field>
            <Field label="EIN / Federal ID" required>
              <input style={s.input} value={data.ein} onChange={set('ein')}
                placeholder="47-3977288" required />
            </Field>
            <Field label="FL Sales Tax #" required>
              <input style={s.input} value={data.fl_sales_tax} onChange={set('fl_sales_tax')}
                placeholder="16-802027156-8" required />
            </Field>
            <Field label="Fecha de aplicación" hint="MM/DD/YYYY">
              <input style={s.input} value={data.fecha_aplicacion} onChange={set('fecha_aplicacion')}
                placeholder="04/27/2026" />
            </Field>
            <Field label="Fecha de inicio del negocio" hint="MM/DD/YYYY">
              <input style={s.input} value={data.fecha_inicio} onChange={set('fecha_inicio')}
                placeholder="04/27/2026" />
            </Field>
            <Field label="Certificate of Use #">
              <input style={s.input} value={data.cert_use} onChange={set('cert_use')}
                placeholder="CU-2026-XXXXX" />
            </Field>
          </div>

          {/* ── Miembros ────────────────────────────────────────────────── */}
          <div style={{ ...s.sectionTitle, marginTop: '2rem' }}>
            Miembros de Sunbiz
            <span style={s.badge}>{members.length}</span>
          </div>

          {members.map((m, i) => (
            <div key={i} style={s.memberCard}>
              <div style={s.memberHeader}>
                <span style={s.memberNum}>Miembro {i + 1}</span>
                {members.length > 1 && (
                  <button type="button" style={s.removeBtn} onClick={() => removeMember(i)}>
                    Eliminar
                  </button>
                )}
              </div>
              <div style={s.grid}>
                <Field label="Nombre completo" required span>
                  <input style={s.input} value={m.nombre} onChange={setMember(i, 'nombre')}
                    placeholder="Mehmet Alp Sunar" required />
                </Field>
                <Field label="Dirección" required span>
                  <input style={s.input} value={m.direccion} onChange={setMember(i, 'direccion')}
                    placeholder="Mimar Sinan Mah Yedpa Ticaret Merkezi" required />
                </Field>
                <Field label="Ciudad" required>
                  <input style={s.input} value={m.ciudad} onChange={setMember(i, 'ciudad')}
                    placeholder="Istanbul" required />
                </Field>
                <Field label="Estado / País" required>
                  <input style={s.input} value={m.estado} onChange={setMember(i, 'estado')}
                    placeholder="Turkey" required />
                </Field>
                <Field label="ZIP / Código postal" required>
                  <input style={s.input} value={m.zip} onChange={setMember(i, 'zip')}
                    placeholder="34779" required />
                </Field>
                <Field label="Teléfono" required>
                  <input style={s.input} value={m.telefono} onChange={setMember(i, 'telefono')}
                    placeholder="+90 532 314 46 71" required />
                </Field>
                <Field label="Email" required span>
                  <input style={s.input} type="email" value={m.email} onChange={setMember(i, 'email')}
                    placeholder="name@example.com" required />
                </Field>
                <Field label="DL #" required span>
                  <input style={s.input} value={m.dl_numero} onChange={setMember(i, 'dl_numero')}
                    placeholder="611997" required />
                </Field>
              </div>
            </div>
          ))}

          <button type="button" style={s.addBtn} onClick={addMember}>
            + Agregar miembro
          </button>

          {members.length > 3 && (
            <p style={s.note}>
              Con {members.length} miembros se generará un formulario Resort Tax adicional (11.2).
            </p>
          )}

          {/* ── Submit ──────────────────────────────────────────────────── */}
          <button type="submit" disabled={loading} style={s.btn}>
            {loading ? 'Generando…' : 'Generar ZIP'}
          </button>

          {status && (
            <div style={{ ...s.statusBox, ...s.statusTypes[status.type] }}>
              {status.msg}
            </div>
          )}
        </form>
      </div>
    </div>
  )
}

function Field({ label, hint, required, span, children }) {
  return (
    <label style={{ ...s.field, ...(span ? s.fieldSpan : {}) }}>
      <span style={s.label}>
        {label} {required && <span style={s.req}>*</span>}
        {hint && <span style={s.hint}> — {hint}</span>}
      </span>
      {children}
    </label>
  )
}

const s = {
  page: { padding: '2rem 1rem', display: 'flex', justifyContent: 'center', minHeight: '100vh' },
  card: {
    background: '#fff', borderRadius: 12,
    boxShadow: '0 2px 16px rgba(0,0,0,.08)',
    width: '100%', maxWidth: 720, padding: '2.5rem',
    alignSelf: 'flex-start',
  },
  back: {
    background: 'none', border: 'none', color: '#666',
    fontSize: '.85rem', cursor: 'pointer', padding: 0,
    marginBottom: '1.5rem', display: 'block',
  },
  header: {
    textAlign: 'center', marginBottom: '2rem',
    paddingBottom: '1.5rem', borderBottom: '1px solid #eee',
  },
  title:    { fontSize: '1.5rem', fontWeight: 700, color: '#111' },
  subtitle: { marginTop: '.3rem', fontSize: '.875rem', color: '#666' },
  sectionTitle: {
    fontSize: '.75rem', fontWeight: 700, textTransform: 'uppercase',
    letterSpacing: '1px', color: '#888', margin: '1.75rem 0 .75rem',
    display: 'flex', alignItems: 'center', gap: '.5rem',
  },
  badge: {
    background: '#1a1a1a', color: '#fff', borderRadius: 99,
    fontSize: '.7rem', padding: '1px 7px', fontWeight: 600,
  },
  grid:      { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '.75rem' },
  field:     { display: 'flex', flexDirection: 'column', gap: '.3rem' },
  fieldSpan: { gridColumn: '1 / -1' },
  label:     { fontSize: '.8125rem', fontWeight: 600, color: '#444' },
  req:       { color: '#c0392b' },
  hint:      { fontWeight: 400, color: '#999', fontSize: '.75rem' },
  input: {
    border: '1px solid #ddd', borderRadius: 6,
    padding: '.5rem .75rem', fontSize: '.9375rem',
    color: '#111', background: '#fafafa',
    outline: 'none', width: '100%', boxSizing: 'border-box',
  },
  memberCard: {
    border: '1px solid #e5e5e5', borderRadius: 8,
    padding: '1.25rem', marginBottom: '.75rem',
    background: '#fafafa',
  },
  memberHeader: {
    display: 'flex', justifyContent: 'space-between',
    alignItems: 'center', marginBottom: '.75rem',
  },
  memberNum:  { fontSize: '.8rem', fontWeight: 700, color: '#555', textTransform: 'uppercase', letterSpacing: '.5px' },
  removeBtn: {
    background: 'none', border: '1px solid #fca5a5',
    color: '#c0392b', borderRadius: 5, padding: '2px 10px',
    fontSize: '.78rem', cursor: 'pointer',
  },
  addBtn: {
    marginTop: '.5rem', width: '100%',
    padding: '.6rem', background: '#fff',
    border: '1px dashed #bbb', borderRadius: 8,
    color: '#555', fontSize: '.875rem',
    fontWeight: 500, cursor: 'pointer',
  },
  note: { marginTop: '.6rem', fontSize: '.8rem', color: '#0369a1', background: '#f0f9ff', borderRadius: 6, padding: '.5rem .75rem' },
  btn: {
    marginTop: '2rem', width: '100%', padding: '.85rem',
    background: '#1a1a1a', color: '#fff', border: 'none',
    borderRadius: 8, fontSize: '1rem', fontWeight: 600, cursor: 'pointer',
  },
  statusBox: { marginTop: '1rem', padding: '.75rem 1rem', borderRadius: 6, fontSize: '.875rem' },
  statusTypes: {
    error:   { background: '#fef2f2', color: '#c0392b', border: '1px solid #fca5a5' },
    success: { background: '#f0fdf4', color: '#166534', border: '1px solid #86efac' },
    loading: { background: '#f0f9ff', color: '#0369a1', border: '1px solid #7dd3fc' },
  },
}
