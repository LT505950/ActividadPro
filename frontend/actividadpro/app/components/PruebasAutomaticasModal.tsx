"use client";

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function PruebasAutomaticasModal({ open, onClose }: Props) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      
      <div className="w-[90%] h-[90%] bg-white rounded-xl shadow-lg flex flex-col">

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b">
          <h2 className="text-lg font-semibold text-[#003A8F]">
            Pruebas Automáticas
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-800 text-xl"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 p-6 overflow-auto">
          <div className="text-sm text-gray-600 mb-4">
            Listado de pruebas
          </div>

          <div className="border border-dashed rounded-lg p-6 text-center text-gray-400 text-sm">
            Aún no existen pruebas automáticas
          </div>
        </div>

        {/* Footer */}
        <div className="border-t px-6 py-4 flex justify-end">
          <button className="bg-yellow-400 text-blue-900 px-4 py-2 rounded-lg text-sm font-medium hover:bg-yellow-300">
            Iniciar nueva prueba automática
          </button>
        </div>

      </div>
    </div>
  );
}