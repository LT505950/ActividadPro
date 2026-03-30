"use client"

import { useState } from "react"
import Sidebar from "../components/Sidebar"
import Chat from "../components/Chat"
import RightPanel from "../components/RightPanel"
import Header from "../components/Header"

type Chunk = {
  text: string
  source: string
}

export default function Home() {
  const [chunks, setChunks] = useState<Chunk[]>([]) // 🔥 estado global de chunks

  return (
    <div className="flex h-screen w-full bg-[#f5f7fb]">
      <Sidebar />

      <div className="flex flex-col flex-1">
        <Header />

        <div className="flex flex-1 overflow-hidden">
          
          {/* Chat */}
          <div className="flex-1 p-4 overflow-hidden">
            <Chat onChunks={setChunks} />
          </div>

          {/* Right Panel */}
          <RightPanel chunks={chunks} />
          
        </div>
      </div>
    </div>
  )
}