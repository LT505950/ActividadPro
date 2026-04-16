"use client";
import { useEffect, useRef, useState } from "react";

type RagType = "actividadpro" | "carbot";

type CSVRow = {
  question: string;
  expectedResponse: string;
  actualResponse?: string;
  chunks?: any[];
};

type Props = {
  open: boolean;
  onClose: () => void;
  ragActivo: RagType;
};

export default function PruebasAutomaticasModal({
  open,
  onClose,
  ragActivo,
}: Props) {
  const [rows, setRows] = useState<CSVRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  /* DASHBOARD */
  const [showDashboard, setShowDashboard] = useState(false);
  const [dashboardData, setDashboardData] = useState<any | null>(null);
  const [dashboardLoading, setDashboardLoading] = useState(false);

  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
  const sessionIdRef = useRef<string>(crypto.randomUUID());

  /* ===================== LOAD CSV BASE ===================== */
  const loadCSVBase = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${BACKEND_URL}/csv/get/${ragActivo}`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      setRows(data.rows);
    } catch {
      setError("Error al cargar el CSV del RAG seleccionado");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!open) return;
    loadCSVBase();
  }, [open, ragActivo]);

  if (!open) return null;

  /* ===================== SAVE CSV BASE ===================== */
  const persistCSV = async (updatedRows: CSVRow[]) => {
    try {
      await fetch(`${BACKEND_URL}/csv/save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ragActivo,
          rows: updatedRows,
        }),
      });
    } catch {}
  };

  /* ===================== INICIAR NUEVA PRUEBA ===================== */
  const iniciarNuevaPrueba = async () => {
    if (isRunning) return;

    try {
      // 1️⃣ Guardar versión (CSV + JSON en backend)
      await fetch(`${BACKEND_URL}/csv/guardar-version`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ragActivo }),
      });

      // 2️⃣ Recargar CSV base limpio
      await loadCSVBase();
    } catch {
      alert("No se pudo iniciar una nueva prueba");
    }
  };

  /* ===================== RUN / CONTINUAR ===================== */
  const runAutomaticTests = async () => {
    if (isRunning) return;

    sessionIdRef.current = crypto.randomUUID();
    setIsRunning(true);

    for (let i = 0; i < rows.length; i++) {
      // ✅ SOLO PREGUNTAS SIN RESPUESTA
      if (rows[i].actualResponse?.trim()) continue;

      let fullResponse = "";
      let retrievedChunks: any[] = [];

      const res = await fetch(
        `${BACKEND_URL}/chat2/${sessionIdRef.current}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            query: rows[i].question,
            rag: ragActivo,
          }),
        }
      );

      if (!res.body) continue;

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value);
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";

        for (const part of parts) {
          if (!part.startsWith("data:")) continue;
          try {
            const e = JSON.parse(part.replace("data: ", ""));
            if (e.type === "chunks") retrievedChunks = e.chunks;
            if (e.type === "token") fullResponse += e.token;
          } catch {}
        }
      }

      setRows(prev => {
        const updated = [...prev];
        updated[i] = {
          ...updated[i],
          actualResponse: fullResponse.trim(),
          chunks: retrievedChunks,
        };
        persistCSV(updated);
        return updated;
      });
    }

    setIsRunning(false);
  };

  /* ===================== PROGRESS ===================== */
  const total = rows.length;
  const answered = rows.filter(
    r => r.actualResponse && r.actualResponse.trim() !== ""
  ).length;
  const percent = total > 0 ? Math.round((answered / total) * 100) : 0;
  const dashboardReady = total > 0 && answered === total;

  /* ===================== LOAD DASHBOARD ===================== */
  const loadDashboard = async () => {
    setDashboardLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/ragas/dashboard/${ragActivo}`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      setDashboardData(data);
      setShowDashboard(true);
    } catch {
      alert("No se pudo cargar el dashboard RAGAS");
    } finally {
      setDashboardLoading(false);
    }
  };

  /* ===================== UI ===================== */
  return (
    <>
      <div className="fixed inset-0 z-40 bg-black/50 flex justify-center items-center">
        <div className="bg-white w-[90%] h-[90%] rounded-xl flex flex-col">

          {/* HEADER */}
          <div className="px-6 py-4 border-b">
            <div className="flex justify-between items-center">
              <h2 className="font-semibold">
                Pruebas Automáticas –{" "}
                {ragActivo === "actividadpro" ? "Actividad Pro" : "CarBot"} (
                {answered}/{total})
              </h2>
              <button onClick={onClose}>✕</button>
            </div>
          </div>

          {/* BODY */}
          <div className="flex-1 p-6 overflow-auto text-sm">
            {loading && <p>Cargando…</p>}
            {error && <p className="text-red-500">{error}</p>}

            {rows.map((row, i) => (
              <div key={i} className="border-b py-3">
                <div><b>Pregunta:</b> {row.question}</div>
                <div className="text-xs text-gray-500">
                  Expected: {row.expectedResponse}
                </div>
                <div className="text-xs text-gray-500">
                  Actual: {row.actualResponse || "Pendiente"}
                </div>
              </div>
            ))}
          </div>

          {/* FOOTER */}
          <div className="border-t px-6 py-4 flex justify-between items-center">
            <button
              disabled={isRunning}
              onClick={runAutomaticTests}
              className="bg-[#003A8F] text-white px-4 py-2 rounded disabled:opacity-60"
            >
              {isRunning ? "Ejecutando..." : "Ejecutar prueba"}
            </button>

            <button
              disabled={isRunning}
              onClick={iniciarNuevaPrueba}
              className="bg-gray-700 text-white px-4 py-2 rounded disabled:opacity-60"
            >
              Iniciar nueva prueba
            </button>

            <button
              disabled={!dashboardReady || dashboardLoading}
              onClick={loadDashboard}
              className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {dashboardLoading ? "Cargando..." : "Ver Dashboard"}
            </button>
          </div>
        </div>
      </div>

      {/* DASHBOARD */}
      {showDashboard && dashboardData && (
        <div className="fixed inset-0 z-50 bg-black/60 flex justify-center items-center">
          <div className="bg-white w-[80%] h-[80%] rounded-xl p-6 overflow-auto">
            {/* igual que antes */}
          </div>
        </div>
      )}
    </>
  );
}
``