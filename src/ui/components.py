"""
Components Module

This module provides reusable UI components for Streamlit.
Includes buttons, cards, forms, and other UI elements.

Author: TechFlow AI Project
License: MIT
"""

import streamlit as st
from typing import Optional, Callable

from src.utils import get_logger


logger = get_logger()


def render_header(title: str, subtitle: str = None) -> None:
    """
    Render page header with title and optional subtitle.
    
    Args:
        title: Page title
        subtitle: Optional subtitle
    
    Example:
        >>> render_header("TechFlow AI", "RAG Agent")
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
    Render metric card.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change value
        help_text: Optional help tooltip
    
    Example:
        >>> render_metric_card("Documents", "42", "+5", "Total indexed")
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
    Render info message box.
    
    Args:
        message: Message text
        message_type: Type ('info', 'success', 'warning', 'error')
    
    Example:
        >>> render_info_message("Upload successful!", "success")
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
    label: str = "Upload Document",
    accepted_types: list = None,
    help_text: str = None,
    key: str = None
) -> Optional:
    """
    Render file uploader component.
    
    Args:
        label: Uploader label
        accepted_types: List of accepted file extensions
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        UploadedFile or None
    
    Example:
        >>> file = render_file_uploader(
        ...     "Upload PDF",
        ...     accepted_types=['pdf'],
        ...     help_text="Max 10MB"
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
    Render text input field.
    
    Args:
        label: Input label
        placeholder: Placeholder text
        help_text: Optional help text
        key: Optional widget key
        password: Whether to mask input
    
    Returns:
        str: Input value
    
    Example:
        >>> name = render_text_input("Your name", placeholder="John Doe")
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
    Render text area field.
    
    Args:
        label: Text area label
        placeholder: Placeholder text
        height: Height in pixels
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        str: Text area content
    
    Example:
        >>> question = render_text_area(
        ...     "Your question",
        ...     placeholder="What is RAG?",
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
    key: str = None
) -> bool:
    """
    Render button.
    
    Args:
        label: Button label
        on_click: Optional click handler
        button_type: Type ('primary' or 'secondary')
        disabled: Whether button is disabled
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        bool: True if clicked
    
    Example:
        >>> if render_button("Submit", button_type="primary"):
        ...     st.success("Submitted!")
    """
    return st.button(
        label=label,
        on_click=on_click,
        type=button_type,
        disabled=disabled,
        help=help_text,
        key=key
    )


def render_select_box(
    label: str,
    options: list,
    default_index: int = 0,
    help_text: str = None,
    key: str = None
) -> any:
    """
    Render select box dropdown.
    
    Args:
        label: Select box label
        options: List of options
        default_index: Default selected index
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        Selected option
    
    Example:
        >>> provider = render_select_box(
        ...     "LLM Provider",
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
    Render slider input.
    
    Args:
        label: Slider label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value
        step: Step increment
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        float: Selected value
    
    Example:
        >>> temp = render_slider(
        ...     "Temperature",
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
    Render number input field.
    
    Args:
        label: Input label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value
        step: Step increment
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        int: Input value
    
    Example:
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
    Render checkbox.
    
    Args:
        label: Checkbox label
        value: Default value
        help_text: Optional help text
        key: Optional widget key
    
    Returns:
        bool: Checkbox state
    
    Example:
        >>> stream = render_checkbox("Stream response", value=True)
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
    Render expander/collapsible section.
    
    Args:
        label: Expander label
        expanded: Whether expanded by default
    
    Returns:
        st.expander: Expander context
    
    Example:
        >>> with render_expander("Advanced Settings"):
        ...     st.write("Advanced options here")
    """
    return st.expander(label=label, expanded=expanded)


def render_spinner(message: str = "Loading...") -> st.spinner:
    """
    Render loading spinner.
    
    Args:
        message: Loading message
    
    Returns:
        st.spinner: Spinner context
    
    Example:
        >>> with render_spinner("Indexing document..."):
        ...     # Long operation
        ...     time.sleep(2)
    """
    return st.spinner(message)


def render_progress_bar(
    progress: float,
    text: str = None
) -> None:
    """
    Render progress bar.
    
    Args:
        progress: Progress value (0.0 to 1.0)
        text: Optional progress text
    
    Example:
        >>> render_progress_bar(0.5, "50% complete")
    """
    st.progress(progress, text=text)


def render_tabs(tab_labels: list[str]) -> list:
    """
    Render tabs.
    
    Args:
        tab_labels: List of tab labels
    
    Returns:
        list: List of tab contexts
    
    Example:
        >>> tabs = render_tabs(["Chat", "Documents", "Settings"])
        >>> with tabs[0]:
        ...     st.write("Chat content")
    """
    return st.tabs(tab_labels)


def render_columns(num_columns: int, gap: str = "small") -> list:
    """
    Render columns layout.
    
    Args:
        num_columns: Number of columns
        gap: Gap size ('small', 'medium', 'large')
    
    Returns:
        list: List of column contexts
    
    Example:
        >>> cols = render_columns(3)
        >>> with cols[0]:
        ...     st.metric("Docs", "42")
        >>> with cols[1]:
        ...     st.metric("Chunks", "210")
        >>> with cols[2]:
        ...     st.metric("Queries", "156")
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
    Render empty state placeholder.
    
    Args:
        icon: Emoji icon
        title: Empty state title
        message: Empty state message
        action_label: Optional action button label
        action_callback: Optional action callback
    
    Example:
        >>> render_empty_state(
        ...     icon="📄",
        ...     title="No documents",
        ...     message="Upload your first document to get started",
        ...     action_label="Upload Document"
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
    Render data table.
    
    Args:
        data: List of data dictionaries
        columns: Optional column names to display
    
    Example:
        >>> data = [
        ...     {'name': 'Doc1', 'size': '1.2MB'},
        ...     {'name': 'Doc2', 'size': '0.8MB'}
        ... ]
        >>> render_data_table(data)
    """
    import pandas as pd
    
    if not data:
        st.info("No data to display")
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
