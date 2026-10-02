// En desarrollo queda vacío y Vite usa el proxy a localhost:5050 (ver vite.config.js).
// En Vercel se define VITE_API_URL apuntando al backend de Render.
export const API_BASE = import.meta.env.VITE_API_URL || ''
