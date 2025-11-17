"""
SVG Illustrations & Icons
Ilustrações e ícones SVG customizados
"""

from reactpy import component, svg, html


@component
def empty_state_illustration(width: str = "200px", height: str = "200px"):
    """Ilustração de estado vazio"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 200 200",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
            "style": {"opacity": "0.6"}
        },
        # Document
        svg.path({
            "d": "M60 40h80v120H60z",
            "fill": "#E5E7EB",
            "stroke": "#9CA3AF",
            "strokeWidth": "2"
        }),
        # Lines
        svg.line({"x1": "70", "y1": "60", "x2": "130", "y2": "60", "stroke": "#9CA3AF", "strokeWidth": "2"}),
        svg.line({"x1": "70", "y1": "80", "x2": "130", "y2": "80", "stroke": "#9CA3AF", "strokeWidth": "2"}),
        svg.line({"x1": "70", "y1": "100", "x2": "110", "y2": "100", "stroke": "#9CA3AF", "strokeWidth": "2"}),
        # Sad face
        svg.circle({"cx": "90", "cy": "130", "r": "3", "fill": "#9CA3AF"}),
        svg.circle({"cx": "110", "cy": "130", "r": "3", "fill": "#9CA3AF"}),
        svg.path({"d": "M85 145Q100 140 115 145", "stroke": "#9CA3AF", "strokeWidth": "2", "fill": "none"})
    )


@component
def loading_illustration(width: str = "100px", height: str = "100px"):
    """Ilustração de loading animada"""
    # Generate unique ID for this instance
    spinner_id = f"spinner-{id(width)}"

    return html.div(
        html.style(
            f"""
            @keyframes spin-{spinner_id} {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            .spinner-{spinner_id} {{
                animation: spin-{spinner_id} 1s linear infinite;
                display: inline-block;
            }}
            """
        ),
        svg.svg(
            {
                "width": width,
                "height": height,
                "viewBox": "0 0 100 100",
                "xmlns": "http://www.w3.org/2000/svg",
                "className": f"spinner-{spinner_id}",
            },
            svg.circle(
                {
                    "cx": "50",
                    "cy": "50",
                    "r": "35",
                    "stroke": "#4F46E5",
                    "strokeWidth": "8",
                    "fill": "none",
                    "strokeDasharray": "164",
                    "stroke_dashoffset": "41",
                    "strokeLinecap": "round",
                }
            )
        )
    )


@component
def success_illustration(width: str = "150px", height: str = "150px"):
    """Ilustração de sucesso"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 150 150",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Circle background
        svg.circle({
            "cx": "75",
            "cy": "75",
            "r": "60",
            "fill": "#D1FAE5"
        }),
        # Checkmark
        svg.path({
            "d": "M50 75L65 90L100 55",
            "stroke": "#10B981",
            "strokeWidth": "8",
            "strokeLinecap": "round",
            "strokeLinejoin": "round"
        })
    )


@component
def error_illustration(width: str = "150px", height: str = "150px"):
    """Ilustração de erro"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 150 150",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Circle background
        svg.circle({
            "cx": "75",
            "cy": "75",
            "r": "60",
            "fill": "#FEE2E2"
        }),
        # X mark
        svg.path({
            "d": "M55 55L95 95M95 55L55 95",
            "stroke": "#EF4444",
            "strokeWidth": "8",
            "strokeLinecap": "round"
        })
    )


@component
def chart_illustration(width: str = "200px", height: str = "200px"):
    """Ilustração de gráfico"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 200 200",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Bars
        svg.rect({"x": "40", "y": "120", "width": "30", "height": "50", "fill": "#4F46E5", "rx": "4"}),
        svg.rect({"x": "80", "y": "90", "width": "30", "height": "80", "fill": "#10B981", "rx": "4"}),
        svg.rect({"x": "120", "y": "70", "width": "30", "height": "100", "fill": "#F59E0B", "rx": "4"}),
        svg.rect({"x": "160", "y": "100", "width": "30", "height": "70", "fill": "#EF4444", "rx": "4"}),
        # Axis
        svg.line({"x1": "30", "y1": "170", "x2": "200", "y2": "170", "stroke": "#9CA3AF", "strokeWidth": "2"}),
        svg.line({"x1": "30", "y1": "30", "x2": "30", "y2": "170", "stroke": "#9CA3AF", "strokeWidth": "2"})
    )


@component
def fund_icon(width: str = "60px", height: str = "60px", color: str = "#4F46E5"):
    """Ícone de fundo de investimento"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 60 60",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Building
        svg.rect({"x": "15", "y": "20", "width": "30", "height": "35", "fill": color, "rx": "2"}),
        # Windows
        svg.rect({"x": "20", "y": "25", "width": "6", "height": "6", "fill": "white", "rx": "1"}),
        svg.rect({"x": "34", "y": "25", "width": "6", "height": "6", "fill": "white", "rx": "1"}),
        svg.rect({"x": "20", "y": "35", "width": "6", "height": "6", "fill": "white", "rx": "1"}),
        svg.rect({"x": "34", "y": "35", "width": "6", "height": "6", "fill": "white", "rx": "1"}),
        # Door
        svg.rect({"x": "25", "y": "45", "width": "10", "height": "10", "fill": "white", "rx": "1"})
    )


@component
def money_icon(width: str = "60px", height: str = "60px", color: str = "#10B981"):
    """Ícone de dinheiro"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 60 60",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Coin
        svg.circle({"cx": "30", "cy": "30", "r": "20", "fill": color}),
        # $ Symbol
        svg.text(
            {
                "x": "30",
                "y": "38",
                "fontSize": "24",
                "fontWeight": "bold",
                "fill": "white",
                "text_anchor": "middle"
            },
            "$"
        )
    )


@component
def trending_up_icon(width: str = "60px", height: str = "60px", color: str = "#10B981"):
    """Ícone de tendência alta"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 60 60",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Line
        svg.path({
            "d": "M10 45L25 30L35 35L50 15",
            "stroke": color,
            "strokeWidth": "4",
            "strokeLinecap": "round",
            "strokeLinejoin": "round"
        }),
        # Arrow
        svg.path({
            "d": "M40 15H50V25",
            "stroke": color,
            "strokeWidth": "4",
            "strokeLinecap": "round",
            "strokeLinejoin": "round"
        })
    )


@component
def trending_down_icon(width: str = "60px", height: str = "60px", color: str = "#EF4444"):
    """Ícone de tendência baixa"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 60 60",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Line
        svg.path({
            "d": "M10 15L25 30L35 25L50 45",
            "stroke": color,
            "strokeWidth": "4",
            "strokeLinecap": "round",
            "strokeLinejoin": "round"
        }),
        # Arrow
        svg.path({
            "d": "M40 45H50V35",
            "stroke": color,
            "strokeWidth": "4",
            "strokeLinecap": "round",
            "strokeLinejoin": "round"
        })
    )


@component
def document_icon(width: str = "60px", height: str = "60px", color: str = "#3B82F6"):
    """Ícone de documento"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 60 60",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Document
        svg.path({
            "d": "M20 10h20l10 10v30H20z",
            "fill": color
        }),
        # Corner fold
        svg.path({
            "d": "M40 10v10h10",
            "fill": "white",
            "opacity": "0.3"
        }),
        # Lines
        svg.line({"x1": "25", "y1": "28", "x2": "45", "y2": "28", "stroke": "white", "strokeWidth": "2"}),
        svg.line({"x1": "25", "y1": "35", "x2": "45", "y2": "35", "stroke": "white", "strokeWidth": "2"}),
        svg.line({"x1": "25", "y1": "42", "x2": "38", "y2": "42", "stroke": "white", "strokeWidth": "2"})
    )


@component
def settings_icon(width: str = "60px", height: str = "60px", color: str = "#6B7280"):
    """Ícone de configurações"""
    return svg.svg(
        {
            "width": width,
            "height": height,
            "viewBox": "0 0 60 60",
            "fill": "none",
            "xmlns": "http://www.w3.org/2000/svg",
        },
        # Gear
        svg.circle({"cx": "30", "cy": "30", "r": "10", "fill": color}),
        svg.circle({"cx": "30", "cy": "30", "r": "5", "fill": "white"}),
        # Teeth
        *[
            svg.rect({
                "x": "28",
                "y": "15",
                "width": "4",
                "height": "5",
                "fill": color,
                "transform": f"rotate({angle} 30 30)"
            })
            for angle in [0, 60, 120, 180, 240, 300]
        ]
    )


@component
def decorative_background_pattern():
    """Padrão decorativo de fundo"""
    return svg.svg(
        {
            "style": {
                "position": "absolute",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "zIndex": "0",
                "opacity": "0.05",
                "pointer_events": "none"
            },
            "xmlns": "http://www.w3.org/2000/svg",
        },
        svg.defs(
            svg.pattern(
                {
                    "id": "pattern",
                    "x": "0",
                    "y": "0",
                    "width": "100",
                    "height": "100",
                    "patternUnits": "userSpaceOnUse"
                },
                svg.circle({"cx": "50", "cy": "50", "r": "2", "fill": "currentColor"}),
                svg.circle({"cx": "10", "cy": "10", "r": "1", "fill": "currentColor"}),
                svg.circle({"cx": "90", "cy": "10", "r": "1", "fill": "currentColor"}),
                svg.circle({"cx": "10", "cy": "90", "r": "1", "fill": "currentColor"}),
                svg.circle({"cx": "90", "cy": "90", "r": "1", "fill": "currentColor"})
            )
        ),
        svg.rect({"width": "100%", "height": "100%", "fill": "url(#pattern)"})
    )
