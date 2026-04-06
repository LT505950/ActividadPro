"use client"
import { useState } from "react"
import MessageBubble from "./MessageBubble"

type Message = {
  role: "user" | "bot"
  text: string
  image?: string
  responseTime?: number
}

type Chunk = {
  text: string
  source: string
}

type TokensInfo = {
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
}

type Props = {
  onChunks: (chunks: Chunk[]) => void
  onTokensInfo?: (info: TokensInfo) => void
}

export default function Chat({ onChunks, onTokensInfo }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", text: "Hola, ¿en qué puedo ayudarte?" }
  ])
  const [input, setInput] = useState("")
  const [image, setImage] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async () => {
    if (input.trim() === "" && !image) return

    const userMsg = input.trim() || (image ? "Te proporciono la descripción del error" : "")
    const currentImage = image
    const imagePreview = currentImage ? URL.createObjectURL(currentImage) : undefined

    setImage(null)
    setInput("")
    const fileInput = document.getElementById("fileInput") as HTMLInputElement
    if (fileInput) fileInput.value = ""

    setMessages(prev => [
      ...prev,
      { role: "user", text: userMsg || "", image: imagePreview },
      { role: "bot", text: "" }
    ])
    setIsLoading(true)

    const startTime = Date.now()

    try {
      let res: Response

      if (currentImage) {
        const formData = new FormData()
        formData.append("query", userMsg || "")
        formData.append("file", currentImage)
        res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          body: formData
        })
      } else {
        res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: userMsg })
        })
      }

      const reader = res.body?.getReader()
      const decoder = new TextDecoder()
      if (!reader) throw new Error("No stream disponible")

      // Buffer para manejar eventos SSE que llegan partidos entre chunks de red
      let buffer = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })

        // Los eventos SSE se separan por doble salto de linea
        const parts = buffer.split("\n\n")
        // El ultimo fragmento puede estar incompleto, lo guardamos en buffer
        buffer = parts.pop() ?? ""

        for (const part of parts) {
          const lines = part.split("\n").filter(l => l.startsWith("data: "))

          for (const line of lines) {
            const jsonStr = line.replace("data: ", "").trim()
            if (!jsonStr) continue

            let event: any
            try {
              event = JSON.parse(jsonStr)
            } catch {
              // Saltar lineas malformadas sin romper el stream
              continue
            }

            if (event.type === "chunks") {
              onChunks(event.chunks || [])
            }

            if (event.type === "token") {
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  role: "bot",
                  text: updated[updated.length - 1].text + event.token
                }
                return updated
              })
            }

            if (event.type === "tokens_info") {
              onTokensInfo?.({
                prompt_tokens: event.prompt_tokens,
                completion_tokens: event.completion_tokens,
                total_tokens: event.total_tokens
              })
            }
          }
        }
      }

      const endTime = Date.now()
      const responseTime = endTime - startTime

      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          responseTime
        }
        return updated
      })

    } catch (error) {
      console.error("Stream error:", error)
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          role: "bot",
          text: "Error al conectar con el servidor."
        }
        return updated
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !isLoading) handleSend()
  }

  const handleSelectFile = () => {
    document.getElementById("fileInput")?.click()
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    validateAndSetImage(file)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    validateAndSetImage(file)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const validateAndSetImage = (file?: File) => {
    if (!file) return
    if (!["image/jpeg", "image/png"].includes(file.type)) {
      alert("Solo se permiten imágenes JPG o PNG")
      return
    }
    setImage(file)
  }

  return (
    <div
      className="flex flex-col h-full bg-gray-50 rounded-xl"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {/* Mensajes */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 max-h-full">
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            role={msg.role}
            text={msg.text}
            image={msg.image}
            responseTime={msg.responseTime}
          />
        ))}
      </div>

      {/* Preview nombre imagen */}
      {image && (
        <div className="px-4 pb-2 flex items-center gap-2 text-sm text-gray-600">
          📷 {image.name}
          <button
            onClick={() => setImage(null)}
            className="text-red-500 hover:underline text-xs"
          >
            ❌ Quitar
          </button>
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-gray-200 bg-white flex gap-2 items-center">
        <button
          onClick={handleSelectFile}
          disabled={isLoading}
          className={`text-xl px-2 hover:opacity-70 ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
          title="Adjuntar imagen"
        >
          📎
        </button>
        <input
          id="fileInput"
          type="file"
          accept="image/png, image/jpeg"
          onChange={handleImageChange}
          className="hidden"
        />
        <input
          type="text"
          placeholder="Escribe tu consulta o arrastra una imagen..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isLoading}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          onClick={handleSend}
          disabled={isLoading}
          className={`bg-yellow-400 text-blue-900 px-4 py-2 rounded-lg text-sm font-medium hover:bg-yellow-300 ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
        >
          {isLoading ? "Escribiendo..." : "Enviar"}
        </button>
      </div>
    </div>
  )
}
