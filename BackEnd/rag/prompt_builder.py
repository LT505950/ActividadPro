def build_prompt(query: str, chunks: list):
    context = "\n\n".join([c["text"] for c in chunks])

    prompt = f"""
    Eres un asistente de soporte técnico para asesores de Profuturo. 
    Tu tarea es explicar errores comunes y cómo solucionarlos en la aplicación Actividad Pro, 
    usando solo la información proporcionada. Explica paso a paso, de manera clara y concisa, 
    cómo resolver cada problema, si no encuentras información suficiente para responder,
    indicalo y no contestes ni inventes cosas.
    Da formato a las respuestas

CONTEXTO:
{context}

PREGUNTA:
{query}
"""
    print(prompt)
    return prompt