"use client";
import { useEffect, useRef, useState } from "react";

type RagType = "actividadpro" | "carbot";

type CSVRow = {
  question: string;
  expectedResponse: string;
  testMethodType: string;
  respuestaGenerada?: string;
  chunks?: any[]; // ✅ NECESARIO PARA RAGAS
};

type Props = {
  open: boolean;
  onClose: () => void;
  ragActivo: RagType;
};

/* ===================== CSV UTIL ===================== */
const parseCSVLine = (line: string, separator: string): string[] => {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      inQuotes = !inQuotes;
      continue;
    }

    if (char === separator && !inQuotes) {
      result.push(current.trim());
      current = "";
      continue;
    }

    current += char;
  }

  result.push(current.trim());
  return result;
};

export default function PruebasAutomaticasModal({
  open,
  onClose,
  ragActivo,
}: Props) {
  const [rows, setRows] = useState<CSVRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});
  const [isRunning, setIsRunning] = useState(false);

  const sessionIdRef = useRef<string>(crypto.randomUUID());
  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

  /* ===================== LOAD CSV ===================== */
  useEffect(() => {
    if (!open) return;

    setLoading(true);
    setError(null);

    fetch(`${BACKEND_URL}/csv/get/${ragActivo}`)
      .then(res => {
        if (!res.ok) throw new Error();
        return res.text();
      })
      .then(parseCSV)
      .catch(() => setError("Error al cargar el CSV del RAG seleccionado"))
      .finally(() => setLoading(false));
  }, [open, ragActivo]);

  if (!open) return null;

  /* ===================== PARSE CSV ===================== */
  const parseCSV = (csvText: string) => {
    const cleanText = csvText.replace(/\r/g, "");
    const rawLines = cleanText.split("\n");

    const rowsCombined: string[] = [];
    let buffer = "";
    let quoteCount = 0;

    for (const line of rawLines) {
      buffer += (buffer ? "\n" : "") + line;
      quoteCount += (line.match(/"/g) || []).length;

      if (quoteCount % 2 === 0) {
        if (buffer.trim()) rowsCombined.push(buffer.trim());
        buffer = "";
        quoteCount = 0;
      }
    }

    if (rowsCombined.length < 2) {
      setError("El CSV no contiene datos");
      return;
    }

    let separator = ",";
    if (rowsCombined[0].includes("\t")) separator = "\t";
    else if (rowsCombined[0].includes(";")) separator = ";";

    const headers = parseCSVLine(rowsCombined[0], separator).map(h =>
      h.replace(/\uFEFF/g, "").toLowerCase()
    );

    const qi = headers.indexOf("question");
    const eri = headers.indexOf("expectedresponse");
    const tmi = headers.indexOf("testmethodtype");
    const rgi = headers.indexOf("respuestagenerada");

    if (qi === -1 || eri === -1 || tmi === -1) {
      setError("El CSV debe contener question, expectedResponse, testMethodType");
      return;
    }

    const data: CSVRow[] = rowsCombined.slice(1).map(line => {
      const cols = parseCSVLine(line, separator);
      return {
        question: cols[qi] || "",
        expectedResponse: cols[eri] || "",
        testMethodType: cols[tmi] || "",
        respuestaGenerada: cols[rgi] || "",
      };
    });

    setRows(data);
  };

  const toggleExpand = (i: number) =>
  setExpanded(prev => ({ ...prev, [i]: !prev[i] }));

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

  /* ===================== RUN TESTS ===================== */
  const runAutomaticTests = async () => {
    if (isRunning) return;
    setIsRunning(true);

    for (let i = 0; i < rows.length; i++) {
      if (rows[i].respuestaGenerada?.trim()) continue;

      let fullResponse = "";
      let retrievedChunks: any[] = []; // ✅ AQUÍ

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

            if (e.type === "chunks") {
              retrievedChunks = e.chunks; // ✅ CAPTURA CHUNKS
            }

            if (e.type === "token") {
              fullResponse += e.token;
            }
          } catch {}
        }
      }

      setRows(prev => {
        const updated = [...prev];
        updated[i] = {
          ...updated[i],
          respuestaGenerada: fullResponse.trim(),
          chunks: retrievedChunks, // ✅ SE GUARDAN
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
    r => r.respuestaGenerada && r.respuestaGenerada.trim() !== ""
  ).length;
  const percent = total ? Math.round((answered / total) * 100) : 0;

  /* ===================== UI ===================== */
  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex justify-center items-center">
      <div className="bg-white w-[90%] h-[90%] rounded-xl flex flex-col">

        <div className="px-6 py-4 border-b">
          <div className="flex justify-between items-center">
            <h2 className="font-semibold">
              Pruebas Automáticas –{" "}
              {ragActivo === "actividadpro" ? "Actividad Pro" : "CarBot"} (
              {answered}/{total})
            </h2>

            <div className="flex items-center gap-4">
              <div className="w-32">
                <div className="text-xs text-gray-500 text-right mb-1">
                  Progreso {percent}%
                </div>
                <div className="bg-gray-200 h-3 rounded">
                  <div
                    className="bg-[#003A8F] h-3 rounded"
                    style={{ width: `${percent}%` }}
                  />
                </div>
              </div>

              <button onClick={onClose}>✕</button>
            </div>
          </div>
        </div>

        <div className="flex-1 p-6 overflow-auto">
          {loading && <p>Cargando casos...</p>}
          {error && <p className="text-red-500 text-sm">{error}</p>}

          {!loading &&
            rows.map((row, i) => {
              const expandedRow = expanded[i];
              return (
                <div key={i} className="border-b py-3 text-sm">
                  <div>
                    <b>Pregunta:</b> {row.question}
                  </div>
                  <div className="text-xs text-gray-500">
                    Expected: {row.expectedResponse}
                  </div>

                  <div className="text-xs text-gray-500">
                    Método: {row.testMethodType}
                  </div>

                  <div className="text-xs text-gray-500">
                    Respuesta generada:{" "}
                    {row.respuestaGenerada?.trim() || "Sin respuesta"}
                  </div>
                </div>
              );
            })}
        </div>

        <div className="border-t px-6 py-4 flex justify-end">
          <button
            disabled={isRunning}
            onClick={runAutomaticTests}
            className="bg-[#003A8F] text-white px-4 py-2 rounded disabled:opacity-60"
          >
            {isRunning ? "Ejecutando..." : "Ejecutar prueba"}
          </button>
        </div>
      </div>
    </div>
  );
}