"use client";
import PruebasAutomaticasModal from "./PruebasAutomaticasModal";
import { Dispatch, SetStateAction, useEffect, useState } from "react";

type RagType = "actividadpro" | "carbot";

type Conversation = {
  test_id: string;
  turns: {
    role: string;
    content: string;
  }[];
};

type Props = {
  ragActivo: RagType;
  setRagActivo: Dispatch<SetStateAction<RagType>>;
};

export default function Sidebar({ ragActivo, setRagActivo }: Props) {
  const [openPruebas, setOpenPruebas] = useState(false);
  const [openHistorial, setOpenHistorial] = useState(false);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [limit, setLimit] = useState(10);

  const cambiarRag = () => {
    setRagActivo((prev) =>
      prev === "actividadpro" ? "carbot" : "actividadpro"
    );
  };

  useEffect(() => {
    if (!openHistorial) return;

    fetch("/api/conversations")
      .then((res) => res.json())
      .then((data) => setConversations(data));
  }, [openHistorial]);

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

          <div
            className="px-3 py-2 rounded-lg hover:bg-blue-700 cursor-pointer"
            onClick={() => setOpenHistorial((p) => !p)}
          >
            Historial
          </div>

          {openHistorial &&
            conversations.slice(0, limit).map((c) => (
              <div key={c.test_id} className="px-6 text-xs">
                {c.turns[0]?.content || "Conversación"}
              </div>
            ))}

          {openHistorial && limit < conversations.length && (
            <div
              className="px-6 text-xs cursor-pointer"
              onClick={() => setLimit((p) => p + 10)}
            >
              Mostrar más
            </div>
          )}

          <div
            className="px-3 py-2 rounded-lg hover:bg-blue-700 cursor-pointer"
            onClick={() => setOpenPruebas(true)}
          >
            Pruebas Automáticas
          </div>

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
        ragActivo={ragActivo}
      />
    </>
  );
}