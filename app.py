import streamlit as st
from agent import run_agent  # <--- HIER HOLLEN WIR UNS DEN MOTOR AUS AGENT.PY!

st.set_page_config(page_title="Lokale KI-Suchmaschine", page_icon="🔍")

st.title("🔍 Self-Correcting KI-Suchmaschine")
st.markdown("Ein lokaler Agent, der Halluzinationen durch iterative Suche und harte Guardrails verhindert.")

# Eingabefeld
nutzer_frage = st.text_input("Stelle deine Frage:", placeholder="z.B. Wer hat den Turing Award 2023 gewonnen?")

# Wenn der Button geklickt wird:
if st.button("🚀 Suche starten"):
    if nutzer_frage.strip():
        # Der Spinner zeigt dem Nutzer, dass gearbeitet wird
        with st.spinner("Der Agent recherchiert und prüft die Quellen... (dauert ca. 10-20 Sek.)"):
            
            # HIER RUFEN WIR DIE FUNKTION AUS AGENT.PY AUF!
            ergebnis = run_agent(nutzer_frage)
            
        # Ergebnis anzeigen
        st.success("Recherche abgeschlossen!")
        st.markdown(ergebnis)
    else:
        st.warning("Bitte gib zuerst eine Frage ein.")
