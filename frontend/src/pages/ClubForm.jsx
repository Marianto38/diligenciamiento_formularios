import { useState } from 'react'

export default function ClubForm({ building, form, onBack }) {
  const [data, setData] = useState({ nombre: '', unidad: '', fecha_corta: '' })
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setData((d) => ({ ...d, [field]: e.target.value }))

  async function handleSubmit(e) {
    e.preventDefault()
    setStatus(null)

    if (!/^\d{2}\/\d{2}\/\d{4}$/.test(data.fecha_corta)) {
      setStatus({ type: 'error', msg: 'La fecha debe estar en formato MM/DD/YYYY' })
      return
    }

    setLoading(true)
    setStatus({ type: 'loading', msg: 'Generando los 4 formularios…' })

    try {
      const res = await fetch('/api/generar-club', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Error del servidor')
      }

      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `TheClub_${data.unidad}_${data.nombre.replace(/\s+/g, '_')}.zip`
      a.click()
      URL.revokeObjectURL(url)
      setStatus({ type: 'success', msg: 'ZIP descargado con los 4 formularios.' })
    } catch (err) {
      setStatus({ type: 'error', msg: err.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <button onClick={onBack} style={styles.back}>← Volver</button>

        <div style={styles.header}>
          <h1 style={styles.title}>{building.name}</h1>
          <p style={styles.subtitle}>{form.label}</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={styles.sectionTitle}>Información del propietario</div>
          <div style={styles.grid}>
            <Field label="Nombre del dueño" required span>
              <input style={styles.input} value={data.nombre} onChange={set('nombre')}
                placeholder="Wilson Cardona" required />
            </Field>
            <Field label="Unidad" required>
              <input style={styles.input} value={data.unidad} onChange={set('unidad')}
                placeholder="3520" required />
            </Field>
            <Field label="Fecha de firma" hint="MM/DD/YYYY" required>
              <input style={styles.input} value={data.fecha_corta} onChange={set('fecha_corta')}
                placeholder="04/21/2026" pattern="\d{2}/\d{2}/\d{4}" required />
            </Field>
          </div>

          <div style={styles.hint}>
            Se generarán los 4 formularios en un solo archivo ZIP.
          </div>

          <button type="submit" disabled={loading} style={styles.btn}>
            {loading ? 'Generando…' : 'Generar formularios'}
          </button>

          {status && (
            <div style={{ ...styles.status, ...styles.statusTypes[status.type] }}>
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
    <label style={{ ...styles.field, ...(span ? styles.fieldSpan : {}) }}>
      <span style={styles.label}>
        {label} {required && <span style={styles.req}>*</span>}
        {hint && <span style={styles.labelHint}> — {hint}</span>}
      </span>
      {children}
    </label>
  )
}

const styles = {
  page:        { padding: '2rem 1rem', display: 'flex', justifyContent: 'center', alignItems: 'flex-start', minHeight: '100vh' },
  card:        { background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px rgba(0,0,0,.08)', width: '100%', maxWidth: 540, padding: '2.5rem' },
  back:        { background: 'none', border: 'none', color: '#666', fontSize: '.85rem', cursor: 'pointer', padding: 0, marginBottom: '1.5rem', display: 'block' },
  header:      { textAlign: 'center', marginBottom: '2rem', paddingBottom: '1.5rem', borderBottom: '1px solid #eee' },
  title:       { fontSize: '1.5rem', fontWeight: 700, color: '#111', letterSpacing: '.5px' },
  subtitle:    { marginTop: '.3rem', fontSize: '.875rem', color: '#666' },
  sectionTitle:{ fontSize: '.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', color: '#888', margin: '1.75rem 0 .75rem' },
  grid:        { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '.75rem' },
  field:       { display: 'flex', flexDirection: 'column', gap: '.3rem' },
  fieldSpan:   { gridColumn: '1 / -1' },
  label:       { fontSize: '.8125rem', fontWeight: 600, color: '#444' },
  labelHint:   { fontWeight: 400, color: '#999', fontSize: '.75rem' },
  req:         { color: '#c0392b' },
  hint:        { marginTop: '1.25rem', fontSize: '.8rem', color: '#999', textAlign: 'center' },
  input:       { border: '1px solid #ddd', borderRadius: 6, padding: '.5rem .75rem', fontSize: '.9375rem', color: '#111', background: '#fafafa', outline: 'none', width: '100%' },
  btn:         { marginTop: '1rem', width: '100%', padding: '.85rem', background: '#1a1a1a', color: '#fff', border: 'none', borderRadius: 8, fontSize: '1rem', fontWeight: 600, cursor: 'pointer' },
  status:      { marginTop: '1rem', padding: '.75rem 1rem', borderRadius: 6, fontSize: '.875rem' },
  statusTypes: {
    error:   { background: '#fef2f2', color: '#c0392b', border: '1px solid #fca5a5' },
    success: { background: '#f0fdf4', color: '#166534', border: '1px solid #86efac' },
    loading: { background: '#f0f9ff', color: '#0369a1', border: '1px solid #7dd3fc' },
  },
}
