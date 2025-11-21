import streamlit as st
import random
from datetime import datetime

# --- CSS pour améliorer l'apparence ---
st.markdown(
    """
    <style>
    .game-title {font-size:32px; font-weight:700; margin-bottom:0.2rem;}
    .hint {color:#ff7f50; font-weight:600;}
    .attempts {background:#f6f8fa; padding:8px; border-radius:8px;}
    .btn-primary {background: linear-gradient(90deg,#ff7f50,#ffb347); color: white; border: none;}
    .small-muted {color:#6c757d; font-size:12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Initialisation session_state ---
if "nombre" not in st.session_state:
    st.session_state.nombre = random.randint(1, 100)
    st.session_state.compteur = 0
    st.session_state.message = ""
    st.session_state.tentatives = []
    st.session_state.scores = []  # liste de dicts: {'score':int,'date':str}
    st.session_state.hints_used = 0

# --- Layout: titre et description ---
st.markdown('<div class="game-title">🎲 Jeu du Nombre Mystère</div>', unsafe_allow_html=True)
st.write("Devine le nombre auquel je pense. Ajuste les paramètres dans la barre latérale pour personnaliser le défi.")

# --- Sidebar: réglages et aide ---
with st.sidebar:
    st.header("⚙️ Réglages")
    min_val = st.number_input("Min", value=1, step=1, key="min_val")
    max_val = st.number_input("Max", value=100, step=1, key="max_val")
    if min_val >= max_val:
        st.error("Min doit être inférieur à Max")
    max_attempts = st.slider("Limite de tentatives (0 = illimité)", 0, 20, 0)
    allow_hints = st.checkbox("Activer indices (coût: +1 tentative)", value=True)
    st.markdown("---")
    st.header("🏆 Classement local")
    if st.session_state.scores:
        # afficher top 5
        top = sorted(st.session_state.scores, key=lambda x: x["score"])[:5]
        for i, s in enumerate(top, 1):
            st.write(f"**{i}.** {s['score']} coups — {s['date']}")
    else:
        st.write("Aucun score pour l'instant. Sois le premier !")
    st.markdown("---")
    if st.button("Réinitialiser le classement"):
        st.session_state.scores = []
        st.success("Classement réinitialisé")

# --- Vérifier cohérence range et réinitialiser si changé ---
if st.session_state.get("game_range") != (min_val, max_val):
    st.session_state.game_range = (min_val, max_val)
    st.session_state.nombre = random.randint(min_val, max_val)
    st.session_state.compteur = 0
    st.session_state.message = ""
    st.session_state.tentatives = []
    st.session_state.hints_used = 0

# --- Colonne jeu / infos ---
col1, col2 = st.columns([2, 1])

with col1:
    # Formulaire pour éviter re-runs intempestifs
    with st.form("guess_form", clear_on_submit=False):
        guess = st.number_input(
            f"Entre un nombre ({min_val}–{max_val})",
            min_value=min_val,
            max_value=max_val,
            step=1,
            value=min_val,
            key="input_guess",
        )
        submitted = st.form_submit_button("Vérifier", help="Appuie pour soumettre ta proposition")
        st.markdown('<div class="small-muted">Appuie sur Vérifier pour valider</div>', unsafe_allow_html=True)

    # Bouton indice (optionnel)
    if allow_hints and st.button("Obtenir un indice (coûte +1 tentative)", key="hint_btn"):
        st.session_state.hints_used += 1
        st.session_state.compteur += 1
        hint_text = []
        n = st.session_state.nombre
        # indices progressifs selon nombre d'indices demandés
        if st.session_state.hints_used == 1:
            hint_text.append("Le nombre est **pair**." if n % 2 == 0 else "Le nombre est **impair**.")
        elif st.session_state.hints_used == 2:
            hint_text.append("Le nombre est divisible par 3." if n % 3 == 0 else "Le nombre n'est pas divisible par 3.")
        else:
            # indice plus précis
            span = max(1, (max_val - min_val) // 10)
            low = max(min_val, n - span)
            high = min(max_val, n + span)
            hint_text.append(f"Le nombre est entre **{low}** et **{high}**.")
        st.markdown(f"<div class='hint'>{' '.join(hint_text)}</div>", unsafe_allow_html=True)

    # Traitement de la soumission
    if submitted:
        # respect de la limite de tentatives
        if max_attempts and st.session_state.compteur >= max_attempts:
            st.warning("Tu as atteint la limite de tentatives. Rejoue pour retenter ta chance.")
        else:
            st.session_state.compteur += 1
            st.session_state.tentatives.append(int(guess))

            diff = abs(guess - st.session_state.nombre)
            # message de feedback
            if guess < st.session_state.nombre:
                st.session_state.message = "C'est plus 🔼"
            elif guess > st.session_state.nombre:
                st.session_state.message = "C'est moins 🔽"
            else:
                st.session_state.message = f"🎉 Bravo ! Tu as trouvé le nombre en {st.session_state.compteur} coups !"
                # enregistrer score
                st.session_state.scores.append({
                    "score": st.session_state.compteur,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.balloons()

    # Affichage message principal
    if st.session_state.message:
        st.info(st.session_state.message)

    # Affichage historique des tentatives
    st.markdown("**Tes tentatives**")
    if st.session_state.tentatives:
        attempts_str = "  ".join([f"`{t}`" for t in st.session_state.tentatives])
        st.markdown(f"<div class='attempts'>{attempts_str}</div>", unsafe_allow_html=True)
    else:
        st.write("_Aucune tentative pour l'instant_")

with col2:
    # Statistiques et progression
    st.metric("Tentatives", st.session_state.compteur)
    if st.session_state.tentatives:
        last = st.session_state.tentatives[-1]
        closeness = 1 - (abs(last - st.session_state.nombre) / max(1, (max_val - min_val)))
        closeness_pct = int(max(0, min(1, closeness)) * 100)
    else:
        closeness_pct = 0
    st.progress(closeness_pct / 100)
    st.write(f"Proximité estimée : **{closeness_pct}%**")

    # Afficher meilleur score local
    if st.session_state.scores:
        best = min(s["score"] for s in st.session_state.scores)
        st.metric("Meilleur score local", best)
    else:
        st.metric("Meilleur score local", "—")

    # Boutons utilitaires
    if st.button("Nouvelle partie", key="new_game"):
        st.session_state.nombre = random.randint(min_val, max_val)
        st.session_state.compteur = 0
        st.session_state.message = ""
        st.session_state.tentatives = []
        st.session_state.hints_used = 0
        st.success("Nouvelle partie lancée !")

    if st.button("Révéler le nombre (abandon)"):
        st.warning(f"Le nombre était {st.session_state.nombre}")
        st.session_state.message = ""
        st.session_state.tentatives = []

# --- Affichage final et conseils ---
st.markdown("---")
st.write("**Conseils** : utilise les indices avec parcimonie (ils coûtent une tentative). Ajuste la plage pour rendre le jeu plus facile ou plus difficile.")

# --- Optionnel : afficher debug (décommenter si besoin) ---
# st.write("DEBUG:", st.session_state)