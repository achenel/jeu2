import streamlit as st
import random

st.title("Test 2")
st.write("Clique pour m'aider.")

# Initialiser la liste des cercles
if "circles" not in st.session_state:
    st.session_state.circles = []

# Bouton : ajoute un nouveau cercle
if st.button("Clique"):
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    x = random.randint(0, 90)   # position horizontale en % de la largeur
    y = random.randint(0, 90)   # position verticale en % de la hauteur
    size = random.randint(20, 100)  # taille aléatoire entre 20px et 100px
    st.session_state.circles.append((x, y, size, color))

# Construire le HTML avec tous les cercles
circles_html = "".join(
    f"""
    <div style="
        position: fixed;
        left: {x}vw; top: {y}vh;
        width: {size}px; height: {size}px;
        border-radius: 50%;
        background-color: {color};
        z-index: 999;
    "></div>
    """
    for x, y, size, color in st.session_state.circles
)

# Injecter le HTML
st.markdown(circles_html, unsafe_allow_html=True)