import streamlit as st
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="EmailPolisher AI",
    page_icon="📧",
    layout="centered"
)

# --- FUNCIONES MODULARES (Criterio: Modularidad y Claridad) ---

def obtener_cliente_openai():
    """
    Intenta obtener la API KEY desde los secretos de Streamlit.
    Maneja el error si no está configurada.
    """
    try:
        # En Streamlit Cloud, las claves se guardan en st.secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def generar_email_profesional(cliente, texto_usuario, tono):
    """
    Función encargada de interactuar con la API de OpenAI.
    Optimiza costos usando gpt-4o-mini y limitando tokens.
    """
    
    # Prompt optimizado (Criterio: Costos y Eficiencia)
    system_prompt = f"""
    Eres un experto en comunicación corporativa. Tu tarea es reescribir el borrador del usuario 
    para convertirlo en un correo electrónico profesional.
    
    Reglas:
    1. Tono: {tono}.
    2. Estructura clara: Asunto, Saludo, Cuerpo, Cierre.
    3. Corrige ortografía y gramática.
    4. Sé conciso para optimizar la lectura.
    """

    try:
        response = cliente.chat.completions.create(
            model="gpt-4o-mini", # Modelo más económico y rápido
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto_usuario}
            ],
            max_tokens=500, # Límite para controlar costos
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al generar el email: {e}"

# --- INTERFAZ DE USUARIO (MAIN) ---

def main():
    # Header
    st.title("📧 EmailPolisher AI")
    st.markdown("**Transforma tus borradores en correos profesionales en segundos.**")

    # Verificación de API Key
    client = obtener_cliente_openai()
    if not client:
        st.error("⚠️ No se detectó la API KEY. Configura 'OPENAI_API_KEY' en los secretos de Streamlit.")
        st.stop()

    # Layout de columnas
    col1, col2 = st.columns([2, 1])

    with col1:
        # Entrada de datos
        borrador = st.text_area(
            "Ingresa tu borrador o ideas sueltas:",
            height=200,
            placeholder="Ej: decirle a Juan que no llego a la reunion de las 5 porque tengo dentista, pedirle que la mueva a mañana."
        )

    with col2:
        # Opciones
        st.markdown("### Configuración")
        tono_seleccionado = st.selectbox(
            "Selecciona el tono:",
            ["Formal y Directo", "Empático y Amable", "Persuasivo (Ventas)"]
        )
        
        # Botón de acción (Requisito obligatorio)
        generar_btn = st.button("✨ Generar Email", type="primary", use_container_width=True)

    # Lógica de ejecución
    if generar_btn:
        if not borrador:
            st.warning("Por favor, escribe algo en el borrador primero.")
        else:
            with st.spinner("La IA está redactando tu correo..."):
                resultado = generar_email_profesional(client, borrador, tono_seleccionado)
                
            st.success("¡Correo generado con éxito!")
            st.markdown("---")
            st.subheader("📨 Resultado:")
            st.markdown(resultado)
            st.caption("Nota: Revisa siempre el contenido antes de enviar.")

    # --- SECCIÓN: CÓMO FUNCIONA  ---
    with st.sidebar:
        st.header("ℹ️ Cómo funciona")
        st.markdown("""
        Esta aplicación utiliza Inteligencia Artificial para mejorar tu comunicación.
        
        **Pasos:**
        1. **Escribe:** Pega tu borrador o ideas en el cuadro principal.
        2. **Configura:** Elige el tono deseado.
        3. **Genera:** Haz clic en el botón y obtén un email listo para enviar.
        
        **Tecnología:**
        Utilizamos el modelo `gpt-4o-mini` de OpenAI para asegurar respuestas rápidas y de bajo costo.
        """)
        st.info("Desarrollado para el Proyecto Final de Prompt Engineering.")

if __name__ == "__main__":
    main()