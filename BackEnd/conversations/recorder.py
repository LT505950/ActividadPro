from rag.pipeline import run_rag_stream
from conversations.conversation import Conversation
from conversations.prompt_utils import build_prompt_from_history

def handle_user_message(conversation: Conversation, query: str) -> Conversation:
    # ⛔ si ya terminó, no seguir
    if conversation.conversation_complete:
        return conversation

    conversation.add_user_turn(query)

    try:
        prompt = build_prompt_from_history(conversation)

        chunks, stream = run_rag_stream(prompt)

        answer = ""
        tokens_info = {}

        for event in stream:
            if event["type"] == "token":
                answer += event["value"]
            elif event["type"] == "tokens_info":
                tokens_info = event

        metadata = {
            "llm_model": "gemma4:e2b",
            "tokens_in": tokens_info.get("prompt_tokens", 0),
            "tokens_out": tokens_info.get("completion_tokens", 0),
            "chunks_used": len(chunks),
            "retrieval_scores": [c.get("score") for c in chunks]
        }

        conversation.add_turn("assistant", answer, metadata)

        # ✅ Corte por límite
        if conversation.reached_max_turns():
            conversation.conversation_complete = True
            conversation.completion_reason = "max_turns"

    except Exception:
        conversation.conversation_complete = True
        conversation.completion_reason = "error"

    return conversation