const BUILDINGS = [
  {
    id: 'crosby',
    name: 'The Crosby',
    forms: [
      { id: 'orientation', label: 'Owners Orientation Package', available: true },
      { id: 'key-release', label: 'Key Release', available: false },
    ],
  },
  {
    id: '501first',
    name: '501 First',
    forms: [
      { id: 'orientation', label: 'Owners Orientation Package', available: false },
      { id: 'key-release', label: 'Key Release', available: false },
    ],
  },
  {
    id: 'district225',
    name: 'District 225',
    forms: [
      { id: 'orientation', label: 'Owners Orientation Package', available: true },
      { id: 'key-release', label: 'Key Release', available: false },
    ],
  },
  {
    id: '72park',
    name: '72 Park',
    forms: [
      { id: 'btr', label: 'BTR — Licencia de negocio', available: true },
    ],
  },
  {
    id: 'club',
    name: 'The Club',
    forms: [
      { id: 'paquete', label: 'Paquete completo (4 formularios)', available: true },
      { id: 'rental',  label: 'Short Term Rental Agreement',       available: false },
    ],
  },
  {
    id: 'nomad',
    name: 'Nomad Residences Wynwood',
    forms: [
      { id: 'orientation', label: 'Owners Orientation Package', available: true },
    ],
  },
]

export default function Home({ onNavigate }) {
  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <h1 style={styles.title}>Diligenciamiento de Formularios</h1>
        <p style={styles.subtitle}>Selecciona un edificio para generar sus formularios</p>
      </div>

      <div style={styles.grid}>
        {BUILDINGS.map((building) => (
          <div key={building.id} style={styles.card}>
            <div style={styles.cardHeader}>
              <span style={styles.cardIcon}>🏢</span>
              <h2 style={styles.cardTitle}>{building.name}</h2>
            </div>
            <div style={styles.formList}>
              {building.forms.map((form) => (
                <button
                  key={form.id}
                  style={{
                    ...styles.formBtn,
                    ...(form.available ? styles.formBtnActive : styles.formBtnDisabled),
                  }}
                  disabled={!form.available}
                  onClick={() => form.available && onNavigate(building, form)}
                >
                  <span style={styles.formBtnDot(form.available)} />
                  {form.label}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const styles = {
  page: {
    padding: '2.5rem 1.5rem',
    maxWidth: 900,
    margin: '0 auto',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2.5rem',
  },
  title: {
    fontSize: '1.75rem',
    fontWeight: 700,
    letterSpacing: '.3px',
    color: '#111',
    marginBottom: '.5rem',
  },
  subtitle: {
    fontSize: '.9rem',
    color: '#888',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '1.25rem',
  },
  card: {
    background: '#fff',
    borderRadius: 12,
    boxShadow: '0 2px 16px rgba(0,0,0,.07)',
    padding: '1.5rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  cardHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '.6rem',
    paddingBottom: '.75rem',
    borderBottom: '1px solid #eee',
  },
  cardIcon: {
    fontSize: '1.25rem',
  },
  cardTitle: {
    fontSize: '1rem',
    fontWeight: 700,
    color: '#111',
    letterSpacing: '.3px',
  },
  formList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '.5rem',
  },
  formBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '.5rem',
    padding: '.55rem .75rem',
    borderRadius: 7,
    border: '1px solid',
    fontSize: '.82rem',
    fontWeight: 500,
    cursor: 'pointer',
    textAlign: 'left',
    transition: 'background .15s',
  },
  formBtnActive: {
    background: '#1a1a1a',
    borderColor: '#1a1a1a',
    color: '#fff',
  },
  formBtnDisabled: {
    background: '#fafafa',
    borderColor: '#e5e5e5',
    color: '#bbb',
    cursor: 'not-allowed',
  },
  formBtnDot: (active) => ({
    width: 7,
    height: 7,
    borderRadius: '50%',
    background: active ? '#4ade80' : '#ddd',
    flexShrink: 0,
  }),
}
