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

export default function Home() {
  const [chunks, setChunks] = useState<Chunk[]>([]) // 🔥 estado global de chunks
  const [tokensInfo, setTokensInfo] = useState<TokensInfo | undefined>(undefined)

  return (
    <div className="flex h-screen w-full bg-[#f5f7fb]">
      <Sidebar />

      <div className="flex flex-col flex-1">
        <Header />

        <div className="flex flex-1 overflow-hidden">
          
          {/* Chat */}
          <div className="flex-1 p-4 overflow-hidden">
            <Chat onChunks={setChunks} onTokensInfo={setTokensInfo} />
          </div>

          {/* Right Panel */}
          <RightPanel chunks={chunks} tokensInfo={tokensInfo} />
          
        </div>
      </div>
    </div>
  )
}