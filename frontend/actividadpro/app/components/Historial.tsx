"use client";
import { useEffect, useState } from "react";

type Conversation = {
  test_id: string;
  created_at: string;
  turns: {
    role: string;
    content: string;
  }[];
};

export default function Historial() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [visibleCount, setVisibleCount] = useState(10);

  useEffect(() => {
    const cargarConversations = async () => {
      const res = await fetch("/test/conversations/index.json");
      const data = await res.json();
      setConversations(data);
    };

    cargarConversations();
  }, []);

  const conversacionesVisibles = conversations.slice(0, visibleCount);

  return (
    <div className="mt-4 space-y-2 text-sm">
      {conversacionesVisibles.map((conv) => (
        <div
          key={conv.test_id}
          className="cursor-pointer rounded px-2 py-1 hover:bg-neutral-200"
        >
          <div className="font-medium truncate">
            {conv.turns[0]?.content || "Conversación"}
          </div>
          <div className="text-xs text-neutral-500">
            {new Date(conv.created_at).toLocaleString()}
          </div>
        </div>
      ))}

      {visibleCount < conversations.length && (
        <button
          className="w-full rounded px-2 py-1 text-xs text-neutral-600 hover:bg-neutral-200"
          onClick={() => setVisibleCount((prev) => prev + 10)}
        >
          Mostrar más
        </button>
      )}
    </div>
  );
}
``