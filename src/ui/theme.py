"""
Theme Module

This module handles UI theming and styling for Streamlit.
Provides light/dark theme management and custom CSS injection.

Author: TechFlow AI Project
License: MIT
"""

import streamlit as st
from pathlib import Path

from src.config import ASSETS_DIR
from src.utils import get_logger


logger = get_logger()


# Theme configurations
LIGHT_THEME = {
    'name': 'light',
    'primary_color': '#1f77b4',
    'background_color': '#ffffff',
    'secondary_background_color': '#f0f2f6',
    'text_color': '#262730',
    'font': 'sans-serif'
}

DARK_THEME = {
    'name': 'dark',
    'primary_color': '#4da6ff',
    'background_color': '#0e1117',
    'secondary_background_color': '#262730',
    'text_color': '#fafafa',
    'font': 'sans-serif'
}


def apply_theme(theme_name: str = 'light') -> None:
    """
    Apply theme to Streamlit app.
    
    Args:
        theme_name: Theme name ('light' or 'dark')
    
    Example:
        >>> apply_theme('dark')
    """
    try:
        theme = DARK_THEME if theme_name == 'dark' else LIGHT_THEME
        
        # Load custom CSS file
        css_file = ASSETS_DIR / 'css' / f'{theme_name}.css'
        
        if css_file.exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                css = f.read()
            
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
            logger.debug(f"Custom CSS loaded", theme=theme_name)
        else:
            logger.warning(f"CSS file not found", path=str(css_file))
            # Apply basic inline styles as fallback
            apply_inline_theme(theme)
        
        logger.info(f"Theme applied", theme=theme_name)
        
    except Exception as e:
        logger.error(f"Failed to apply theme", theme=theme_name, error=str(e))
        # Fallback to basic theme
        apply_inline_theme(LIGHT_THEME)


def apply_inline_theme(theme: dict) -> None:
    """
    Apply inline CSS theme (fallback when CSS file not found).
    
    Args:
        theme: Theme configuration dict
    """
    css = f"""
    <style>
        .stApp {{
            background-color: {theme['background_color']};
            color: {theme['text_color']};
        }}
        
        .stButton>button {{
            background-color: {theme['primary_color']};
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }}
        
        .stButton>button:hover {{
            opacity: 0.8;
        }}
        
        .stTextInput>div>div>input {{
            background-color: {theme['secondary_background_color']};
            color: {theme['text_color']};
            border-radius: 5px;
        }}
        
        .stSelectbox>div>div>select {{
            background-color: {theme['secondary_background_color']};
            color: {theme['text_color']};
            border-radius: 5px;
        }}
        
        .stMarkdown {{
            color: {theme['text_color']};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['text_color']};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def get_theme_icon(theme_name: str) -> str:
    """
    Get icon for theme.
    
    Args:
        theme_name: Theme name
    
    Returns:
        str: Icon emoji
    
    Example:
        >>> icon = get_theme_icon('dark')
        >>> print(icon)
        🌙
    """
    return '🌙' if theme_name == 'dark' else '☀️'


def inject_custom_css(css_content: str) -> None:
    """
    Inject custom CSS into the page.
    
    Args:
        css_content: CSS content to inject
    
    Example:
        >>> inject_custom_css(".custom-class { color: red; }")
    """
    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)


def load_theme_from_config(config_service) -> str:
    """
    Load theme from configuration service.
    
    Args:
        config_service: ConfigurationService instance
    
    Returns:
        str: Theme name
    
    Example:
        >>> from src.services import get_configuration_service
        >>> config = get_configuration_service()
        >>> theme = load_theme_from_config(config)
        >>> apply_theme(theme)
    """
    try:
        theme = config_service.get_theme()
        logger.debug(f"Theme loaded from config", theme=theme)
        return theme
    except Exception as e:
        logger.warning(f"Failed to load theme from config", error=str(e))
        return 'light'


def style_metric_card(
    label: str,
    value: str,
    delta: str = None,
    background_color: str = "#f0f2f6"
) -> str:
    """
    Generate styled metric card HTML.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta value
        background_color: Card background color
    
    Returns:
        str: HTML for metric card
    
    Example:
        >>> html = style_metric_card("Documents", "42", "+5")
        >>> st.markdown(html, unsafe_allow_html=True)
    """
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''
    
    html = f"""
    <div style="
        background-color: {background_color};
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    ">
        <div style="font-size: 0.875rem; color: #6c757d; margin-bottom: 0.25rem;">
            {label}
        </div>
        <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.25rem;">
            {value}
        </div>
        {delta_html}
    </div>
    """
    return html


def style_info_box(
    message: str,
    box_type: str = "info"
) -> str:
    """
    Generate styled info box HTML.
    
    Args:
        message: Message text
        box_type: Box type ('info', 'success', 'warning', 'error')
    
    Returns:
        str: HTML for info box
    
    Example:
        >>> html = style_info_box("Upload successful!", "success")
        >>> st.markdown(html, unsafe_allow_html=True)
    """
    colors = {
        'info': {'bg': '#d1ecf1', 'border': '#bee5eb', 'text': '#0c5460'},
        'success': {'bg': '#d4edda', 'border': '#c3e6cb', 'text': '#155724'},
        'warning': {'bg': '#fff3cd', 'border': '#ffeaa7', 'text': '#856404'},
        'error': {'bg': '#f8d7da', 'border': '#f5c6cb', 'text': '#721c24'}
    }
    
    color = colors.get(box_type, colors['info'])
    
    html = f"""
    <div style="
        background-color: {color['bg']};
        border: 1px solid {color['border']};
        color: {color['text']};
        padding: 0.75rem 1.25rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    ">
        {message}
    </div>
    """
    return html


def hide_streamlit_elements() -> None:
    """
    Hide default Streamlit UI elements (menu, footer).
    
    Example:
        >>> hide_streamlit_elements()
    """
    hide_css = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_css, unsafe_allow_html=True)


def apply_chat_message_style() -> None:
    """
    Apply custom styling for chat messages.
    
    Example:
        >>> apply_chat_message_style()
    """
    css = """
    <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .stChatMessage[data-testid="user"] {
            background-color: #e3f2fd;
        }
        
        .stChatMessage[data-testid="assistant"] {
            background-color: #f5f5f5;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def apply_sidebar_style() -> None:
    """
    Apply custom styling for sidebar.
    
    Example:
        >>> apply_sidebar_style()
    """
    css = """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }
        
        [data-testid="stSidebar"] .stButton>button {
            width: 100%;
            margin: 0.25rem 0;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Convenience: Allow direct import
__all__ = [
    'LIGHT_THEME',
    'DARK_THEME',
    'apply_theme',
    'apply_inline_theme',
    'get_theme_icon',
    'inject_custom_css',
    'load_theme_from_config',
    'style_metric_card',
    'style_info_box',
    'hide_streamlit_elements',
    'apply_chat_message_style',
    'apply_sidebar_style',
]
