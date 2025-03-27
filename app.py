import streamlit as st
import json
import plotly.graph_objects as go
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu

# Configuration de la page
st.set_page_config(layout="wide", page_title="Atomic Visualizer")

# Données des éléments (simplifié)
with open("elements.json") as f:
    elements = json.load(f)

# CSS personnalisé
st.markdown("""
<style>
.element-card {
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 5px;
    cursor: grab;
    transition: transform 0.2s;
}
.element-card:hover {
    transform: scale(1.1);
}

.workspace {
    border: 2px dashed #ccc;
    min-height: 600px;
    margin: 20px 0;
    position: relative;
}

@keyframes orbit {
    from { transform: rotate(0deg) translateX(50px) rotate(0deg); }
    to { transform: rotate(360deg) translateX(50px) rotate(-360deg); }
}
</style>
""", unsafe_allow_html=True)

# Navigation
selected = option_menu(
    menu_title=None,
    options=["Accueil", "Effacer", "Connexion"],
    icons=["house", "eraser", "person"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Gestion d'état
if "selected_elements" not in st.session_state:
    st.session_state.selected_elements = []

# Fonction pour générer l'animation atomique
def create_atom_animation(element):
    fig = go.Figure()
    
    # Noyau
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(
            size=20,
            color='rgba(255, 0, 0, 0.8)',
            opacity=0.8
        ),
        name='Noyau'
    ))
    
    # Électrons
    for i in range(element['atomic_number']):
        theta = i * (360/element['atomic_number'])
        fig.add_trace(go.Scatter3d(
            x=[50 * np.cos(theta)],
            y=[50 * np.sin(theta)],
            z=[0],
            mode='markers',
            marker=dict(size=10, color='blue'),
            name=f'Électron {i+1}'
        ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    return fig

# Affichage des éléments
with st.container():
    cols = st.columns(10)
    element_cols = [cols[i % 10] for i in range(len(elements))]
    
    for idx, element in enumerate(elements):
        with element_cols[idx]:
            st.markdown(
                f"""
                <div class="element-card" style="background: {element['color']};"
                     onclick="window.parent.postMessage({{'type': 'elementSelected', 'data': {element}}}, '*')">
                    <strong>{element['symbol']}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

# Espace de travail
workspace = st.empty()
current_elements = st.session_state.selected_elements.copy()

# JavaScript pour gérer le drag-and-drop
html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'elementSelected') {
        window.parent.streamlitApi.runScript({
            "type": "elementSelected",
            "data": event.data.data
        })
    }
});
</script>
""")

# Gestion des sélections
if st.session_state.get('selected_element'):
    element = st.session_state.selected_element
    current_elements.append(element)
    st.session_state.selected_elements = current_elements

# Affichage des éléments dans l'espace de travail
with workspace.container():
    if st.session_state.selected_elements:
        cols = st.columns(len(st.session_state.selected_elements))
        for idx, element in enumerate(st.session_state.selected_elements):
            with cols[idx]:
                st.plotly_chart(
                    create_atom_animation(element),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )
    else:
        st.markdown("<div class='workspace'></div>", unsafe_allow_html=True)

# Gestion des actions
if selected == "Effacer":
    st.session_state.selected_elements = []
    st.experimental_rerun()
