"use client"

import { useState } from "react"
import Sidebar from "./components/Sidebar"
import Chat from "./components/Chat"
import RightPanel from "./components/RightPanel"
import Header from "./components/Header"

type Chunk = {
  text: string
  source: string
}

type TokensInfo = {
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
}
export type RagType = "actividadpro" | "carbot"

export default function Home() {
  const [chunks, setChunks] = useState<Chunk[]>([])
  const [tokensInfo, setTokensInfo] = useState<TokensInfo | undefined>()
  
  // ✅ ESTADO GLOBAL DEL RAG
  const [ragActivo, setRagActivo] = useState<RagType>("actividadpro")

  return (
    <div className="flex h-screen w-full bg-[#f5f7fb]">
      <Sidebar ragActivo={ragActivo} setRagActivo={setRagActivo} />

      <div className="flex flex-col flex-1">
        <Header ragActivo={ragActivo} />

        <div className="flex flex-1 overflow-hidden">
          <div className="flex-1 p-4 overflow-hidden">
            <Chat
              ragActivo={ragActivo}
              onChunks={setChunks}
              onTokensInfo={setTokensInfo}
            />
          </div>

          <RightPanel chunks={chunks} tokensInfo={tokensInfo} />
        </div>
      </div>
    </div>
  )
}