export default function Sidebar() {
  return (
    <div className="w-64 bg-[#003A8F] text-white p-4 flex flex-col">
      
      <h1 className="text-lg font-semibold mb-6">
        ActividadPro
      </h1>

      <nav className="space-y-2 text-sm">
        
        <div className="px-3 py-2 rounded-lg bg-yellow-400 text-blue-900 font-medium">
          Inicio
        </div>

        <div className="px-3 py-2 rounded-lg hover:bg-blue-700 cursor-pointer">
          Historial
        </div>

        <div className="px-3 py-2 rounded-lg hover:bg-blue-700 cursor-pointer">
          Categorías
        </div>

        <div className="pl-4 text-xs text-blue-200 space-y-1">
          <div>Inicio de sesión</div>
          <div>Errores de red</div>
          <div>Problemas de carga</div>
          <div>Configuración</div>
        </div>

      </nav>

      <div className="mt-auto text-xs text-blue-300">
        v1.0
      </div>
    </div>
  )
}