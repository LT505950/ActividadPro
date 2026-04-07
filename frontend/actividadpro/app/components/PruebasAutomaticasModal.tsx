"use client";
import { useState } from "react";

type CSVRow = {
  question: string;
};

type Props = {
  open: boolean;
  onClose: () => void;
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

    reader.onload = (e) => {
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

    const headers = lines[0]
      .split(separator)
      .map(h => h.replace(/\uFEFF/g, "").trim().toLowerCase());

    const questionIndex = headers.findIndex(h =>
      h === "question" || h.includes("question")
    );

    if (questionIndex === -1) {
      setError("El CSV no contiene la columna 'question'");
      return;
    }

    const data: CSVRow[] = lines.slice(1).map(line => {
      const columns = line.split(separator);
      const question = columns[questionIndex]?.trim() || "";
      return { question };
    });

    const validRows = data.filter(r => r.question.length > 0);

    if (validRows.length === 0) {
      setError("No se encontraron preguntas en el CSV");
      return;
    }

    setRows(validRows);
  };

  const removeQuestion = (index: number) => {
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
          <button onClick={onClose} className="text-xl text-gray-500">
            ✕
          </button>
        </div>

        {/* BODY */}
        <div className="flex-1 p-6 overflow-auto">

          {/* LISTADO */}
          {mode === "list" && (
            <>
              <div className="text-sm text-gray-600 mb-4">
                Evaluaciones anteriores
              </div>

              <div className="border border-dashed rounded-lg p-6 text-center text-gray-400 text-sm">
                Aún no existen evaluaciones registradas
              </div>
            </>
          )}

          {/* DROPZONE */}
          {mode === "new" && rows.length === 0 && (
            <div className="w-full flex justify-center items-center h-full">
              <div
                className={`w-full max-w-xl h-64 border-2 border-dashed rounded-xl flex flex-col items-center justify-center text-sm transition
                  ${dragOver ? "border-yellow-400 bg-yellow-50" : "border-gray-300"}
                `}
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragOver(true);
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
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
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) {
                      handleFile(file);
                      e.target.value = "";
                    }
                  }}
                />

                {!loading ? (
                  <>
                    <p className="text-gray-600 mb-2">
                      Arrastra tu archivo CSV aquí
                    </p>
                    <p className="text-gray-400 mb-4">o</p>
                    <label
                      htmlFor="csvInput"
                      className="cursor-pointer bg-yellow-400 text-blue-900 px-4 py-2 rounded-lg font-medium hover:bg-yellow-300"
                    >
                      Seleccionar archivo
                    </label>
                  </>
                ) : (
                  <p className="text-gray-600">Cargando archivo...</p>
                )}

                {fileName && (
                  <p className="mt-4 text-xs text-gray-500">
                    Archivo: {fileName}
                  </p>
                )}

                {error && (
                  <p className="mt-2 text-red-600 text-xs">
                    {error}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* PREGUNTAS */}
          {mode === "new" && rows.length > 0 && (
            <>
              <div className="text-sm text-gray-600 mb-4">
                Preguntas a evaluar ({rows.length})
              </div>

              <div className="border rounded-lg divide-y">
                {rows.map((row, index) => {
                  const isExpanded = expanded[index];
                  const shouldTruncate = row.question.length > 100;
                  const text =
                    !shouldTruncate || isExpanded
                      ? row.question
                      : row.question.slice(0, 100) + "...";

                  return (
                    <div
                      key={index}
                      className="flex items-start justify-between px-4 py-3 text-sm gap-4"
                    >
                      <div className="flex-1 text-gray-800 whitespace-pre-line">
                        {text}
                        {shouldTruncate && (
                          <button
                            onClick={() => toggleExpand(index)}
                            className="ml-2 text-blue-600 text-xs hover:underline"
                          >
                            {isExpanded ? "Ver menos" : "Ver más"}
                          </button>
                        )}
                      </div>

                      <button
                        onClick={() => removeQuestion(index)}
                        className="text-red-500 hover:underline text-xs shrink-0"
                      >
                        Eliminar
                      </button>
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </div>

        {/* FOOTER */}
        <div className="border-t px-6 py-4 flex justify-between">
          {mode === "new" && (
            <button
              onClick={() => {
                setMode("list");
                resetNewTest();
              }}
              className="text-sm text-gray-500 hover:underline"
            >
              ← Volver
            </button>
          )}

          <div className="ml-auto">
            {mode === "list" ? (
              <button
                onClick={() => setMode("new")}
                className="bg-yellow-400 text-blue-900 px-4 py-2 rounded-lg text-sm font-medium hover:bg-yellow-300"
              >
                Iniciar nueva prueba automática
              </button>
            ) : (
              <button
                disabled={rows.length === 0}
                className="bg-[#003A8F] text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-50"
              >
                Ejecutar prueba
              </button>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}