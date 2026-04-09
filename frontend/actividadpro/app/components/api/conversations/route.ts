import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET() {
  const dirPath = path.join(process.cwd(), "test", "conversations");
  const files = fs
    .readdirSync(dirPath)
    .filter((f) => f.endsWith(".json"));

  const conversations = files.map((file) => {
    const filePath = path.join(dirPath, file);
    const content = JSON.parse(fs.readFileSync(filePath, "utf-8"));
    return content;
  });

  return NextResponse.json(conversations);
}