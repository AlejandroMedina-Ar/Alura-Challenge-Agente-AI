"""
Módulo de Componentes

Este módulo proporciona componentes de UI reutilizables para Streamlit.
Incluye botones, tarjetas, formularios y otros elementos de UI.

Autor: TechFlow Solutions Project
Licencia: MIT
"""

import streamlit as st
from typing import Optional, Callable

from src.utils import get_logger


logger = get_logger()


def render_header(title: str, subtitle: str = None) -> None:
    """
    Renderiza encabezado de página con título y subtítulo opcional.
    
    Args:
        title: Título de la página
        subtitle: Subtítulo opcional
    
    Ejemplo:
        >>> render_header("TechFlow Solutions", "Agente RAG")
    """
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def render_metric_card(
    label: str,
    value: str,
    delta: str = None,
    help_text: str = None
) -> None:
    """
    Renderiza tarjeta de métrica.
    
    Args:
        label: Etiqueta de la métrica
        value: Valor de la métrica
        delta: Valor delta/cambio opcional
        help_text: Texto de ayuda opcional
    
    Ejemplo:
        >>> render_metric_card("Documentos", "42", "+5", "Total indexados")
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text
    )


def render_info_message(
    message: str,
    message_type: str = "info"
) -> None:
    """
    Renderiza caja de mensaje informativo.
    
    Args:
        message: Texto del mensaje
        message_type: Tipo ('info', 'success', 'warning', 'error')
    
    Ejemplo:
        >>> render_info_message("¡Carga exitosa!", "success")
    """
    if message_type == "success":
        st.success(message)
    elif message_type == "warning":
        st.warning(message)
    elif message_type == "error":
        st.error(message)
    else:
        st.info(message)


def render_file_uploader(
    label: str = "Subir Documento",
    accepted_types: list = None,
    help_text: str = None,
    key: str = None
) -> Optional:
    """
    Renderiza componente de carga de archivos.
    
    Args:
        label: Etiqueta del cargador
        accepted_types: Lista de extensiones de archivo aceptadas
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
    
    Retorna:
        UploadedFile o None
    
    Ejemplo:
        >>> file = render_file_uploader(
        ...     "Subir PDF",
        ...     accepted_types=['pdf'],
        ...     help_text="Máx 10MB"
        ... )
    """
    if accepted_types is None:
        accepted_types = ['txt', 'pdf', 'docx', 'md']
    
    return st.file_uploader(
        label=label,
        type=accepted_types,
        help=help_text,
        key=key
    )


def render_text_input(
    label: str,
    placeholder: str = "",
    help_text: str = None,
    key: str = None,
    password: bool = False
) -> str:
    """
    Renderiza campo de entrada de texto.
    
    Args:
        label: Etiqueta del input
        placeholder: Texto de marcador de posición
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
        password: Si se debe enmascarar la entrada
    
    Retorna:
        str: Valor de entrada
    
    Ejemplo:
        >>> name = render_text_input("Tu nombre", placeholder="Juan Pérez")
    """
    input_type = "password" if password else "default"
    
    return st.text_input(
        label=label,
        placeholder=placeholder,
        help=help_text,
        key=key,
        type=input_type
    )


def render_text_area(
    label: str,
    placeholder: str = "",
    height: int = 150,
    help_text: str = None,
    key: str = None
) -> str:
    """
    Renderiza campo de área de texto.
    
    Args:
        label: Etiqueta del área de texto
        placeholder: Texto de marcador de posición
        height: Altura en píxeles
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
    
    Retorna:
        str: Contenido del área de texto
    
    Ejemplo:
        >>> question = render_text_area(
        ...     "Tu pregunta",
        ...     placeholder="¿Qué es RAG?",
        ...     height=100
        ... )
    """
    return st.text_area(
        label=label,
        placeholder=placeholder,
        height=height,
        help=help_text,
        key=key
    )


def render_button(
    label: str,
    on_click: Callable = None,
    button_type: str = "primary",
    disabled: bool = False,
    help_text: str = None,
    key: str = None,
    use_container_width: bool = False
) -> bool:
    """
    Renderiza botón.
    
    Args:
        label: Etiqueta del botón
        on_click: Manejador de clic opcional
        button_type: Tipo ('primary' o 'secondary')
        disabled: Si el botón está deshabilitado
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
        use_container_width: Si el botón ocupa todo el ancho del contenedor
    
    Retorna:
        bool: True si se hizo clic
    
    Ejemplo:
        >>> if render_button("Enviar", button_type="primary"):
        ...     st.success("¡Enviado!")
    """
    return st.button(
        label=label,
        on_click=on_click,
        type=button_type,
        disabled=disabled,
        help=help_text,
        key=key,
        use_container_width=use_container_width
    )


def render_select_box(
    label: str,
    options: list,
    default_index: int = 0,
    help_text: str = None,
    key: str = None
) -> any:
    """
    Renderiza menú desplegable de selección.
    
    Args:
        label: Etiqueta del select box
        options: Lista de opciones
        default_index: Índice seleccionado por defecto
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
    
    Retorna:
        Opción seleccionada
    
    Ejemplo:
        >>> provider = render_select_box(
        ...     "Proveedor LLM",
        ...     options=['gemini', 'cohere']
        ... )
    """
    return st.selectbox(
        label=label,
        options=options,
        index=default_index,
        help=help_text,
        key=key
    )


def render_slider(
    label: str,
    min_value: float,
    max_value: float,
    value: float,
    step: float = 0.1,
    help_text: str = None,
    key: str = None
) -> float:
    """
    Renderiza entrada deslizante.
    
    Args:
        label: Etiqueta del slider
        min_value: Valor mínimo
        max_value: Valor máximo
        value: Valor por defecto
        step: Incremento del paso
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
    
    Retorna:
        float: Valor seleccionado
    
    Ejemplo:
        >>> temp = render_slider(
        ...     "Temperatura",
        ...     min_value=0.0,
        ...     max_value=2.0,
        ...     value=0.7,
        ...     step=0.1
        ... )
    """
    return st.slider(
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=help_text,
        key=key
    )


def render_number_input(
    label: str,
    min_value: int,
    max_value: int,
    value: int,
    step: int = 1,
    help_text: str = None,
    key: str = None
) -> int:
    """
    Renderiza campo de entrada numérica.
    
    Args:
        label: Etiqueta del input
        min_value: Valor mínimo
        max_value: Valor máximo
        value: Valor por defecto
        step: Incremento del paso
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
    
    Retorna:
        int: Valor de entrada
    
    Ejemplo:
        >>> top_k = render_number_input(
        ...     "Top K",
        ...     min_value=1,
        ...     max_value=20,
        ...     value=5
        ... )
    """
    return st.number_input(
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        help=help_text,
        key=key
    )


def render_checkbox(
    label: str,
    value: bool = False,
    help_text: str = None,
    key: str = None
) -> bool:
    """
    Renderiza casilla de verificación.
    
    Args:
        label: Etiqueta del checkbox
        value: Valor por defecto
        help_text: Texto de ayuda opcional
        key: Clave de widget opcional
    
    Retorna:
        bool: Estado del checkbox
    
    Ejemplo:
        >>> stream = render_checkbox("Respuesta en streaming", value=True)
    """
    return st.checkbox(
        label=label,
        value=value,
        help=help_text,
        key=key
    )


def render_expander(
    label: str,
    expanded: bool = False
) -> st.expander:
    """
    Renderiza sección expandible/colapsable.
    
    Args:
        label: Etiqueta del expander
        expanded: Si está expandido por defecto
    
    Retorna:
        st.expander: Contexto del expander
    
    Ejemplo:
        >>> with render_expander("Configuración Avanzada"):
        ...     st.write("Opciones avanzadas aquí")
    """
    return st.expander(label=label, expanded=expanded)


def render_spinner(message: str = "Cargando...") -> st.spinner:
    """
    Renderiza spinner de carga.
    
    Args:
        message: Mensaje de carga
    
    Retorna:
        st.spinner: Contexto del spinner
    
    Ejemplo:
        >>> with render_spinner("Indexando documento..."):
        ...     # Operación larga
        ...     time.sleep(2)
    """
    return st.spinner(message)


def render_progress_bar(
    progress: float,
    text: str = None
) -> None:
    """
    Renderiza barra de progreso.
    
    Args:
        progress: Valor de progreso (0.0 a 1.0)
        text: Texto de progreso opcional
    
    Ejemplo:
        >>> render_progress_bar(0.5, "50% completado")
    """
    st.progress(progress, text=text)


def render_tabs(tab_labels: list[str]) -> list:
    """
    Renderiza pestañas.
    
    Args:
        tab_labels: Lista de etiquetas de pestañas
    
    Retorna:
        list: Lista de contextos de pestañas
    
    Ejemplo:
        >>> tabs = render_tabs(["Chat", "Documentos", "Configuración"])
        >>> with tabs[0]:
        ...     st.write("Contenido del chat")
    """
    return st.tabs(tab_labels)


def render_columns(num_columns: int, gap: str = "small") -> list:
    """
    Renderiza diseño de columnas.
    
    Args:
        num_columns: Número de columnas
        gap: Tamaño del espacio ('small', 'medium', 'large')
    
    Retorna:
        list: Lista de contextos de columnas
    
    Ejemplo:
        >>> cols = render_columns(3)
        >>> with cols[0]:
        ...     st.metric("Docs", "42")
        >>> with cols[1]:
        ...     st.metric("Fragmentos", "210")
        >>> with cols[2]:
        ...     st.metric("Consultas", "156")
    """
    return st.columns(num_columns, gap=gap)


def render_empty_state(
    icon: str,
    title: str,
    message: str,
    action_label: str = None,
    action_callback: Callable = None
) -> None:
    """
    Renderiza marcador de estado vacío.
    
    Args:
        icon: Icono emoji
        title: Título del estado vacío
        message: Mensaje del estado vacío
        action_label: Etiqueta del botón de acción opcional
        action_callback: Callback de acción opcional
    
    Ejemplo:
        >>> render_empty_state(
        ...     icon="📄",
        ...     title="Sin documentos",
        ...     message="Sube tu primer documento para comenzar",
        ...     action_label="Subir Documento"
        ... )
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem 1rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h3>{title}</h3>
            <p style="color: #6c757d;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if action_label and action_callback:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.button(action_label, on_click=action_callback, type="primary")


def render_data_table(
    data: list[dict],
    columns: list[str] = None
) -> None:
    """
    Renderiza tabla de datos.
    
    Args:
        data: Lista de diccionarios de datos
        columns: Nombres de columnas opcionales a mostrar
    
    Ejemplo:
        >>> data = [
        ...     {'nombre': 'Doc1', 'tamaño': '1.2MB'},
        ...     {'nombre': 'Doc2', 'tamaño': '0.8MB'}
        ... ]
        >>> render_data_table(data)
    """
    import pandas as pd
    
    if not data:
        st.info("No hay datos para mostrar")
        return
    
    df = pd.DataFrame(data)
    
    if columns:
        df = df[columns]
    
    st.dataframe(df, use_container_width=True)


# Convenience: Allow direct import
__all__ = [
    'render_header',
    'render_metric_card',
    'render_info_message',
    'render_file_uploader',
    'render_text_input',
    'render_text_area',
    'render_button',
    'render_select_box',
    'render_slider',
    'render_number_input',
    'render_checkbox',
    'render_expander',
    'render_spinner',
    'render_progress_bar',
    'render_tabs',
    'render_columns',
    'render_empty_state',
    'render_data_table',
]
