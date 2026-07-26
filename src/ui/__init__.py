"""
UI Package

This package provides the Streamlit user interface components.

Modules:
- theme: Theme management and styling
- components: Reusable UI components (buttons, inputs, cards)
- sidebar: Navigation sidebar
- chat: Chat interface
- admin_panel: Document management and system stats
- settings_panel: Configuration (LLM, RAG, UI)

Author: TechFlow Solutions Project
License: MIT
"""

from .theme import (
    LIGHT_THEME,
    DARK_THEME,
    apply_theme,
    get_theme_icon,
    load_theme_from_config,
    hide_streamlit_elements,
    apply_chat_message_style,
    apply_sidebar_style
)

from .components import (
    render_header,
    render_metric_card,
    render_info_message,
    render_file_uploader,
    render_text_input,
    render_text_area,
    render_button,
    render_select_box,
    render_slider,
    render_number_input,
    render_checkbox,
    render_expander,
    render_spinner,
    render_progress_bar,
    render_tabs,
    render_columns,
    render_empty_state,
    render_data_table
)

from .sidebar import (
    render_sidebar,
    render_user_info,
    render_theme_toggle,
    render_admin_sidebar,
    render_compact_sidebar,
    get_navigation_state,
    set_navigation_state,
    render_quick_stats
)

from .chat import (
    render_chat_page,
    render_chat_with_controls,
    render_chat_controls,
    render_chat_info_panel,
    clear_chat_history,
    export_chat_history,
    get_chat_statistics
)

from .admin_panel import (
    render_admin_panel,
    render_dashboard_tab,
    render_documents_tab,
    render_indexing_tab,
    render_testing_tab
)

from .settings_panel import (
    render_settings_panel,
    render_llm_settings_tab,
    render_rag_settings_tab,
    render_ui_settings_tab,
    render_configuration_tab
)


__all__ = [
    # Theme
    'LIGHT_THEME',
    'DARK_THEME',
    'apply_theme',
    'get_theme_icon',
    'load_theme_from_config',
    'hide_streamlit_elements',
    'apply_chat_message_style',
    'apply_sidebar_style',
    
    # Components
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
    
    # Sidebar
    'render_sidebar',
    'render_user_info',
    'render_theme_toggle',
    'render_admin_sidebar',
    'render_compact_sidebar',
    'get_navigation_state',
    'set_navigation_state',
    'render_quick_stats',
    
    # Chat
    'render_chat_page',
    'render_chat_with_controls',
    'render_chat_controls',
    'render_chat_info_panel',
    'clear_chat_history',
    'export_chat_history',
    'get_chat_statistics',
    
    # Admin Panel
    'render_admin_panel',
    'render_dashboard_tab',
    'render_documents_tab',
    'render_indexing_tab',
    'render_testing_tab',
    
    # Settings Panel
    'render_settings_panel',
    'render_llm_settings_tab',
    'render_rag_settings_tab',
    'render_ui_settings_tab',
    'render_configuration_tab',
]
