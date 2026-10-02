import { useState } from 'react'
import { API_BASE } from '../apiBase'

export default function NexoTransientForm({ building, form, onBack }) {
  const [data, setData] = useState({
    nombre:               '',
    unidad:               '',
    fecha_corta:          '',
    telefono:             '',
    email1:               '',
    fecha_inicio_renta:   '',
    tipo_gestion:         'AvantStay',
    mgmt_nombre:          '',
    mgmt_email:           '',
    mgmt_contacto:        '',
    mgmt_telefono:        '',
    contacto247_nombre:     '',
    contacto247_email:      '',
    contacto247_telefono:   '',
    contacto247_afterhours: '',
  })
  const [status,  setStatus]  = useState(null)
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setData((d) => ({ ...d, [field]: e.target.value }))

  async function handleSubmit(e) {
    e.preventDefault()
    setStatus(null)

    if (!/^\d{2}\/\d{2}\/\d{4}$/.test(data.fecha_corta)) {
      setStatus({ type: 'error', msg: 'La fecha de aplicación debe estar en formato MM/DD/YYYY' })
      return
    }
    if (!/^\d{2}\/\d{2}\/\d{4}$/.test(data.fecha_inicio_renta)) {
      setStatus({ type: 'error', msg: 'La fecha de inicio de renta debe estar en formato MM/DD/YYYY' })
      return
    }

    setLoading(true)
    setStatus({ type: 'loading', msg: 'Generando PDF…' })

    try {
      const res = await fetch(`${API_BASE}/api/generar-nexo-transient`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(data),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Error del servidor')
      }

      const blob = await res.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href     = url
      a.download = `Nexo_Transient_${data.unidad}_${data.nombre.replace(/\s+/g, '_')}_filled.pdf`
      a.click()
      URL.revokeObjectURL(url)
      setStatus({ type: 'success', msg: 'PDF generado y descargado correctamente.' })
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

          <div style={s.sectionTitle}>Información del propietario</div>
          <div style={s.grid}>
            <Field label="Nombre del dueño" required span>
              <input style={s.input} value={data.nombre} onChange={set('nombre')}
                placeholder="Wilson Cardona" required />
            </Field>
            <Field label="Unidad" required>
              <input style={s.input} value={data.unidad} onChange={set('unidad')}
                placeholder="1201" required />
            </Field>
            <Field label="Fecha de aplicación" hint="MM/DD/YYYY" required>
              <input style={s.input} value={data.fecha_corta} onChange={set('fecha_corta')}
                placeholder="10/02/2026" pattern="\d{2}/\d{2}/\d{4}" required />
            </Field>
          </div>

          <div style={s.sectionTitle}>Contacto</div>
          <div style={s.grid}>
            <Field label="Teléfono celular" required>
              <input style={s.input} value={data.telefono} onChange={set('telefono')}
                placeholder="786-555-1234" required />
            </Field>
            <Field label="Email" required>
              <input style={s.input} type="email" value={data.email1} onChange={set('email1')}
                placeholder="owner@example.com" required />
            </Field>
          </div>

          <div style={s.sectionTitle}>Detalles del alquiler</div>
          <div style={s.grid}>
            <Field label="Fecha de inicio de renta" hint="MM/DD/YYYY" required>
              <input style={s.input} value={data.fecha_inicio_renta} onChange={set('fecha_inicio_renta')}
                placeholder="11/01/2026" pattern="\d{2}/\d{2}/\d{4}" required />
            </Field>
            <Field label="Entidad que administra" required>
              <select style={s.input} value={data.tipo_gestion} onChange={set('tipo_gestion')}>
                <option value="AvantStay">AvantStay</option>
                <option value="SelfManaged">Self-Managed</option>
                <option value="Other">Other (compañía externa)</option>
              </select>
            </Field>
          </div>

          {data.tipo_gestion === 'Other' && (
            <>
              <div style={s.sectionTitle}>Compañía de gestión (opcional)</div>
              <div style={s.grid}>
                <Field label="Nombre de la compañía">
                  <input style={s.input} value={data.mgmt_nombre} onChange={set('mgmt_nombre')}
                    placeholder="Acme Rentals LLC" />
                </Field>
                <Field label="Email">
                  <input style={s.input} type="email" value={data.mgmt_email} onChange={set('mgmt_email')}
                    placeholder="ops@acmerentals.com" />
                </Field>
                <Field label="Nombre de contacto">
                  <input style={s.input} value={data.mgmt_contacto} onChange={set('mgmt_contacto')}
                    placeholder="Jane Doe" />
                </Field>
                <Field label="Teléfono">
                  <input style={s.input} value={data.mgmt_telefono} onChange={set('mgmt_telefono')}
                    placeholder="305-555-0000" />
                </Field>
              </div>
            </>
          )}

          <div style={s.sectionTitle}>Contacto designado 24/7 (opcional)</div>
          <div style={s.grid}>
            <Field label="Nombre / compañía" span>
              <input style={s.input} value={data.contacto247_nombre} onChange={set('contacto247_nombre')}
                placeholder="Jane Doe / Acme Rentals LLC" />
            </Field>
            <Field label="Email">
              <input style={s.input} type="email" value={data.contacto247_email} onChange={set('contacto247_email')}
                placeholder="contacto@acmerentals.com" />
            </Field>
            <Field label="Teléfono principal">
              <input style={s.input} value={data.contacto247_telefono} onChange={set('contacto247_telefono')}
                placeholder="305-555-0001" />
            </Field>
            <Field label="Teléfono fuera de horario">
              <input style={s.input} value={data.contacto247_afterhours} onChange={set('contacto247_afterhours')}
                placeholder="305-555-0002" />
            </Field>
          </div>

          <button type="submit" disabled={loading} style={s.btn}>
            {loading ? 'Generando…' : 'Generar PDF'}
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
        {hint && <span style={s.labelHint}> — {hint}</span>}
      </span>
      {children}
    </label>
  )
}

const s = {
  page:     { padding: '2rem 1rem', display: 'flex', justifyContent: 'center', alignItems: 'flex-start', minHeight: '100vh' },
  card:     { background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px rgba(0,0,0,.08)', width: '100%', maxWidth: 540, padding: '2.5rem' },
  back:     { background: 'none', border: 'none', color: '#666', fontSize: '.85rem', cursor: 'pointer', padding: 0, marginBottom: '1.5rem', display: 'block' },
  header:   { textAlign: 'center', marginBottom: '2rem', paddingBottom: '1.5rem', borderBottom: '1px solid #eee' },
  title:    { fontSize: '1.5rem', fontWeight: 700, color: '#111', letterSpacing: '.5px' },
  subtitle: { marginTop: '.3rem', fontSize: '.875rem', color: '#666' },
  sectionTitle: { fontSize: '.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', color: '#888', margin: '1.75rem 0 .75rem' },
  grid:     { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '.75rem' },
  field:    { display: 'flex', flexDirection: 'column', gap: '.3rem' },
  fieldSpan:{ gridColumn: '1 / -1' },
  label:    { fontSize: '.8125rem', fontWeight: 600, color: '#444' },
  labelHint:{ fontWeight: 400, color: '#999', fontSize: '.75rem' },
  req:      { color: '#c0392b' },
  input:    { border: '1px solid #ddd', borderRadius: 6, padding: '.5rem .75rem', fontSize: '.9375rem', color: '#111', background: '#fafafa', outline: 'none', width: '100%' },
  btn:      { marginTop: '2rem', width: '100%', padding: '.85rem', background: '#1a1a1a', color: '#fff', border: 'none', borderRadius: 8, fontSize: '1rem', fontWeight: 600, cursor: 'pointer' },
  statusBox:{ marginTop: '1rem', padding: '.75rem 1rem', borderRadius: 6, fontSize: '.875rem' },
  statusTypes: {
    error:   { background: '#fef2f2', color: '#c0392b', border: '1px solid #fca5a5' },
    success: { background: '#f0fdf4', color: '#166534', border: '1px solid #86efac' },
    loading: { background: '#f0f9ff', color: '#0369a1', border: '1px solid #7dd3fc' },
  },
}
