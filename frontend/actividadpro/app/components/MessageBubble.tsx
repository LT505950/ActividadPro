import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
type Props = {
  role: "user" | "bot"
  text: string
  image?: string
}

export default function MessageBubble({ role, text, image }: Props) {
  const isUser = role === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      
      <div
        className={`max-w-md px-4 py-3 rounded-2xl text-sm shadow-sm space-y-2 ${
          isUser
            ? "bg-blue-900 text-white"
            : "bg-white border border-gray-200 text-gray-700"
        }`}
      >
        {/* Imagen */}
        {image && (
          <img
            src={image}
            alt="uploaded"
            className="rounded-lg max-h-60 w-auto"
          />
        )}

        {/* Texto */}
        
        { text && (
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {text}
            </ReactMarkdown>
          </div>
        )}

      </div>

    </div>
  )
}