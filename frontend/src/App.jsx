import { useState } from 'react'
import Home from './pages/Home'
import CrosbyForm from './pages/CrosbyForm'
import ClubForm from './pages/ClubForm'
import Park72Form from './pages/Park72Form'
import NomadForm from './pages/NomadForm'
import District225Form from './pages/District225Form'
import NexoForm from './pages/NexoForm'

export default function App() {
  const [page, setPage] = useState({ name: 'home' })

  if (page.name === 'form') {
    const { building, form } = page
    const back = () => setPage({ name: 'home' })

    if (building.id === 'club')   return <ClubForm    building={building} form={form} onBack={back} />
    if (building.id === '72park') return <Park72Form  building={building} form={form} onBack={back} />
    if (building.id === 'nomad')  return <NomadForm   building={building} form={form} onBack={back} />
    if (building.id === 'district225') return <District225Form building={building} form={form} onBack={back} />
    if (building.id === 'nexo')  return <NexoForm    building={building} form={form} onBack={back} />

    return <CrosbyForm building={building} form={form} onBack={back} />
  }

  return (
    <Home
      onNavigate={(building, form) => setPage({ name: 'form', building, form })}
    />
  )
}
