"use client";
import { useEffect, useState } from "react";

type RagType = "actividadpro" | "carbot";

type CSVRow = {
  question: string;
  expectedResponse: string;
  testMethodType: string;
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

/* ===================== RAG → CSV MAP ===================== */
const RAG_CSV_PATH: Record<RagType, string> = {
  actividadpro: "/evaluar_helpdesk.csv",
  carbot: "/evaluar_carbot.csv",
};

export default function PruebasAutomaticasModal({
  open,
  onClose,
  ragActivo,
}: Props) {
  const [mode, setMode] = useState<"list" | "new">("list");
  const [rows, setRows] = useState<CSVRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});

  /* ===================== AUTO LOAD CSV ===================== */
  useEffect(() => {
    if (!open) return;

    // ✅ Forzar modo new al abrir
    if (mode !== "new") {
      setMode("new");
      return;
    }

    const path = RAG_CSV_PATH[ragActivo];
    setLoading(true);
    setError(null);

    fetch(path)
      .then(res => {
        if (!res.ok) throw new Error();
        return res.text();
      })
      .then(text => parseCSV(text))
      .catch(() =>
        setError("Error al cargar el CSV del RAG seleccionado")
      )
      .finally(() => setLoading(false));
  }, [open, mode, ragActivo]);


  // ✅ AHORA SÍ
  if (!open) return null;



  /* ===================== PARSE CSV ===================== */
  const parseCSV = (csvText: string) => {
    const cleanText = csvText.replace(/\r/g, "");

    const lines = cleanText
      .split("\n")
      .map(l => l.trim())
      .filter(Boolean);

    if (lines.length < 2) {
      setError("El CSV no contiene datos");
      return;
    }

    let separator = ",";
    if (lines[0].includes("\t")) separator = "\t";
    else if (lines[0].includes(";")) separator = ";";

    const headers = parseCSVLine(lines[0], separator).map(h =>
      h.replace(/\uFEFF/g, "").toLowerCase()
    );

    const questionIndex = headers.indexOf("question");
    const expectedResponseIndex = headers.indexOf("expectedresponse");
    const testMethodTypeIndex = headers.indexOf("testmethodtype");

    if (
      questionIndex === -1 ||
      expectedResponseIndex === -1 ||
      testMethodTypeIndex === -1
    ) {
      setError(
        "El CSV debe contener: question, expectedResponse, testMethodType"
      );
      return;
    }

    const data: CSVRow[] = lines.slice(1).map(line => {
      const columns = parseCSVLine(line, separator);

      return {
        question: columns[questionIndex] || "",
        expectedResponse: columns[expectedResponseIndex] || "",
        testMethodType: columns[testMethodTypeIndex] || "",
      };
    });

    const validRows = data.filter(
      r => r.question && r.expectedResponse && r.testMethodType
    );

    if (!validRows.length) {
      setError("No se encontraron filas válidas");
      return;
    }

    setRows(validRows);
  };

  const resetNewTest = () => {
    setRows([]);
    setError(null);
    setExpanded({});
  };

  const toggleExpand = (i: number) =>
    setExpanded(p => ({ ...p, [i]: !p[i] }));

  /* ===================== UI ===================== */
  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex justify-center items-center">
      <div className="bg-white w-[90%] h-[90%] rounded-xl flex flex-col">

        <div className="px-6 py-4 border-b flex justify-between">
          <h2 className="font-semibold">
            Pruebas Automáticas –{" "}
            {ragActivo === "actividadpro" ? "Actividad Pro" : "CarBot"}
          </h2>
          <button onClick={onClose}>✕</button>
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
                    {expandedRow
                      ? row.question
                      : row.question.slice(0, 120)}
                    {row.question.length > 120 && (
                      <button
                        className="text-xs text-blue-500 ml-2"
                        onClick={() => toggleExpand(i)}
                      >
                        {expandedRow ? "Ver menos" : "Ver más"}
                      </button>
                    )}
                  </div>
                  <div className="text-xs text-gray-500">
                    Expected: {row.expectedResponse}
                  </div>
                  <div className="text-xs text-gray-500">
                    Método: {row.testMethodType}
                  </div>
                </div>
              );
            })}
        </div>

        <div className="border-t px-6 py-4 flex justify-between">

          <button className="bg-[#003A8F] text-white px-4 py-2 rounded">
            Ejecutar prueba
          </button>
        </div>
      </div>
    </div>
  );
}