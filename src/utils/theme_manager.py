"""
Theme Manager - Sistema de Temas Customizável
Gerenciamento de temas light/dark e temas personalizados
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class Theme:
    """Definição de um tema"""
    name: str
    colors: Dict[str, str]
    display_name: str
    icon: str = "🎨"


class ThemeManager:
    """Gerenciador de temas"""

    THEMES = {
        "light": Theme(
            name="light",
            display_name="Light",
            icon="☀️",
            colors={
                # Primary
                "primary": "#4F46E5",
                "primary_hover": "#4338CA",
                "primary_light": "#6366F1",
                "primary_dark": "#3730A3",

                # Text
                "text_primary": "#111827",
                "text_secondary": "#6B7280",
                "text_tertiary": "#9CA3AF",

                # Background
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#F9FAFB",
                "bg_tertiary": "#F3F4F6",

                # Border
                "border_light": "#E5E7EB",
                "border_medium": "#D1D5DB",
            }
        ),

        "dark": Theme(
            name="dark",
            display_name="Dark",
            icon="🌙",
            colors={
                # Primary
                "primary": "#6366F1",
                "primary_hover": "#818CF8",
                "primary_light": "#A5B4FC",
                "primary_dark": "#4F46E5",

                # Text
                "text_primary": "#F9FAFB",
                "text_secondary": "#D1D5DB",
                "text_tertiary": "#9CA3AF",

                # Background
                "bg_primary": "#111827",
                "bg_secondary": "#1F2937",
                "bg_tertiary": "#374151",

                # Border
                "border_light": "#374151",
                "border_medium": "#4B5563",
            }
        ),

        "purple": Theme(
            name="purple",
            display_name="Purple Dream",
            icon="💜",
            colors={
                # Primary
                "primary": "#9333EA",
                "primary_hover": "#7E22CE",
                "primary_light": "#A855F7",
                "primary_dark": "#6B21A8",

                # Text
                "text_primary": "#111827",
                "text_secondary": "#6B7280",
                "text_tertiary": "#9CA3AF",

                # Background
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#FAF5FF",
                "bg_tertiary": "#F3E8FF",

                # Border
                "border_light": "#E9D5FF",
                "border_medium": "#D8B4FE",
            }
        ),

        "ocean": Theme(
            name="ocean",
            display_name="Ocean Blue",
            icon="🌊",
            colors={
                # Primary
                "primary": "#0EA5E9",
                "primary_hover": "#0284C7",
                "primary_light": "#38BDF8",
                "primary_dark": "#0369A1",

                # Text
                "text_primary": "#111827",
                "text_secondary": "#6B7280",
                "text_tertiary": "#9CA3AF",

                # Background
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#F0F9FF",
                "bg_tertiary": "#E0F2FE",

                # Border
                "border_light": "#BAE6FD",
                "border_medium": "#7DD3FC",
            }
        ),

        "forest": Theme(
            name="forest",
            display_name="Forest Green",
            icon="🌲",
            colors={
                # Primary
                "primary": "#059669",
                "primary_hover": "#047857",
                "primary_light": "#10B981",
                "primary_dark": "#065F46",

                # Text
                "text_primary": "#111827",
                "text_secondary": "#6B7280",
                "text_tertiary": "#9CA3AF",

                # Background
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#F0FDF4",
                "bg_tertiary": "#DCFCE7",

                # Border
                "border_light": "#BBF7D0",
                "border_medium": "#86EFAC",
            }
        ),

        "sunset": Theme(
            name="sunset",
            display_name="Sunset Orange",
            icon="🌅",
            colors={
                # Primary
                "primary": "#F97316",
                "primary_hover": "#EA580C",
                "primary_light": "#FB923C",
                "primary_dark": "#C2410C",

                # Text
                "text_primary": "#111827",
                "text_secondary": "#6B7280",
                "text_tertiary": "#9CA3AF",

                # Background
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#FFF7ED",
                "bg_tertiary": "#FFEDD5",

                # Border
                "border_light": "#FED7AA",
                "border_medium": "#FDBA74",
            }
        ),
    }

    def __init__(self):
        self.current_theme = "light"

    def get_theme(self, theme_name: str) -> Optional[Theme]:
        """Obtém um tema pelo nome"""
        return self.THEMES.get(theme_name)

    def get_all_themes(self) -> Dict[str, Theme]:
        """Retorna todos os temas disponíveis"""
        return self.THEMES

    def set_theme(self, theme_name: str):
        """Define o tema atual"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            return True
        return False

    def get_current_theme(self) -> Theme:
        """Retorna o tema atual"""
        return self.THEMES[self.current_theme]

    def generate_css_variables(self, theme_name: str) -> str:
        """Gera CSS variables para um tema"""
        theme = self.get_theme(theme_name)
        if not theme:
            return ""

        css_vars = [":root {"]
        for key, value in theme.colors.items():
            css_var_name = f"--color-{key.replace('_', '-')}"
            css_vars.append(f"  {css_var_name}: {value};")
        css_vars.append("}")

        return "\n".join(css_vars)

    def get_inline_styles(self, theme_name: str) -> Dict[str, str]:
        """Retorna estilos inline para um tema"""
        theme = self.get_theme(theme_name)
        if not theme:
            return {}

        return {
            f"--color-{key.replace('_', '-')}": value
            for key, value in theme.colors.items()
        }


# Singleton instance
_theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    """Obtém a instância singleton do ThemeManager"""
    return _theme_manager
