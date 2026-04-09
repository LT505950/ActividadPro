"use client";
import { useState } from "react";

type CSVRow = {
  question: string;
  expectedResponse: string;
  testMethodType: string;
};

type Props = {
  open: boolean;
  onClose: () => void;
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

export default function PruebasAutomaticasModal({ open, onClose }: Props) {
  const [mode, setMode] = useState<"list" | "new">("list");
  const [rows, setRows] = useState<CSVRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});

  if (!open) return null;

  /* ===================== FILE HANDLING ===================== */

  const handleFile = (file: File) => {
    if (!file.name.toLowerCase().endsWith(".csv")) {
      setError("Solo se permiten archivos CSV");
      return;
    }

    setError(null);
    setLoading(true);
    setFileName(file.name);

    const reader = new FileReader();

    reader.onload = e => {
      const text = e.target?.result;
      if (!text) {
        setError("El archivo está vacío");
        setLoading(false);
        return;
      }
      parseCSV(text as string);
      setLoading(false);
    };

    reader.onerror = () => {
      setError("No se pudo leer el archivo");
      setLoading(false);
    };

    reader.readAsText(file);
  };

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
        "El CSV debe contener las columnas: question, expectedResponse, testMethodType"
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

    if (validRows.length === 0) {
      setError("No se encontraron filas válidas en el CSV");
      return;
    }

    setRows(validRows);
  };

  const removeRow = (index: number) => {
    setRows(prev => prev.filter((_, i) => i !== index));
  };

  const toggleExpand = (index: number) => {
    setExpanded(prev => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const resetNewTest = () => {
    setRows([]);
    setError(null);
    setFileName(null);
    setExpanded({});
    setLoading(false);
  };

  /* ===================== UI ===================== */

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-[90%] h-[90%] bg-white rounded-xl shadow-lg flex flex-col">

        {/* HEADER */}
        <div className="flex items-center justify-between px-6 py-4 border-b">
          <h2 className="text-lg font-semibold text-[#003A8F]">
            Pruebas Automáticas
          </h2>
          <button onClick={onClose} className="text-xl text-gray-500">✕</button>
        </div>

        {/* BODY */}
        <div className="flex-1 p-6 overflow-auto">

          {mode === "list" && (
            <div className="border border-dashed rounded-lg p-6 text-center text-gray-400">
              Aún no existen evaluaciones registradas
            </div>
          )}

          {mode === "new" && rows.length === 0 && (
            <div
              className={`h-64 border-2 border-dashed rounded-xl flex items-center justify-center
                ${dragOver ? "bg-yellow-50 border-yellow-400" : "border-gray-300"}
              `}
              onDragOver={e => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={e => {
                e.preventDefault();
                setDragOver(false);
                const file = e.dataTransfer.files?.[0];
                if (file) handleFile(file);
              }}
            >
              <input
                type="file"
                accept=".csv"
                id="csvInput"
                className="hidden"
                onChange={e => {
                  const file = e.target.files?.[0];
                  if (file) handleFile(file);
                }}
              />
              <label htmlFor="csvInput" className="cursor-pointer text-blue-600">
                Seleccionar archivo CSV
              </label>
              {error && <p className="text-red-500 text-xs mt-2">{error}</p>}
            </div>
          )}

          {mode === "new" && rows.length > 0 && (
            <div className="border rounded-lg divide-y">
              {rows.map((row, i) => {
                const expandedRow = expanded[i];
                return (
                  <div key={i} className="p-4 space-y-1 text-sm">
                    <div>
                      {expandedRow ? row.question : row.question.slice(0, 120)}
                      {row.question.length > 120 && (
                        <button
                          className="ml-2 text-blue-500 text-xs"
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
                    <button
                      className="text-red-500 text-xs"
                      onClick={() => removeRow(i)}
                    >
                      Eliminar
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* FOOTER */}
        <div className="border-t px-6 py-4 flex justify-between">
          {mode === "new" && (
            <button onClick={() => { setMode("list"); resetNewTest(); }}>
              ← Volver
            </button>
          )}

          <button
            onClick={() => setMode(mode === "list" ? "new" : "list")}
            className="bg-yellow-400 text-blue-900 px-4 py-2 rounded"
          >
            {mode === "list"
              ? "Iniciar nueva prueba"
              : "Ejecutar prueba"}
          </button>
        </div>

      </div>
    </div>
  );
}