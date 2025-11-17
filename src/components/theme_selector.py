"""
Theme Selector Component
Seletor de temas com preview
"""

from reactpy import component, html, use_state
from utils.theme_manager import get_theme_manager


@component
def theme_selector(on_theme_change=None):
    """
    Seletor de tema com preview visual

    Args:
        on_theme_change: Callback ao mudar tema (recebe theme_name)
    """
    theme_manager = get_theme_manager()
    current_theme, set_current_theme = use_state(theme_manager.current_theme)

    def change_theme(theme_name: str):
        theme_manager.set_theme(theme_name)
        set_current_theme(theme_name)
        if on_theme_change:
            on_theme_change(theme_name)

    themes = theme_manager.get_all_themes()

    return html.div(
        {
            "class": "theme-selector",
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
            }
        },

        # Header
        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.75rem",
                    "marginBottom": "1.5rem",
                }
            },
            html.span({"style": {"fontSize": "1.5rem"}}, "🎨"),
            html.h3(
                {
                    "style": {
                        "margin": "0",
                        "fontSize": "1.25rem",
                        "fontWeight": "600",
                    }
                },
                "Selecione o Tema"
            )
        ),

        # Theme Grid
        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fill, minmax(150px, 1fr))",
                    "gap": "1rem",
                }
            },

            *[
                html.button(
                    {
                        "key": theme.name,
                        "onClick": lambda e, tn=theme.name: change_theme(tn),
                        "style": {
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "center",
                            "gap": "0.75rem",
                            "padding": "1rem",
                            "border": f"3px solid {theme.colors['primary']}" if current_theme == theme.name else "2px solid var(--color-border-light)",
                            "borderRadius": "0.75rem",
                            "background": "var(--color-bg-secondary)",
                            "cursor": "pointer",
                            "transition": "all 0.2s",
                            "position": "relative",
                        }
                    },

                    # Checkmark for active theme
                    html.div(
                        {
                            "style": {
                                "position": "absolute",
                                "top": "0.5rem",
                                "right": "0.5rem",
                                "width": "1.5rem",
                                "height": "1.5rem",
                                "background": theme.colors['primary'],
                                "borderRadius": "50%",
                                "display": "flex" if current_theme == theme.name else "none",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "color": "white",
                                "fontSize": "0.75rem",
                            }
                        },
                        "✓"
                    ) if current_theme == theme.name else None,

                    # Icon
                    html.div(
                        {"style": {"fontSize": "2rem"}},
                        theme.icon
                    ),

                    # Name
                    html.div(
                        {
                            "style": {
                                "fontWeight": "600",
                                "fontSize": "0.875rem",
                                "color": "var(--color-text-primary)",
                            }
                        },
                        theme.display_name
                    ),

                    # Color Preview
                    html.div(
                        {
                            "style": {
                                "display": "flex",
                                "gap": "0.25rem",
                                "marginTop": "0.5rem",
                            }
                        },
                        html.div({
                            "style": {
                                "width": "1.5rem",
                                "height": "1.5rem",
                                "borderRadius": "0.25rem",
                                "background": theme.colors['primary'],
                            }
                        }),
                        html.div({
                            "style": {
                                "width": "1.5rem",
                                "height": "1.5rem",
                                "borderRadius": "0.25rem",
                                "background": theme.colors['bg_secondary'],
                                "border": "1px solid var(--color-border-light)",
                            }
                        }),
                        html.div({
                            "style": {
                                "width": "1.5rem",
                                "height": "1.5rem",
                                "borderRadius": "0.25rem",
                                "background": theme.colors['text_primary'],
                            }
                        }),
                    )
                )
                for theme in themes.values()
            ]
        ),

        # Current Theme Info
        html.div(
            {
                "style": {
                    "marginTop": "1.5rem",
                    "padding": "1rem",
                    "background": "var(--color-bg-secondary)",
                    "borderRadius": "0.5rem",
                    "border_left": "4px solid var(--color-primary)",
                }
            },
            html.div(
                {
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "0.5rem",
                        "fontSize": "0.875rem",
                        "color": "var(--color-text-secondary)",
                    }
                },
                html.span("💡"),
                html.span(f"Tema atual: "),
                html.strong(
                    {"style": {"color": "var(--color-text-primary)"}},
                    themes[current_theme].display_name
                )
            )
        )
    )


@component
def theme_toggle_button(on_theme_change=None):
    """
    Botão simples de toggle dark/light

    Args:
        on_theme_change: Callback ao mudar tema
    """
    theme_manager = get_theme_manager()
    is_dark, set_is_dark = use_state(theme_manager.current_theme == "dark")

    def toggle():
        new_theme = "dark" if not is_dark else "light"
        theme_manager.set_theme(new_theme)
        set_is_dark(not is_dark)
        if on_theme_change:
            on_theme_change(new_theme)

    return html.button(
        {
            "onClick": lambda e: toggle(),
            "class": "btn btn-ghost",
            "style": {
                "padding": "0.75rem",
                "borderRadius": "0.5rem",
                "fontSize": "1.25rem",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "width": "3rem",
                "height": "3rem",
            },
            "title": "Alternar tema"
        },
        "🌙" if is_dark else "☀️"
    )


@component
def theme_preview_card():
    """Card de preview do tema atual"""
    theme_manager = get_theme_manager()
    current_theme = theme_manager.get_current_theme()

    return html.div(
        {
            "class": "card",
            "style": {
                "background": "white",
                "padding": "1.5rem",
                "borderRadius": "1rem",
                "boxShadow": "var(--shadow-sm)",
            }
        },

        html.div(
            {
                "style": {
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.75rem",
                    "marginBottom": "1rem",
                }
            },
            html.span({"style": {"fontSize": "2rem"}}, current_theme.icon),
            html.h4(
                {"style": {"margin": "0", "fontSize": "1.25rem"}},
                current_theme.display_name
            )
        ),

        html.div(
            {
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, 1fr)",
                    "gap": "0.75rem",
                }
            },

            *[
                html.div(
                    {
                        "style": {
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "0.25rem",
                        }
                    },
                    html.div(
                        {
                            "style": {
                                "fontSize": "0.75rem",
                                "color": "var(--color-text-tertiary)",
                                "textTransform": "uppercase",
                                "letterSpacing": "0.05em",
                            }
                        },
                        key.replace("_", " ").title()
                    ),
                    html.div(
                        {
                            "style": {
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "0.5rem",
                            }
                        },
                        html.div({
                            "style": {
                                "width": "2rem",
                                "height": "2rem",
                                "borderRadius": "0.375rem",
                                "background": value,
                                "border": "1px solid var(--color-border-light)",
                            }
                        }),
                        html.span(
                            {
                                "style": {
                                    "fontSize": "0.75rem",
                                    "fontFamily": "monospace",
                                    "color": "var(--color-text-secondary)",
                                }
                            },
                            value
                        )
                    )
                )
                for key, value in list(current_theme.colors.items())[:4]
            ]
        )
    )
