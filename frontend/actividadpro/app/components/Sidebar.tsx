"use client";

import PruebasAutomaticasModal from "./PruebasAutomaticasModal";
import { useState } from "react";

type RagType = "actividadpro" | "carbot";

type Props = {
  ragActivo: RagType;
  setRagActivo: (rag: RagType) => void;
};

export default function Sidebar({ ragActivo, setRagActivo }: Props) {
  const [openPruebas, setOpenPruebas] = useState(false);

  const cambiarRag = () => {
    setRagActivo(prev =>
      prev === "actividadpro" ? "carbot" : "actividadpro"
    );
  };

  return (
    <>
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

          <div
            className="px-3 py-2 rounded-lg hover:bg-blue-700 cursor-pointer"
            onClick={() => setOpenPruebas(true)}
          >
            Pruebas Automáticas
          </div>

          {/* ✅ BOTÓN RAG REAL */}
          <div
            className="px-3 py-2 rounded-lg hover:bg-blue-700 cursor-pointer"
            onClick={cambiarRag}
          >
            RAG: {ragActivo === "actividadpro" ? "Actividad Pro" : "CarBot"}
          </div>
        </nav>

        <div className="mt-auto text-xs text-blue-300">
          v1.0
        </div>
      </div>

      <PruebasAutomaticasModal
        open={openPruebas}
        onClose={() => setOpenPruebas(false)}
      />
    </>
  );
}