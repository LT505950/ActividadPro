"use client";
import { useState } from "react";

type Chunk = {
  text: string;
  source: string;
};

type TokensInfo = {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
};

type Props = {
  chunks: Chunk[];
  tokensInfo?: TokensInfo;
};

export default function RightPanel({ chunks, tokensInfo }: Props) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  const toggleExpand = (idx: number) => {
    setExpandedIdx(expandedIdx === idx ? null : idx);
  };

  return (
    <div className="w-80 flex-shrink-0 bg-[#f9fafc] border-l border-gray-200 p-4 flex flex-col gap-4 overflow-y-auto">

      {/* Tarjeta de uso de tokens */}
      <div className="bg-white rounded-xl border shadow-sm p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">
        Uso de Tokens
        </h3>
        <div className="flex flex-col gap-2 text-sm">
          <div className="flex justify-between items-center">
            <span className="text-gray-500">Entrada (prompt):</span>
            <span className="font-mono font-semibold text-green-600">
              {tokensInfo ? tokensInfo.prompt_tokens.toLocaleString() : "\u2014"}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-500">Salida (respuesta):</span>
            <span className="font-mono font-semibold text-blue-600">
              {tokensInfo ? tokensInfo.completion_tokens.toLocaleString() : "\u2014"}
            </span>
          </div>
          <div className="border-t pt-2 flex justify-between items-center">
            <span className="text-gray-600 font-medium">Total:</span>
            <span className="font-mono font-bold text-gray-800">
              {tokensInfo ? tokensInfo.total_tokens.toLocaleString() : "\u2014"}
            </span>
          </div>
        </div>
      </div>

      {/* T\u00edtulo fuentes */}
      <h2 className="text-sm font-semibold text-gray-700">
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
              <div className="text-xs font-semibold text-blue-900 mb-1">
                {chunk.source || "Fuente desconocida"}
              </div>
              <div className="text-xs text-gray-600">
                {expandedIdx === idx
                  ? chunk.text
                  : chunk.text.length > 120
                  ? chunk.text.slice(0, 120) + "..."
                  : chunk.text}
              </div>
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
