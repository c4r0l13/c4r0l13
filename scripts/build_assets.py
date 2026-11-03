"""Generate the SVG artwork for the profile README (light and dark versions).

Run from the repository root:  python scripts/build_assets.py
Everything is plain SVG (no external fonts, scripts or services), so GitHub renders it reliably.
"""

from __future__ import annotations

import textwrap
from html import escape
from pathlib import Path

OUT = Path("assets")
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117", "card": "#161b22", "card2": "#1c2330", "border": "#30363d", "text": "#e6edf3",
        "muted": "#9198a1", "faint": "#21262d",
        "genai": "#a78bfa", "risk": "#2dd4bf", "science": "#fbbf24", "accent": "#60a5fa", "hot": "#fb7185",
    },
    "light": {
        "bg": "#ffffff", "card": "#f6f8fa", "card2": "#eef1f5", "border": "#d0d7de", "text": "#1f2328",
        "muted": "#59636e", "faint": "#eaeef2",
        "genai": "#6d28d9", "risk": "#0f766e", "science": "#b45309", "accent": "#1d4ed8", "hot": "#be123c",
    },
}  # fmt: skip


def width_of(text: str, size: float, bold: bool = False) -> float:
    """Rough text width for a sans-serif system font (no font metrics available in SVG-as-image)."""
    per = 0.60 if bold else 0.54
    narrow = sum(text.count(c) for c in "ilI.,:;|' ")
    wide = sum(text.count(c) for c in "MWmw%")
    return size * (per * len(text) - 0.25 * narrow + 0.25 * wide)


def t(x, y, text, size, fill, weight=400, anchor="start", family=FONT, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(text)}</text>')  # fmt: skip


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>\n')  # fmt: skip


def pill(x, y, text, color, c, size=17, filled=False):
    w = width_of(text, size) * 1.06 + 28
    bg = color if filled else c["card2"]
    fg = c["bg"] if filled else c["text"]
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 16}" rx="{(size + 16) / 2}" fill="{bg}" '
            f'stroke="{color}" stroke-opacity="0.55"/>' + t(x + 13, y + size + 3, text, size, fg, 500)), w


# ---------------------------------------------------------------- header
def header(c) -> str:
    W, H = 1200, 340
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>']
    b.append('<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
             f'<circle cx="2" cy="2" r="1.3" fill="{c["border"]}"/></pattern>'
             f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{c["genai"]}"/>'
             f'<stop offset="0.5" stop-color="{c["risk"]}"/><stop offset="1" stop-color="{c["science"]}"/>'
             '</linearGradient></defs>')  # fmt: skip
    b.append(f'<rect x="700" y="1" width="499" height="{H - 2}" rx="18" fill="url(#dots)" opacity="0.7"/>')
    # Network / molecule motif: data, chemistry and agents connected.
    nodes = {
        "a": (790, 92, "genai"), "b": (905, 64, "risk"), "c": (1040, 104, "science"), "d": (860, 178, "accent"),
        "e": (990, 205, "genai"), "f": (1110, 196, "risk"), "g": (775, 262, "science"), "h": (930, 285, "risk"),
        "i": (1080, 285, "accent"),
    }  # fmt: skip
    edges = ["ab", "bc", "ad", "bd", "de", "ce", "cf", "ef", "dg", "dh", "eh", "ei", "fi", "gh", "hi"]
    for k, (u, v) in enumerate(edges):
        (x1, y1, _), (x2, y2, _) = nodes[u], nodes[v]
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["muted"]}" stroke-opacity="0.45" '
                 f'stroke-width="1.6"/>')  # fmt: skip
        if k % 3 == 0:  # packets travelling along some edges
            b.append(f'<circle r="3.5" fill="{c[nodes[u][2]]}"><animateMotion dur="{3 + k % 4}s" '
                     f'repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/></circle>')  # fmt: skip
    for k, (x, y, col) in enumerate(nodes.values()):
        r = 13 if k % 2 == 0 else 10
        b.append(f'<circle cx="{x}" cy="{y}" r="{r + 9}" fill="{c[col]}" opacity="0.14">'
                 f'<animate attributeName="r" values="{r + 4};{r + 14};{r + 4}" dur="{3 + k % 3}s" '
                 f'repeatCount="indefinite"/></circle>')  # fmt: skip
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["card"]}" stroke="{c[col]}" stroke-width="3"/>')
    for (x, y, _), label in zip([nodes["a"], nodes["c"], nodes["h"]], ["LLM", "CO₂", "f(x)"], strict=True):
        b.append(t(x, y - 24, label, 15, c["muted"], 600, "middle", MONO))
    # Text block
    b.append(t(60, 70, "HOLA, SOY", 18, c["muted"], 600, extra='letter-spacing="3"'))
    b.append(t(58, 132, "Carolina Lievanos", 60, c["text"], 700))
    b.append(f'<rect x="60" y="150" width="300" height="5" rx="2.5" fill="url(#bar)"/>')
    b.append(t(60, 196, "Científica de datos  ·  IA generativa  ·  Machine learning", 26, c["text"], 500))
    b.append(t(60, 232, "MSc. en Ingeniería Química. Construyo modelos y agentes que se", 19, c["muted"]))
    b.append(t(60, 258, "pueden auditar: calibrados, reproducibles y evaluados con rigor.", 19, c["muted"]))
    x = 60
    for label, col in (("Machine learning", "risk"), ("RAG y agentes", "genai"), ("Catálisis y laboratorio", "science")):
        p, w = pill(x, 282, label, c[col], c, 16)
        b.append(p)
        x += w + 12
    return svg(W, H, "".join(b), "Carolina Lievanos — Científica de datos, IA generativa, machine learning")


# ---------------------------------------------------------------- impact tiles
IMPACT = [
    ("13% → 63%", "evidencia correcta en el top 5", "RAG sobre 84 reportes de la SEC", "genai"),
    ("73% vs 31%", "de los mejores catalizadores en 60 pruebas", "aprendizaje activo vs al azar", "science"),
    ("−88%", "costo total del fraude", "umbral de alertas elegido por costo", "risk"),
    ("+5 / 100", "solicitantes aprobados con el mismo riesgo", "scoring monótono, calibrado y auditado", "risk"),
    ("82%", "de errores de transcripción detectados, sin falsas alarmas", "copiloto de reportes de laboratorio", "genai"),
    ("0.3%", "de falsas alarmas al detectar fallas", "proceso químico Tennessee Eastman", "science"),
]


def impact(c) -> str:
    W, H = 1200, 470
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>']
    b.append(t(40, 52, "IMPACTO MEDIDO", 17, c["muted"], 700, extra='letter-spacing="3"'))
    b.append(t(1160, 52, "cada número sale de un repositorio reproducible", 16, c["muted"], 400, "end"))
    tw, th, gap = 360, 175, 20
    for k, (num, what, where, col) in enumerate(IMPACT):
        x, y = 40 + (k % 3) * (tw + gap), 80 + (k // 3) * (th + gap)
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="{c["card"]}" stroke="{c["border"]}"/>')
        b.append(f'<rect x="{x}" y="{y + 18}" width="4" height="{th - 36}" rx="2" fill="{c[col]}"/>')
        b.append(t(x + 26, y + 64, num, 44, c[col], 700))
        for i, line in enumerate(textwrap.wrap(what, 36)[:2]):
            b.append(t(x + 26, y + 98 + i * 22, line, 18, c["text"], 500))
        b.append(t(x + 26, y + th - 16, where, 14.5, c["muted"]))
    return svg(W, H, "".join(b), "Impacto medido en los proyectos")


# ---------------------------------------------------------------- journey
STAGES = [
    ("01", "Investigación química", "science",
     ["Maestría en Ingeniería Química (UAM)", "en catálisis ambiental y materiales;", "I+D en transición energética."]),
    ("02", "Laboratorios y LIMS", "accent",
     ["Consultora certificada de LIMS/ELN:", "implementación y automatización", "para laboratorios en América Latina."]),
    ("03", "Ciencia de datos e IA", "genai",
     ["Machine learning, series de tiempo,", "RAG y agentes con herramientas,", "evaluados con rigor y reproducibles."]),
]  # fmt: skip


def journey(c) -> str:
    W, H = 1200, 250
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>']
    b.append(t(40, 50, "TRAYECTORIA", 17, c["muted"], 700, extra='letter-spacing="3"'))
    cw, gap = 348, 38
    for k, (num, title, col, lines) in enumerate(STAGES):
        x, y = 40 + k * (cw + gap), 72
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="150" rx="14" fill="{c["card"]}" stroke="{c["border"]}"/>')
        b.append(t(x + 22, y + 44, num, 30, c[col], 700, family=MONO))
        b.append(t(x + 78, y + 42, title, 22, c["text"], 700))
        for i, line in enumerate(lines):
            b.append(t(x + 22, y + 78 + i * 24, line, 17, c["muted"]))
        if k < len(STAGES) - 1:
            ax = x + cw + 6
            b.append(f'<path d="M{ax} {y + 75} l{gap - 14} 0 m-9 -8 l9 8 l-9 8" fill="none" stroke="{c["muted"]}" '
                     f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')  # fmt: skip
    return svg(W, H, "".join(b), "Trayectoria: química, laboratorios y LIMS, ciencia de datos e IA")


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("financial-rag-eval", "RAG financiero evaluado", "genai", "13%→63%", "evidencia correcta en el top 5",
     "Preguntas sobre 84 reportes de la SEC: filtros por empresa y año y reescritura de consultas.",
     ["RAG", "BM25", "Claude"]),
    ("lab-report-copilot", "Copiloto de laboratorio", "genai", "82%", "errores detectados, 0 falsas alarmas",
     "De PDF a registro LIMS validado: Claude, reglas de dominio y un ciclo de reparación.",
     ["Claude", "LIMS", "PDF"]),
    ("payments-agent-eval", "Agente de pagos evaluado", "genai", "pass^k", "17 escenarios, 5 ataques",
     "Clientes simulados, ingeniería social e inyección de instrucciones en los datos.",
     ["Agentes", "Tool use", "Seguridad"]),
    ("credit-risk-scorecard", "Credit scoring explicable", "risk", "+5/100", "aprobados con el mismo riesgo",
     "Scorecard WoE vs LightGBM monótono, calibración, equidad y razones de rechazo.",
     ["LightGBM", "SHAP", "Equidad"]),
    ("credit-risk-api", "API de riesgo de crédito", "risk", "PSI", "monitoreo de drift en producción",
     "Decisión con razones, validación de entrada, métricas Prometheus y controles en CI.",
     ["FastAPI", "Docker", "MLOps"]),
    ("fraud-detection", "Detección de fraude", "risk", "−88%", "costo vs no filtrar",
     "Variables de comportamiento sin fuga, validación temporal y umbral por costo.",
     ["LightGBM", "MLflow", "Costo"]),
    ("usdmxn-volatility-var", "Volatilidad y VaR USD/MXN", "risk", "1 de 5", "métodos de VaR pasa las pruebas",
     "Desde 1996: pronóstico de tipo de cambio, GARCH y backtesting regulatorio del VaR.",
     ["GARCH", "VaR", "Series"]),
    ("co2-catalyst-discovery", "Catalizadores para CO₂", "science", "73% vs 31%", "mejores encontrados en 60 pruebas",
     "179 catalizadores probados en laboratorio: DFT vs experimento y laboratorio autónomo.",
     ["Active learning", "DFT", "Catálisis"]),
    ("tep-fault-detection", "Fallas en procesos químicos", "science", "0.3%", "falsas alarmas",
     "Tennessee Eastman: cartas PCA/DPCA, análisis de contribución y diagnóstico con LightGBM.",
     ["PCA", "SPC", "Diagnóstico"]),
    ("cdmx-air-quality-forecasting", "Calidad del aire CDMX", "science", "0.90", "ROC-AUC, alerta a un día",
     "SQL sobre 2015–2023, efecto del confinamiento y pronóstico de PM2.5 y ozono.",
     ["SQL", "Series", "LightGBM"]),
    ("plant-disease-detection", "Enfermedades en hojas", "science", "94%", "exactitud en 38 clases",
     "Auditoría de atajos: el fondo de la foto delata la clase; cultivos nunca vistos.",
     ["TensorFlow", "FastAPI", "Visión"]),
    ("dog-adoption-analysis", "Adopción de perros", "science", "27% vs 85%", "adopción real vs Kaplan-Meier ingenuo",
     "9,750 perros de un refugio real: supervivencia y modelo sin fuga de datos.",
     ["Supervivencia", "LightGBM", "Fuga"]),
]  # fmt: skip
AREA = {"genai": "IA GENERATIVA", "risk": "FINANZAS Y RIESGO", "science": "CIENCIA E INGENIERÍA"}


def card(p, c) -> str:
    slug, title, col, metric, metric_label, desc, tags = p
    W, H = 600, 300
    b = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["card"]}" stroke="{c["border"]}"/>']
    b.append(f'<rect x="1" y="1" width="{W - 2}" height="6" rx="3" fill="{c[col]}"/>')
    b.append(t(28, 44, AREA[col], 14, c[col], 700, extra='letter-spacing="2"'))
    b.append(t(W - 28, 44, "↗", 20, c["muted"], 400, "end"))
    b.append(t(28, 82, title, 30, c["text"], 700))
    b.append(t(28, 140, metric, 46, c[col], 700))
    b.append(t(28, 168, metric_label, 18, c["muted"], 500))
    for i, line in enumerate(textwrap.wrap(desc, 56)[:2]):
        b.append(t(28, 206 + i * 24, line, 18, c["text"], 400))
    x = 28
    for tag in tags:
        pl, w = pill(x, 250, tag, c[col], c, 15)
        b.append(pl)
        x += w + 10
    return svg(W, H, "".join(b), f"{title}: {metric} {metric_label}")


# ---------------------------------------------------------------- stack
STACK = [
    ("IA generativa", "genai", ["Claude / OpenAI APIs", "RAG", "Agentes con herramientas", "Evaluación de LLMs",
                                "Extracción estructurada"]),
    ("Machine learning", "risk", ["scikit-learn", "LightGBM", "SHAP", "Series de tiempo", "Supervivencia",
                                  "Active learning"]),
    ("MLOps", "accent", ["FastAPI", "Docker", "GitHub Actions", "MLflow", "Prometheus", "pytest"]),
    ("Datos y BI", "science", ["Python", "SQL", "R", "pandas", "Power BI", "Tableau", "KNIME"]),
    ("Laboratorio", "hot", ["LIMS / ELN", "Catálisis", "Electroquímica", "Control estadístico", "Mathematica"]),
]  # fmt: skip


def stack(c) -> str:
    W, H = 1200, 70 + len(STACK) * 58 + 10
    b = [f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}"/>']
    b.append(t(40, 50, "HERRAMIENTAS", 17, c["muted"], 700, extra='letter-spacing="3"'))
    for k, (area, col, items) in enumerate(STACK):
        y = 74 + k * 58
        b.append(f'<circle cx="48" cy="{y + 17}" r="6" fill="{c[col]}"/>')
        b.append(t(64, y + 24, area, 19, c["text"], 700))
        x = 260
        for item in items:
            pl, w = pill(x, y, item, c[col], c, 16)
            b.append(pl)
            x += w + 10
    return svg(W, H, "".join(b), "Herramientas")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, c in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(c), encoding="utf-8")
        (OUT / f"impact-{name}.svg").write_text(impact(c), encoding="utf-8")
        (OUT / f"journey-{name}.svg").write_text(journey(c), encoding="utf-8")
        (OUT / f"stack-{name}.svg").write_text(stack(c), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f"card-{p[0]}-{name}.svg").write_text(card(p, c), encoding="utf-8")
    print(f"{len(list(OUT.glob('*.svg')))} SVG files in {OUT}/")


if __name__ == "__main__":
    main()
