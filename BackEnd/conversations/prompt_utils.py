def build_prompt_from_history(conversation):
    """
    Construye el prompt usando el historial completo de la conversación.
    """
    history = ""

    for turn in conversation.turns:
        role = "Usuario" if turn["role"] == "user" else "Asistente"
        history += f"{role}: {turn['content']}\n"

    return history.strip()
