"use client";

import { useState } from "react";

type Chunk = {
  text: string;
  source: string;
};

type Props = {
  chunks: Chunk[];
};

export default function RightPanel({ chunks }: Props) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  const toggleExpand = (idx: number) => {
    setExpandedIdx(expandedIdx === idx ? null : idx);
  };

  return (
    <div className="w-80 flex-shrink-0 bg-[#f9fafc] border-l border-gray-200 p-4 flex flex-col">
      
      {/* Título */}
      <h2 className="text-sm font-semibold mb-4 text-gray-700">
        Fuentes utilizadas (RAG)
      </h2>

      {/* Lista de chunks */}
      <div className="space-y-3 overflow-y-auto flex-1">
        {chunks.length > 0 ? (
          chunks.map((chunk, idx) => (
            <div
              key={idx}
              onClick={() => toggleExpand(idx)}
              className="bg-white p-3 rounded-lg border shadow-sm cursor-pointer hover:bg-gray-50 transition"
            >
              {/* Fuente */}
              <div className="text-xs font-semibold text-blue-900 mb-1">
                {chunk.source || "Fuente desconocida"}
              </div>

              {/* Texto */}
              <div className="text-xs text-gray-600">
                {expandedIdx === idx
                  ? chunk.text
                  : chunk.text.length > 120
                  ? chunk.text.slice(0, 120) + "..."
                  : chunk.text}
              </div>

              {/* Hint */}
              <div className="text-[10px] text-gray-400 mt-1">
                {expandedIdx === idx ? "Click para contraer" : "Click para expandir"}
              </div>
            </div>
          ))
        ) : (
          <div className="text-gray-400 text-sm">
            Aquí se mostrarán los chunks utilizados por el modelo.
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="mt-4 text-xs text-gray-400">
        Mostrando contexto real del modelo
      </div>
    </div>
  );
}