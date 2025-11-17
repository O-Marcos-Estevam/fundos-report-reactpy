"""
Teste simples do ReactPy para diagnosticar problema
"""
import sys
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from reactpy import component, html
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

@component
def hello_world():
    """Componente simples de teste"""
    return html.div(
        {"style": {"padding": "2rem", "fontFamily": "Arial"}},
        html.h1("ReactPy está funcionando!"),
        html.p("Se você vê esta mensagem, o ReactPy está renderizando corretamente."),
        html.button(
            {"onClick": lambda e: print("Botão clicado!")},
            "Clique aqui"
        )
    )

# Criar app FastAPI
app = FastAPI()

# Configurar ReactPy
configure(app, hello_world)

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Teste ReactPy")
    print("Acesse: http://localhost:8001")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
