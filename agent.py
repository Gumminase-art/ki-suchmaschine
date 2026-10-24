import requests
from duckduckgo_search import DDGS

def suche_nach(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    if not results:
        return "Keine Ergebnisse gefunden."
    return "\n".join([f"- {r['title']}: {r['body']}" for r in results])

def frage_ki(kontext, frage):
    prompt = f"""Du bist ein präziser, faktenbasierter Such-Assistent. 
    
    AUFGABE: Beantworte die Frage kurz und direkt, indem du die Informationen aus den Suchergebnissen zusammenfasst.
    
    REGELN:
    1. Wenn die Suchergebnisse ausreichend Informationen enthalten, antworte nur mit der faktenbasierten Antwort.
    2. Wenn die Ergebnisse widersprüchlich, vage oder irrelevant sind, antworte EXAKT mit: 
       "NEUE_SUCHE: [ein besserer, spezifischerer Suchbegriff]"
    3. Erfinde NIEMALS Fakten.

    Frage: {frage}
    Suchergebnisse:
    {kontext}
    """
    
    url = "http://localhost:11434/api/generate"
    data = {"model": "qwen2.5:3b", "prompt": prompt, "stream": False}
    response = requests.post(url, json=data)
    return response.json()["response"]

# --- DIESE FUNKTION WIRD VON APP.PY AUFGERUFEN ---
def run_agent(nutzer_frage):
    aktueller_query = nutzer_frage
    max_versuche = 3
    protokoll = [] # Hier speichern wir die Schritte für die UI
    
    for versuch in range(1, max_versuche + 1):
        protokoll.append(f"🔄 **Versuch {versuch}**: Suche nach '{aktueller_query}'...")
        ergebnisse = suche_nach(aktueller_query)
        antwort = frage_ki(ergebnisse, nutzer_frage)
        
        if "NEUE_SUCHE:" in antwort:
            aktueller_query = antwort.split("NEUE_SUCHE:")[1].strip()
            protokoll.append(f"⚠️ Nicht eindeutig. Agent optimiert Suche zu: *'{aktueller_query}'*")
        else:
            protokoll.append("✅ **Antwort in den Quellen verifiziert!**")
            # Wir geben das Protokoll und die finale Antwort zurück
            return "\n\n".join(protokoll) + f"\n\n---\n💡 **Endergebnis:**\n{antwort.strip()}"
    
    # Wenn die Schleife 3x durchläuft, ohne 'break':
    protokoll.append("❌ **EISERNE REGEL AKTIVIERT:** Nach 3 Versuchen konnte keine verifizierbare Quelle gefunden werden. Der Agent verweigert eine Antwort, um Halluzinationen zu vermeiden.")
    return "\n\n".join(protokoll)
