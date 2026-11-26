#!/usr/bin/env python3
"""Генерация иллюстраций (эскизы, схемы) для отчёта по ИВЛ."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import matplotlib.patheffects as pe

OUT = Path(__file__).resolve().parent / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

# Сдержанная медицинская палитра (не «AI-purple»)
C_BG = "#F7F4EF"
C_BIO = "#2F6F5E"
C_TECH = "#2C4A6E"
C_ACCENT = "#B85C38"
C_LINE = "#333333"
C_SOFT = "#E6E0D6"
C_BOX = "#FFFFFF"
C_PORT = "#3D6B8C"
C_STAT = "#5A7A4A"


def style_ax(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(C_BG)


def box(ax, x, y, w, h, text, color, fontsize=8, text_color="white"):
    r = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.2, edgecolor=C_LINE, facecolor=color,
    )
    ax.add_patch(r)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fontsize,
        color=text_color, wrap=True,
        fontweight="medium",
    )
    return r


def arrow(ax, x1, y1, x2, y2, color=C_LINE):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=1.4),
    )


def fig_scheme_links():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=150)
    style_ax(ax)
    ax.set_ylim(0, 8)
    fig.patch.set_facecolor(C_BG)

    ax.text(5, 7.6, "Система «пациент — аппарат ИВЛ»", ha="center", fontsize=13, fontweight="bold", color=C_LINE)
    ax.text(2.3, 7.1, "Биологические звенья", ha="center", fontsize=10, color=C_BIO, fontweight="bold")
    ax.text(7.7, 7.1, "Технические звенья", ha="center", fontsize=10, color=C_TECH, fontweight="bold")

    bios = [
        (0.4, 5.9, "Дыхательный центр\n/ диафрагм. нерв"),
        (0.4, 4.6, "Дыхательные мышцы\nи грудная клетка"),
        (0.4, 3.3, "Дыхательные пути\n(мёртвое пространство)"),
        (0.4, 2.0, "Альвеолы\nгазообмен O₂/CO₂"),
        (0.4, 0.7, "Лёгочный кровоток\nV/Q, шунт"),
    ]
    techs = [
        (6.3, 5.9, "Триггер / контроллер\nSIMV · P-SIMV · PSV"),
        (6.3, 4.6, "Клапаны вдоха/выдоха\nPEEP"),
        (6.3, 3.3, "Датчики Paw, потока,\nFiO₂"),
        (6.3, 2.0, "Генератор потока\n(турбина / газ)"),
        (6.3, 0.7, "Монитор, тревоги,\nжурнал"),
    ]
    for x, y, t in bios:
        box(ax, x, y, 3.8, 1.0, t, C_BIO, fontsize=8)
    for x, y, t in techs:
        box(ax, x, y, 3.8, 1.0, t, C_TECH, fontsize=8)

    # Cross interactions
    arrow(ax, 4.3, 5.1, 6.2, 6.2, C_ACCENT)
    ax.text(5.2, 5.85, "попытка\nвдоха", fontsize=7, color=C_ACCENT, ha="center")
    arrow(ax, 6.3, 5.0, 4.3, 3.8, C_ACCENT)
    ax.text(5.5, 4.2, "поток/Paw", fontsize=7, color=C_ACCENT, ha="center")
    arrow(ax, 4.3, 2.5, 6.2, 1.2, C_ACCENT)
    ax.text(5.6, 1.7, "EtCO₂/SpO₂\nобратная связь", fontsize=7, color=C_ACCENT, ha="center")

    fig.tight_layout()
    fig.savefig(OUT / "scheme_links.png", facecolor=C_BG, bbox_inches="tight")
    plt.close(fig)


def fig_block_scheme():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.text(6, 6.6, "Структурная схема «РеспироПВ-2»", ha="center", fontsize=13, fontweight="bold")

    items = [
        (0.3, 4.8, 2.2, 1.1, "Источник\nO₂ / воздух\nили турбина", C_TECH),
        (2.9, 4.8, 2.2, 1.1, "Редуктор /\nblender FiO₂", C_TECH),
        (5.5, 4.8, 2.4, 1.1, "Блок управления\nSIMV / P-SIMV", C_ACCENT),
        (8.3, 4.8, 2.2, 1.1, "Нереверсивный\nклапан + ПДКВ", C_TECH),
        (10.5, 4.8, 1.3, 1.1, "Пациент", C_BIO),
        (5.5, 2.8, 2.4, 1.1, "Датчики\nPaw · поток · FiO₂", C_PORT),
        (5.5, 1.0, 2.4, 1.1, "UI / тревоги\nжурнал событий", C_PORT),
        (0.3, 2.8, 2.2, 1.1, "Питание\n220 В / АКБ", C_STAT),
        (8.3, 2.8, 2.2, 1.1, "Увлажнитель\nили HME", C_STAT),
    ]
    for x, y, w, h, t, c in items:
        box(ax, x, y, w, h, t, c, fontsize=7.5)

    for x1, x2 in [(2.5, 2.9), (5.1, 5.5), (7.9, 8.3), (10.5, 10.5)]:
        pass
    arrow(ax, 2.5, 5.35, 2.9, 5.35)
    arrow(ax, 5.1, 5.35, 5.5, 5.35)
    arrow(ax, 7.9, 5.35, 8.3, 5.35)
    arrow(ax, 10.5, 5.35, 10.5, 5.35)
    # last to patient
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35),
                arrowprops=dict(arrowstyle="->", color=C_LINE, lw=1.4))
    arrow(ax, 10.5, 5.35, 10.5, 5.35)
    # fix patient arrow from valve
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))
    arrow(ax, 10.5, 5.35, 10.5, 5.35)

    # redraw clean arrows
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))
    from matplotlib.patches import FancyArrow
    # Valve -> patient already has box at 10.5; need arrow from 10.5 left edge
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))

    # Feedback arrows
    ax.annotate("", xy=(6.7, 3.9), xytext=(6.7, 4.8),
                arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.3))
    ax.annotate("", xy=(6.7, 2.1), xytext=(6.7, 2.8),
                arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.3))
    ax.annotate("", xy=(2.5, 3.35), xytext=(5.5, 3.35),
                arrowprops=dict(arrowstyle="->", color=C_LINE, lw=1.2))
    ax.annotate("", xy=(8.3, 3.35), xytext=(7.9, 3.35),
                arrowprops=dict(arrowstyle="->", color=C_LINE, lw=1.2))
    # patient connection label
    ax.text(9.4, 6.1, "дыхательный контур", fontsize=8, color=C_LINE, style="italic")
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))
    # Explicit arrow valve->patient
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))
    ax.plot([10.5, 10.5], [5.35, 5.35])  # noop
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))

    # Proper arrow from valve right to patient left
    ax.annotate("", xy=(10.5, 5.35), xytext=(10.5, 5.35))
    ax.annotate(
        "", xy=(10.5, 5.35), xytext=(10.5, 5.35),
    )
    # coordinates: valve ends at 10.5, patient starts 10.5 — wait patient is at x=10.5 w=1.3
    # valve is 8.3..10.5 — overlaps! Fix layout in redraw - actually valve is 8.3+2.2=10.5, patient at 10.5
    # They're adjacent. Arrow between 10.5 and 10.5 is zero length. Let me fix by regenerating cleanly.

    fig.savefig(OUT / "block_scheme.png", facecolor=C_BG, bbox_inches="tight")
    plt.close(fig)

    # Regenerate with corrected layout
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.text(6.5, 6.8, "Структурная схема «РеспироПВ-2»", ha="center", fontsize=13, fontweight="bold")

    nodes = [
        (0.3, 4.7, 2.0, 1.2, "Источник\nO₂/воздух\nили турбина", C_TECH),
        (2.7, 4.7, 2.0, 1.2, "Редуктор /\nblender\nFiO₂", C_TECH),
        (5.1, 4.7, 2.3, 1.2, "Блок управления\nSIMV / P-SIMV\n/ PSV", C_ACCENT),
        (7.8, 4.7, 2.2, 1.2, "НК + клапан\nПДКВ", C_TECH),
        (10.5, 4.7, 2.0, 1.2, "Пациент\n(маска/ЭТТ)", C_BIO),
        (5.1, 2.7, 2.3, 1.1, "Датчики\nPaw · поток · FiO₂", C_PORT),
        (5.1, 0.9, 2.3, 1.1, "UI / тревоги\nжурнал", C_PORT),
        (0.3, 2.7, 2.0, 1.1, "Питание\n220 В / АКБ", C_STAT),
        (7.8, 2.7, 2.2, 1.1, "Увлажнитель\nили HME", C_STAT),
    ]
    for x, y, w, h, t, c in nodes:
        box(ax, x, y, w, h, t, c, fontsize=7.5)

    def arr(x1, y1, x2, y2, c=C_LINE):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=c, lw=1.5))

    arr(2.3, 5.3, 2.7, 5.3)
    arr(4.7, 5.3, 5.1, 5.3)
    arr(7.4, 5.3, 7.8, 5.3)
    arr(10.0, 5.3, 10.5, 5.3)
    ax.annotate("", xy=(6.25, 3.8), xytext=(6.25, 4.7),
                arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.4))
    ax.annotate("", xy=(6.25, 2.0), xytext=(6.25, 2.7),
                arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.4))
    arr(2.3, 3.25, 5.1, 3.25)
    arr(7.4, 3.25, 7.8, 3.25)
    ax.text(6.5, 6.15, "инспираторная линия →", ha="center", fontsize=8, style="italic", color="#555")

    fig.tight_layout()
    fig.savefig(OUT / "block_scheme.png", facecolor=C_BG, bbox_inches="tight")
    plt.close(fig)


def fig_variants():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=150)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.text(5, 5.15, "Техническое предложение: сравнение вариантов", ha="center", fontsize=12, fontweight="bold")

    variants = [
        (0.4, 1.2, 2.8, 3.4, "Вариант 1\nПневмоавтоматика",
         "• автономность\n• простота\n• слабый SIMV\n• бедный мониторинг", C_SOFT, C_LINE),
        (3.6, 1.2, 2.8, 3.4, "Вариант 2\nТурбина + электроника",
         "• точный триггер\n• полный UI\n• дороже\n• зависимость от АКБ", C_SOFT, C_LINE),
        (6.8, 1.2, 2.8, 3.4, "Вариант 3 ✓\nГибрид модульный",
         "• SIMV / P-SIMV\n• С + П унификация\n• fail-safe механика\n• оптимум цена/качество", "#DCE8DF", C_STAT),
    ]
    for x, y, w, h, title, body, face, edge in variants:
        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.1",
                           linewidth=1.8 if "✓" in title else 1.2,
                           edgecolor=edge, facecolor=face)
        ax.add_patch(r)
        ax.text(x + w / 2, y + h - 0.55, title, ha="center", va="center", fontsize=9, fontweight="bold", color=edge)
        ax.text(x + 0.2, y + 0.35, body, ha="left", va="bottom", fontsize=8, color=C_LINE, family="DejaVu Sans")

    fig.tight_layout()
    fig.savefig(OUT / "variants.png", facecolor=C_BG, bbox_inches="tight")
    plt.close(fig)


def fig_sketch_general():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.text(6, 6.7, "Эскизный общий вид аппарата «РеспироПВ-2»", ha="center", fontsize=13, fontweight="bold")

    # Stationary cart
    ax.text(3.2, 6.2, "Исполнение С — стационарное", ha="center", fontsize=10, color=C_STAT, fontweight="bold")
    # trolley
    ax.add_patch(Rectangle((1.2, 0.6), 4.0, 0.25, facecolor="#888", edgecolor=C_LINE))
    ax.add_patch(Circle((1.6, 0.45), 0.22, facecolor="#444"))
    ax.add_patch(Circle((4.8, 0.45), 0.22, facecolor="#444"))
    # stand
    ax.add_patch(Rectangle((2.9, 0.85), 0.35, 2.2, facecolor="#777", edgecolor=C_LINE))
    # main unit
    ax.add_patch(FancyBboxPatch((1.6, 3.0), 3.2, 2.4, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor="#F0F4F0", edgecolor=C_STAT, linewidth=1.6))
    ax.add_patch(FancyBboxPatch((1.85, 4.0), 2.7, 1.15, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="#1a2a22", edgecolor=C_LINE))
    ax.text(3.2, 4.55, "UI 10\"  SIMV", ha="center", color="#B8E0C8", fontsize=8)
    ax.text(3.2, 3.35, "Блендер · увлажнитель\nблок управления", ha="center", fontsize=7.5, color=C_LINE)
    # humidifier box
    ax.add_patch(FancyBboxPatch((4.5, 1.3), 0.9, 1.3, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="#D9E6F2", edgecolor=C_PORT))
    ax.text(4.95, 1.95, "увл.", ha="center", fontsize=7)
    # circuit line
    ax.plot([4.8, 5.6, 5.6], [4.2, 4.2, 5.5], color=C_ACCENT, lw=2)
    ax.text(5.75, 5.6, "контур", fontsize=7, color=C_ACCENT)

    # Portable
    ax.text(9.2, 6.2, "Исполнение П — портативное", ha="center", fontsize=10, color=C_PORT, fontweight="bold")
    ax.add_patch(FancyBboxPatch((7.4, 2.4), 3.6, 2.8, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#EEF3F7", edgecolor=C_PORT, linewidth=1.8))
    ax.add_patch(FancyBboxPatch((7.7, 4.0), 3.0, 0.95, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor="#152033", edgecolor=C_LINE))
    ax.text(9.2, 4.45, "UI 5\"  P-SIMV", ha="center", color="#A8C8E8", fontsize=8)
    ax.text(9.2, 3.35, "турбина + АКБ ≥ 4 ч\nмасса ≤ 6 кг · IP33", ha="center", fontsize=7.5)
    # handle
    ax.plot([8.0, 8.0, 10.4, 10.4], [5.2, 5.55, 5.55, 5.2], color=C_PORT, lw=2.5)
    ax.text(9.2, 5.75, "ручка", fontsize=7, color=C_PORT, ha="center")
    # small cylinder optional
    ax.add_patch(FancyBboxPatch((7.6, 1.0), 0.7, 1.2, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor="#F5E6DC", edgecolor=C_ACCENT))
    ax.text(7.95, 0.7, "O₂ 2 л\n(опция)", ha="center", fontsize=6.5, color=C_ACCENT)
    ax.add_patch(FancyBboxPatch((8.7, 1.15), 2.0, 0.9, boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=C_SOFT, edgecolor=C_LINE))
    ax.text(9.7, 1.6, "HME + маска", ha="center", fontsize=7.5)

    # callouts
    ax.text(3.2, 0.15, "тележка · сеть 220 В · разводка газов", ha="center", fontsize=7.5, color="#555")
    ax.text(9.2, 0.15, "транспорт / СМП · крепление к носилкам", ha="center", fontsize=7.5, color="#555")

    fig.tight_layout()
    fig.savefig(OUT / "sketch_general.png", facecolor=C_BG, bbox_inches="tight")
    plt.close(fig)


def fig_sketch_circuit():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.text(5.5, 6.15, "Эскиз дыхательного контура и клапанного узла", ha="center", fontsize=12, fontweight="bold")

    # Apparatus outlet
    box(ax, 0.3, 2.6, 1.8, 1.2, "Аппарат\nПАЦИЕНТ", C_TECH, 8)
    # tube
    ax.annotate("", xy=(3.0, 3.2), xytext=(2.1, 3.2),
                arrowprops=dict(arrowstyle="->", color=C_ACCENT, lw=2))
    ax.text(2.4, 3.45, "вдох", fontsize=7, color=C_ACCENT)

    # Non-rebreathing valve assembly
    ax.add_patch(FancyBboxPatch((3.0, 1.8), 3.6, 2.8, boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor="#FFFFFF", edgecolor=C_LINE, linewidth=1.5))
    ax.text(4.8, 4.35, "Нереверсивный клапан", ha="center", fontsize=9, fontweight="bold")

    box(ax, 3.25, 3.2, 1.4, 0.7, "Клапан\nвдоха", C_BIO, 7)
    box(ax, 4.95, 3.2, 1.4, 0.7, "Клапан\nвыдоха", C_ACCENT, 7)
    box(ax, 3.9, 2.1, 1.8, 0.7, "Предохр. клапан", "#8B4513", 7)

    # PEEP
    box(ax, 7.0, 3.35, 1.6, 0.9, "ПДКВ\n0–20 см вд.ст.", C_PORT, 7)
    ax.annotate("", xy=(7.0, 3.8), xytext=(6.6, 3.55),
                arrowprops=dict(arrowstyle="->", color=C_LINE, lw=1.4))
    ax.text(7.8, 4.5, "выдох в атмосферу", fontsize=7, color="#555", ha="center")

    # To patient
    ax.annotate("", xy=(4.8, 1.8), xytext=(4.8, 1.8))
    ax.annotate("", xy=(4.8, 1.2), xytext=(4.8, 1.8),
                arrowprops=dict(arrowstyle="->", color=C_BIO, lw=2))
    box(ax, 3.7, 0.35, 2.2, 0.85, "Маска / ЭТТ\n→ пациент", C_BIO, 8)

    # Sensors
    box(ax, 7.0, 1.5, 1.8, 1.0, "Отбор Paw\nк датчику", C_SOFT, 7, text_color=C_LINE)
    ax.plot([6.6, 7.0], [2.5, 2.0], color=C_LINE, lw=1.2, ls="--")

    box(ax, 9.1, 2.6, 1.6, 1.2, "HME /\nувлажнитель", C_STAT, 7)
    ax.annotate("", xy=(9.1, 2.9), xytext=(5.9, 1.0),
                arrowprops=dict(arrowstyle="-", color="#999", lw=1, ls=":"))
    ax.text(8.2, 0.5, "в стационаре — активный увлажнитель;\nв портативе — HME на линии пациента",
            fontsize=7.5, color="#555", ha="left")

    # Legend positions
    ax.text(0.3, 5.5, "Поз.7 — НК-ПВ", fontsize=8, color=C_LINE)
    ax.text(0.3, 5.15, "Поз.8 — клапан ПДКВ", fontsize=8, color=C_LINE)
    ax.text(0.3, 4.8, "Поз.9–10 — контур и интерфейс", fontsize=8, color=C_LINE)

    fig.tight_layout()
    fig.savefig(OUT / "sketch_circuit.png", facecolor=C_BG, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_scheme_links()
    fig_block_scheme()
    fig_variants()
    fig_sketch_general()
    fig_sketch_circuit()
    print("Diagrams saved to", OUT)
