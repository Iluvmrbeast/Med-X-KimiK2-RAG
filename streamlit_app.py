#!/usr/bin/env python3
"""
🏥 MedeX - Medical AI Intelligence System
Streamlit Interface for Hugging Face Spaces

Professional medical AI assistant with intelligent user detection,
emergency protocols, and comprehensive medical knowledge base.
"""

import streamlit as st
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import MedeX system
from MEDEX_FINAL import MedeXv2583

# Page configuration
st.set_page_config(
    page_title="MedeX - Medical AI System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",  # Sidebar starts expanded
    menu_items={
        "Get Help": "https://huggingface.co/spaces",
        "Report a bug": None,
        "About": """
        # MedeX - Medical AI Intelligence System
        
        Advanced medical AI assistant powered by Kimi K2-0711-Preview.
        
        **Features:**
        - Intelligent user detection (Educational vs Professional)
        - Emergency protocol activation
        - AI-enhanced medical knowledge base
        - Real-time streaming responses
        
        **⚠️ Important Disclaimers:**
        - For educational purposes only
        - Does NOT replace professional medical consultation
        - In real emergencies, call 911 immediately
        """,
    },
)

# Custom CSS - Clean & Elegant Medical Interface (Inspired by Canva Design)
st.markdown(
    """
<style>
    /* Color palette from Canva design */
    :root {
        --medex-green: #3b8e72;
        --medex-green-light: #90ceb1;
        --chat-bg: #f8f8f9;
        --disclaimer-orange: #ff751f;
        --white: #ffffff;
        --text-dark: #2d3748;
        --text-gray: #718096;
        --border-light: #e2e8f0;
        --emergency-red: #ef4444;
    }
    
    /* Global background - Clean white */
    .main {
        background-color: var(--white);
    }
    
    /* Chat area background - More pronounced gray to make bubbles stand out */
    .main .block-container {
        background: linear-gradient(to bottom, #f8f8f9 0%, #f1f3f5 100%);
        border-radius: 12px;
        padding: 2rem;
    }
    
    /* Hide Streamlit default footer ONLY - Keep header for sidebar controls */
    footer {
        visibility: hidden;
    }
    
    /* CRITICAL: Ensure Streamlit header with controls is ALWAYS visible */
    header {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Force visibility of ALL header elements including sidebar toggle */
    header * {
        visibility: visible !important;
        display: inherit !important;
        opacity: 1 !important;
    }
    
    /* Compact header - Only subtitle, no logo */
    .medex-subtitle {
        display: inline-block;
        background-color: var(--medex-green-light);
        color: var(--text-dark);
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 1rem 0 1.5rem 0;
    }
    
    /* Chat container background */
    .stChatFloatingInputContainer {
        background-color: var(--chat-bg);
        padding: 1rem;
        border-radius: 12px;
    }
    
    /* User message bubble - Green with STRONG visible border */
    .stChatMessage[data-testid="user-message"],
    div[data-testid="stChatMessage"]:has(div[data-testid="user-message"]),
    .stChatMessage:has([data-testid="user-message"]) {
        background-color: var(--medex-green) !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 1rem 1.25rem !important;
        margin: 0.75rem 0 !important;
        box-shadow: 0 4px 12px rgba(59, 142, 114, 0.4) !important;
        border: 4px solid #1a5a44 !important;
    }
    
    .stChatMessage[data-testid="user-message"] p,
    .stChatMessage[data-testid="user-message"] div {
        color: white !important;
    }
    
    /* Assistant message bubble - White with STRONG visible border */
    .stChatMessage[data-testid="assistant-message"],
    div[data-testid="stChatMessage"]:has(div[data-testid="assistant-message"]),
    .stChatMessage:has([data-testid="assistant-message"]) {
        background-color: var(--white) !important;
        border-radius: 18px !important;
        padding: 1rem 1.25rem !important;
        margin: 0.75rem 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        border: 4px solid #64748b !important;
    }
    
    /* Fallback for ALL chat messages - FORCE visible borders */
    [data-testid="stChatMessage"],
    .stChatMessage,
    div[class*="stChatMessage"] {
        border: 4px solid #94a3b8 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        border-radius: 18px !important;
        margin: 0.75rem 0 !important;
    }
    
    /* User type badges - Compact & elegant */
    .user-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
    }
    
    .badge-professional {
        background-color: var(--medex-green);
        color: white;
    }
    
    .badge-educational {
        background-color: var(--medex-green);
        color: white;
    }
    
    .badge-emergency {
        background-color: var(--emergency-red);
        color: white;
        animation: pulse-soft 2s ease-in-out infinite;
    }
    
    @keyframes pulse-soft {
        0%, 100% { 
            opacity: 1;
            transform: scale(1);
        }
        50% { 
            opacity: 0.9;
            transform: scale(1.02);
        }
    }
    
    /* Sidebar - Clean & minimal - Always accessible */
    section[data-testid="stSidebar"] {
        background-color: var(--white);
        border-right: 1px solid var(--border-light);
        transition: all 0.3s ease-in-out;
        min-width: 200px; /* Prevent complete collapse */
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Prevent sidebar from being completely hidden */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 50px !important;
        display: block !important;
    }
    
    /* CRITICAL: Force sidebar toggle to always be visible and functional */
    button[kind="header"],
    button[data-testid="baseButton-header"],
    button[data-testid="collapsedControl"],
    [data-testid="stSidebarNav"] button,
    [class*="viewerBadge"],
    [data-testid="stHeader"] button {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        position: relative !important;
        z-index: 999999 !important;
    }
    
    /* Sidebar collapse/expand button - ALWAYS visible and accessible */
    [data-testid="collapsedControl"],
    button[aria-label*="sidebar"],
    button[title*="sidebar"] {
        display: flex !important;
        visibility: visible !important;
        cursor: pointer !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 999999 !important;
        background-color: var(--medex-green) !important;
        color: white !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 0.5rem !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Ensure header toolbar is always visible */
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
    }
    
    /* When sidebar is collapsed, make the reopen button very visible */
    [data-testid="collapsedControl"] {
        background-color: var(--medex-green) !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Sidebar headers */
    section[data-testid="stSidebar"] h3 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: 0.75rem;
        font-style: italic;
    }
    
    /* Quick Actions buttons */
    section[data-testid="stSidebar"] button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid var(--border-light);
        background-color: var(--white);
        color: var(--text-dark);
        font-weight: 500;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background-color: var(--chat-bg);
        border-color: var(--medex-green);
    }
    
    /* Disclaimer box - Orange like in image */
    .disclaimer-box {
        background-color: var(--disclaimer-orange);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(255, 117, 31, 0.25);
    }
    
    .disclaimer-box strong {
        font-weight: 700;
    }
    
    /* Emergency banner - Minimal & clear */
    .emergency-banner {
        background-color: #fef2f2;
        border-left: 4px solid var(--emergency-red);
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .emergency-banner h3 {
        color: var(--emergency-red);
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .emergency-banner p, .emergency-banner ul {
        color: var(--text-dark);
        font-size: 0.95rem;
    }
    
    /* Info box - Subtle & elegant */
    .info-box {
        background-color: #f7fafc;
        border-left: 4px solid var(--medex-green);
        padding: 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box strong {
        color: var(--medex-green);
        font-weight: 600;
    }
    
    /* Stats metrics */
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--medex-green);
    }
    
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: var(--text-gray);
        font-weight: 500;
    }
    
    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid var(--border-light);
        padding-top: 1rem;
    }
    
    .stChatInputContainer input {
        border-radius: 24px;
        border: 2px solid var(--border-light);
        padding: 0.75rem 1.25rem;
        font-size: 0.95rem;
    }
    
    .stChatInputContainer input:focus {
        border-color: var(--medex-green);
        box-shadow: 0 0 0 3px rgba(59, 142, 114, 0.1);
    }
    
    /* Scrollbar - Subtle */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--chat-bg);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a0aec0;
    }
    
    /* Remove unnecessary padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--chat-bg);
        border-radius: 8px;
        font-weight: 500;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if "medex_system" not in st.session_state:
        st.session_state.medex_system = None
        st.session_state.initialized = False

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "session_stats" not in st.session_state:
        st.session_state.session_stats = {
            "total_queries": 0,
            "professional_queries": 0,
            "educational_queries": 0,
            "emergency_queries": 0,
            "images_analyzed": 0,
            "session_start": datetime.now(),
        }

    if "current_user_type" not in st.session_state:
        st.session_state.current_user_type = None

    if "current_emergency" not in st.session_state:
        st.session_state.current_emergency = False


@st.cache_resource
def initialize_medex():
    """Initialize MedeX system with caching"""
    try:
        with st.spinner("🧠 Initializing MedeX v25.83 System..."):
            medex = MedeXv2583()
            return medex
    except Exception as e:
        st.error(f"❌ Error initializing MedeX: {e}")
        return None


def render_header():
    """Render minimal header - Only subtitle"""
    st.markdown(
        """
    <div class="medex-subtitle">
        Asistencia Médica para Profesionales y Estudiantes
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render clean sidebar like Canva design"""
    with st.sidebar:
        # Logo banner
        st.image(str(Path("banner.png")))

        st.markdown("---")

        # Quick Actions
        st.markdown("### Quick Actions")

        if st.button(
            "Limpiar Historial",
            key="clear_history_btn",
            help="Limpiar todos los mensajes del chat",
        ):
            st.session_state.chat_history = []
            st.rerun()

        if st.button(
            "Exportar Chat",
            key="export_session_btn",
            help="Exportar datos de la sesión",
        ):
            export_session()

        st.markdown("---")

        # About Med-X
        st.markdown("### About Med-X")
        st.markdown(
            """
            • **Detección inteligente**: Identifica automáticamente si eres un profesional de la salud o buscas información educativa.
            
            • **Reconocimiento de emergencias**: Detecta situaciones médicas urgentes y activa protocolos de emergencia.
            
            • **Mejora con IA**: Con tecnología Kimi K2 (Vista previa) para información médica precisa.
            
            • **Respuestas adaptativas**: Adapta el lenguaje y el nivel de detalle a tus necesidades.
            """
        )

        st.markdown("---")

        # Examples section - In sidebar
        with st.expander("💡 Ejemplos de consultas"):
            st.markdown("**👨‍⚕️ Profesionales:**")
            st.caption("Paciente 65 años, diabético, dolor precordial de 2 horas")
            st.caption("Protocolo de manejo de síndrome coronario agudo")

            st.markdown("**🎓 Educativas:**")
            st.caption("¿Qué es la diabetes tipo 2?")
            st.caption("Explica la fisiopatología de la insuficiencia cardíaca")

        st.markdown("---")

        # Session Statistics
        st.markdown("### 📊 Session Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", st.session_state.session_stats["total_queries"])
            st.metric(
                "👨‍⚕️ Professional",
                st.session_state.session_stats["professional_queries"],
            )
        with col2:
            st.metric(
                "🎓 Educational", st.session_state.session_stats["educational_queries"]
            )
            st.metric(
                "🚨 Emergency", st.session_state.session_stats["emergency_queries"]
            )

        st.markdown("---")

        # Important Disclaimers
        st.markdown(
            """
        <div class="disclaimer-box">
            <strong>⚠️ Important Disclaimers</strong><br><br>
            • Solo con fines educativos<br>
            • No reemplaza el consejo médico<br>
            • En emergencias, llame al 911<br>
            • Siempre consulte a profesionales de la salud
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Compact footer
        st.markdown("---")
        st.markdown(
            """
        <div style="text-align: center; font-size: 0.75rem; color: #718096;">
            MedeX v25.83 | Powered by Kimi K2
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_user_type_badge(user_type, is_emergency):
    """Render user type badge"""
    if is_emergency:
        return '<span class="user-badge badge-emergency">🚨 EMERGENCY</span>'
    elif user_type == "Professional":
        return '<span class="user-badge badge-professional">👨‍⚕️ PROFESSIONAL</span>'
    else:
        return '<span class="user-badge badge-educational">🎓 EDUCATIONAL</span>'


def render_emergency_banner():
    """Render emergency protocol banner"""
    st.markdown(
        """
    <div class="emergency-banner">
        <h3>🚨 EMERGENCY PROTOCOL ACTIVATED</h3>
        <p><strong>This query has been identified as a potential medical emergency.</strong></p>
        <p>If you or someone else is experiencing a medical emergency:</p>
        <ul>
            <li>📞 <strong>Call 911 immediately</strong></li>
            <li>🏥 Go to the nearest emergency room</li>
            <li>⏰ Do not wait for online responses</li>
        </ul>
        <p>The following information is for educational context only and does NOT replace emergency medical care.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


async def process_medical_query(query_text):
    """Process medical query with MedeX system"""

    try:
        # Get MedeX system
        medex = st.session_state.medex_system

        # Detect user type and emergency
        user_type = medex.detect_user_type(query_text)
        is_emergency = medex.detect_emergency(query_text)

        # Update session state
        st.session_state.current_user_type = user_type
        st.session_state.current_emergency = is_emergency

        # Update statistics
        st.session_state.session_stats["total_queries"] += 1
        if user_type == "Professional":
            st.session_state.session_stats["professional_queries"] += 1
        else:
            st.session_state.session_stats["educational_queries"] += 1
        if is_emergency:
            st.session_state.session_stats["emergency_queries"] += 1

        # Show emergency banner if needed
        if is_emergency:
            render_emergency_banner()

        # Display user type badge
        badge_html = render_user_type_badge(user_type, is_emergency)
        st.markdown(badge_html, unsafe_allow_html=True)

        # Generate response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Generate response with REAL streaming
            if st.session_state.get("streaming_enabled", True):
                # Usar el generador asíncrono para streaming real
                async for chunk in medex.generate_response_stream(query_text):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")

                # Remover cursor al final
                message_placeholder.markdown(full_response)
            else:
                # Sin streaming - generar respuesta completa
                response = await medex.generate_response(
                    query_text, use_streaming=False
                )
                message_placeholder.markdown(response)
                full_response = response

            return full_response

    except Exception as e:
        st.error(f"❌ Error processing query: {e}")
        return None


def export_session():
    """Export session data"""
    try:
        # Convert datetime objects to ISO format strings for JSON serialization
        session_stats_serializable = {
            "total_queries": st.session_state.session_stats["total_queries"],
            "professional_queries": st.session_state.session_stats[
                "professional_queries"
            ],
            "educational_queries": st.session_state.session_stats[
                "educational_queries"
            ],
            "emergency_queries": st.session_state.session_stats["emergency_queries"],
            "images_analyzed": st.session_state.session_stats["images_analyzed"],
            "session_start": st.session_state.session_stats[
                "session_start"
            ].isoformat(),
        }

        session_data = {
            "session_start": st.session_state.session_stats[
                "session_start"
            ].isoformat(),
            "statistics": session_stats_serializable,
            "chat_history": st.session_state.chat_history,
        }

        # Create download button
        import json

        json_str = json.dumps(session_data, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download Session Data (JSON)",
            data=json_str,
            file_name=f"medex_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )

        st.success("✅ Session data ready for download!")

    except Exception as e:
        st.error(f"Error exporting session: {e}")


def main():
    """Main application"""

    # Initialize session state
    init_session_state()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar()

    # Initialize MedeX system
    if not st.session_state.initialized:
        st.session_state.medex_system = initialize_medex()
        if st.session_state.medex_system:
            st.session_state.initialized = True
            st.success("✅ MedeX v25.83 System initialized successfully!")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message.get("user_type"):
                badge_html = render_user_type_badge(
                    message["user_type"], message.get("is_emergency", False)
                )
                st.markdown(badge_html, unsafe_allow_html=True)
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input(
        "Escribe tu consulta médica aquí...", key="main_chat_input"
    ):
        # Check if system is initialized
        if not st.session_state.initialized:
            st.error("⚠️ System not initialized. Please wait...")
            return

        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process query asynchronously
        response = asyncio.run(process_medical_query(prompt))

        # Add assistant response to chat
        if response:
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": response,
                    "user_type": st.session_state.current_user_type,
                    "is_emergency": st.session_state.current_emergency,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            # Force rerun to update statistics in sidebar
            st.rerun()


if __name__ == "__main__":
    main()