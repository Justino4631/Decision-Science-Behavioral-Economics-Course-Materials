import inspect
import json
import sys

from PySide6.QtCore import Qt, QTimer, QPointF, QRectF, QPropertyAnimation, QEasingCurve, Signal, QUrl
from PySide6.QtGui import QFont, QColor, QPainter, QPainterPath, QPen
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QComboBox, QLineEdit, QPlainTextEdit, QSpinBox, QSlider, QScrollArea,
    QHBoxLayout, QVBoxLayout, QStackedWidget, QButtonGroup,
    QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QAbstractItemView, QFileDialog,
)

from game import Game
import strategy_store
import sounds_gen
from strategies import STRATEGY_DESCRIPTIONS

PAYOFFS = {
    (0, 0): (3, 3),
    (1, 0): (5, 0),
    (0, 1): (0, 5),
    (1, 1): (1, 1),
}

COLORS = {
    "void":      "#0a0e17",
    "bg":        "#0d1220",
    "panel":     "#11172a",
    "card":      "#161d33",
    "card_hi":   "#1c2540",
    "border":    "#26314f",
    "border_hi": "#3a4a75",

    "cyan":      "#00e5ff",
    "cyan_dim":  "#0891a8",
    "magenta":   "#ff2ea6",
    "magenta_dim": "#a81c6d",
    "gold":      "#ffc857",

    "coop":      "#00ffa3",
    "defect":    "#ff3b5c",

    "text":      "#e9edf7",
    "text_dim":  "#8792ab",
    "text_faint": "#4d5878",
    "success":   "#00ffa3",
}

MONO_FAMILY = "Consolas"
NEW_STRAT_LABEL = "\u270e  New strategy\u2026"

STYLESHEET = f"""
QWidget {{
    background: {COLORS["bg"]};
    color: {COLORS["text"]};
    font-family: "Segoe UI";
    font-size: 13px;
}}
#Sidebar {{
    background: {COLORS["panel"]};
    border-right: 1px solid {COLORS["border"]};
}}
#Brand {{
    color: {COLORS["cyan"]};
    font-size: 18px;
    font-weight: 700;
}}
#BrandSub, #SidebarFooter {{
    color: {COLORS["text_faint"]};
    font-size: 11px;
}}
QPushButton#NavButton {{
    text-align: left;
    padding: 12px 14px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0px;
    background: transparent;
    color: {COLORS["text_dim"]};
    font-weight: 600;
}}
QPushButton#NavButton:hover {{
    background: {COLORS["card"]};
    color: {COLORS["text"]};
}}
QPushButton#NavButton:checked {{
    background: {COLORS["card"]};
    color: {COLORS["cyan"]};
    border-left: 3px solid {COLORS["cyan"]};
}}
QFrame#Card, QFrame#PlayerCard {{
    background: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 14px;
}}
QLabel#PageTitle {{ font-size: 17px; font-weight: 700; }}
QLabel#PageSubtitle {{ color: {COLORS["text_dim"]}; font-size: 12px; }}
QLabel#FieldLabel {{ color: {COLORS["text_dim"]}; font-size: 11px; font-weight: 600; }}
QLabel#DescLabel {{ color: {COLORS["text_dim"]}; font-size: 12px; }}
QLabel#DirtySynced {{ color: {COLORS["text_faint"]}; font-size: 11px; }}
QLabel#DirtyUnsaved {{ color: {COLORS["gold"]}; font-size: 11px; font-weight: 600; }}

QComboBox, QLineEdit, QSpinBox {{
    background: {COLORS["card_hi"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    padding: 6px 8px;
    color: {COLORS["text"]};
}}
QComboBox:focus, QLineEdit:focus, QSpinBox:focus {{
    border: 1px solid {COLORS["cyan"]};
}}
QComboBox QAbstractItemView {{
    background: {COLORS["card_hi"]};
    color: {COLORS["text"]};
    selection-background-color: {COLORS["cyan_dim"]};
    outline: none;
}}

QPlainTextEdit#CodeEditor {{
    background: {COLORS["void"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 10px;
    padding: 8px;
    selection-background-color: {COLORS["cyan_dim"]};
}}

QPushButton {{
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 700;
    border: none;
}}
QPushButton#PrimaryButton {{ background: {COLORS["cyan"]}; color: #0a0e17; }}
QPushButton#PrimaryButton:hover {{ background: #5df3ff; }}
QPushButton#PrimaryButton:disabled {{ background: {COLORS["card_hi"]}; color: {COLORS["text_faint"]}; }}
QPushButton#SuccessButton {{ background: {COLORS["success"]}; color: #0a0e17; }}
QPushButton#SuccessButton:hover {{ background: #5dffc4; }}
QPushButton#GhostButton {{ background: {COLORS["card_hi"]}; color: {COLORS["text"]}; }}
QPushButton#GhostButton:hover {{ background: {COLORS["border_hi"]}; }}
QPushButton#GhostButton:disabled {{ background: {COLORS["card_hi"]}; color: {COLORS["text_faint"]}; }}
QPushButton#GhostButton:checked {{ background: {COLORS["cyan_dim"]}; color: {COLORS["cyan"]}; }}

QLabel#StatusIdle {{ background: {COLORS["card_hi"]}; color: {COLORS["text_dim"]};
                      border-radius: 10px; padding: 4px 12px; font-weight: 700; }}
QLabel#StatusRunning {{ background: {COLORS["cyan_dim"]}; color: {COLORS["cyan"]};
                         border-radius: 10px; padding: 4px 12px; font-weight: 700; }}
QLabel#StatusPaused {{ background: {COLORS["magenta_dim"]}; color: {COLORS["magenta"]};
                        border-radius: 10px; padding: 4px 12px; font-weight: 700; }}
QLabel#StatusDone {{ background: #1f4d3a; color: {COLORS["success"]};
                      border-radius: 10px; padding: 4px 12px; font-weight: 700; }}

QSlider::groove:horizontal {{ background: {COLORS["card_hi"]}; height: 4px; border-radius: 2px; }}
QSlider::handle:horizontal {{ background: {COLORS["cyan"]}; width: 14px; margin: -6px 0; border-radius: 7px; }}

QScrollBar:horizontal {{ background: {COLORS["panel"]}; height: 12px; border-radius: 6px; }}
QScrollBar::handle:horizontal {{ background: {COLORS["card_hi"]}; border-radius: 6px; min-width: 24px; }}
QScrollBar::handle:horizontal:hover {{ background: {COLORS["border_hi"]}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
QScrollBar:vertical {{ background: {COLORS["panel"]}; width: 12px; border-radius: 6px; }}
QScrollBar::handle:vertical {{ background: {COLORS["card_hi"]}; border-radius: 6px; min-height: 24px; }}

QTableWidget {{
    background: {COLORS["card"]};
    gridline-color: {COLORS["border"]};
    border: none;
    border-radius: 10px;
}}
QHeaderView::section {{
    background: {COLORS["card_hi"]};
    color: {COLORS["cyan"]};
    border: none;
    padding: 8px;
    font-weight: 700;
}}
QTableWidget::item {{ padding: 4px; }}
QTableWidget::item:selected {{ background: {COLORS["cyan_dim"]}; color: #0a0e17; }}
"""


# ======================================================================
# Small building blocks
# ======================================================================
class StatusPill(QLabel):
    STATES = {
        "idle":    ("StatusIdle", "\u25cf Ready"),
        "running": ("StatusRunning", "\u25c9 Running"),
        "paused":  ("StatusPaused", "\u275a\u275a Paused"),
        "done":    ("StatusDone", "\u2713 Complete"),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_state("idle")

    def set_state(self, state, text=None):
        object_name, default_text = self.STATES.get(state, self.STATES["idle"])
        self.setObjectName(object_name)
        self.setText(text or default_text)
        self.style().unpolish(self)
        self.style().polish(self)


def legend_dot(color: str, text: str) -> QWidget:
    wrap = QWidget()
    row = QHBoxLayout(wrap)
    row.setContentsMargins(12, 0, 0, 0)
    row.setSpacing(5)
    dot = QLabel()
    dot.setFixedSize(10, 10)
    dot.setStyleSheet(f"background:{color}; border-radius:5px;")
    row.addWidget(dot)
    lbl = QLabel(text)
    lbl.setObjectName("DescLabel")
    row.addWidget(lbl)
    return wrap


# ======================================================================
# Player strategy panel — combo + name + description + always-visible,
# expanding code editor + save/reset. Everything is on screen at once,
# no scrolling or expand/collapse needed to see or edit the code.
# ======================================================================
class PlayerPanel(QFrame):
    def __init__(self, title: str, accent: str, parent=None):
        super().__init__(parent)
        self.setObjectName("PlayerCard")
        self.accent = accent
        self.dirty = False
        self.loaded_source = ""
        self._build(title)

    def _build(self, title):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        title_row = QHBoxLayout()
        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background:{self.accent}; border-radius:5px;")
        title_row.addWidget(dot)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color:{self.accent}; font-weight:700; font-size:12px;")
        title_row.addWidget(title_lbl)
        title_row.addStretch(1)
        layout.addLayout(title_row)

        pick_row = QHBoxLayout()
        self.combo = QComboBox()
        pick_row.addWidget(self.combo, 1)
        self.name_edit = QLineEdit()
        self.name_edit.setFont(QFont(MONO_FAMILY, 10))
        pick_row.addWidget(self.name_edit, 1)
        layout.addLayout(pick_row)

        meta_row = QHBoxLayout()
        self.desc_lbl = QLabel("")
        self.desc_lbl.setObjectName("DescLabel")
        self.desc_lbl.setWordWrap(True)
        meta_row.addWidget(self.desc_lbl, 1)
        self.dirty_lbl = QLabel("\u2713 synced")
        self.dirty_lbl.setObjectName("DirtySynced")
        meta_row.addWidget(self.dirty_lbl, 0, Qt.AlignmentFlag.AlignRight)
        layout.addLayout(meta_row)

        self.code_edit = QPlainTextEdit()
        self.code_edit.setObjectName("CodeEditor")
        self.code_edit.setFont(QFont(MONO_FAMILY, 11))
        self.code_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.code_edit, 1)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("\U0001f4be  Save to Catalog")
        self.save_btn.setObjectName("SuccessButton")
        btn_row.addWidget(self.save_btn)
        self.reset_btn = QPushButton("\u21ba  Reset")
        self.reset_btn.setObjectName("GhostButton")
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

    def set_dirty(self, dirty: bool):
        self.dirty = dirty
        if dirty:
            self.dirty_lbl.setObjectName("DirtyUnsaved")
            self.dirty_lbl.setText("\u25cf unsaved edits")
        else:
            self.dirty_lbl.setObjectName("DirtySynced")
            self.dirty_lbl.setText("\u2713 synced")
        self.dirty_lbl.style().unpolish(self.dirty_lbl)
        self.dirty_lbl.style().polish(self.dirty_lbl)


# ======================================================================
# Timeline canvas — custom-painted widget (antialiased, real rounded
# rects and smooth curves) living inside a QScrollArea so scroll-back
# is just... a scrollbar, with no manual redraw bookkeeping needed.
# ======================================================================
class TimelineCanvas(QWidget):
    def __init__(self, num_rounds: int, parent=None):
        super().__init__(parent)
        self.num_rounds = num_rounds
        self.moves = []
        self.p1_scores = [0]
        self.p2_scores = [0]
        self.current_step = 0
        self.plot_h = 230
        width = max(1400, num_rounds * 22 + 200)
        self.setFixedSize(width, self.plot_h + 60)

    def advance(self, move):
        m1, m2 = move
        self.moves.append(move)
        p1_pts, p2_pts = PAYOFFS[(m1, m2)]
        self.p1_scores.append(self.p1_scores[-1] + p1_pts)
        self.p2_scores.append(self.p2_scores[-1] + p2_pts)
        self.current_step += 1
        self.update()
        x_head = 20 + (self.current_step - 1) * 22 + 16
        return self.p1_scores[-1], self.p2_scores[-1], x_head

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(COLORS["void"]))

        base_y = 210
        plot_top = 20
        plot_bottom = base_y

        grid_pen = QPen(QColor(COLORS["border"]))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        painter.drawLine(QPointF(0, base_y), QPointF(self.width(), base_y))
        faint_pen = QPen(QColor("#161d2e"))
        faint_pen.setWidth(1)
        painter.setPen(faint_pen)
        painter.drawLine(QPointF(0, plot_top), QPointF(self.width(), plot_top))
        painter.drawLine(QPointF(0, (plot_top + base_y) / 2), QPointF(self.width(), (plot_top + base_y) / 2))

        text_faint = QColor(COLORS["text_faint"])
        for i in range(self.current_step):
            m1, m2 = self.moves[i]
            x = 20 + i * 22
            c1 = QColor(COLORS["coop"] if m1 == 0 else COLORS["defect"])
            c2 = QColor(COLORS["coop"] if m2 == 0 else COLORS["defect"])

            p1 = QPainterPath()
            p1.addRoundedRect(QRectF(x, 15, 16, 18), 3, 3)
            painter.fillPath(p1, c1)

            p2 = QPainterPath()
            p2.addRoundedRect(QRectF(x, 40, 16, 18), 3, 3)
            painter.fillPath(p2, c2)

            if (i + 1) % 5 == 0 or i == 0:
                painter.setPen(text_faint)
                painter.drawText(QPointF(x + 2, 78), str(i + 1))

        if self.current_step > 0:
            last_x = 20 + (self.current_step - 1) * 22 + 8
            playhead_pen = QPen(QColor(COLORS["border_hi"]))
            playhead_pen.setWidth(1)
            playhead_pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(playhead_pen)
            painter.drawLine(QPointF(last_x, 10), QPointF(last_x, 62))

        if self.current_step > 0:
            max_p = max(max(self.p1_scores), max(self.p2_scores), 1)
            scale = (plot_bottom - plot_top - 10) / max_p

            def score_path(scores):
                path = QPainterPath()
                for i, s in enumerate(scores):
                    x = 20 + (i - 1) * 22 + 8
                    y = plot_bottom - s * scale
                    if i == 0:
                        path.moveTo(x, y)
                    else:
                        path.lineTo(x, y)
                return path

            pen1 = QPen(QColor(COLORS["cyan"]))
            pen1.setWidth(2)
            pen1.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen1.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen1)
            painter.drawPath(score_path(self.p1_scores))

            pen2 = QPen(QColor(COLORS["magenta"]))
            pen2.setWidth(2)
            pen2.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen2.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen2)
            painter.drawPath(score_path(self.p2_scores))

            tip_x = 20 + (self.current_step - 1) * 22 + 8
            tip_y1 = plot_bottom - self.p1_scores[-1] * scale
            tip_y2 = plot_bottom - self.p2_scores[-1] * scale
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(COLORS["cyan"]))
            painter.drawEllipse(QPointF(tip_x, tip_y1), 3.5, 3.5)
            painter.setBrush(QColor(COLORS["magenta"]))
            painter.drawEllipse(QPointF(tip_x, tip_y2), 3.5, 3.5)

        painter.end()


class TimelineScrollArea(QScrollArea):
    """A horizontal-only scroll area that turns any wheel scroll (even a
    plain vertical mouse wheel) into horizontal panning, and reports when
    the person scrolls it by hand so auto-follow can step aside."""
    userScrolled = Signal()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() or event.angleDelta().x()
        if delta:
            sb = self.horizontalScrollBar()
            sb.setValue(sb.value() - delta)
            self.userScrolled.emit()
        event.accept()


# ======================================================================
# Match animation popup
# ======================================================================
class MatchAnimationWindow(QDialog):
    def __init__(self, parent, p1_name, p2_name, moves, speed_ms=35, on_finish=None):
        super().__init__(parent)
        self.setWindowTitle(f"{p1_name}  vs  {p2_name}")
        self.resize(1150, 650)
        self.setMinimumSize(760, 460)

        self.p1_name = p1_name
        self.p2_name = p2_name
        self.moves = moves
        self.on_finish = on_finish
        self.follow_playhead = True
        self._last_head_x = 0
        self._closed = False

        self.sound_enabled = True
        self.coop_sound = None
        self.defect_sound = None
        self._init_sounds()

        self._build_ui(speed_ms)
        self._center_over(parent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        QTimer.singleShot(60, self._start)

    def _center_over(self, parent):
        if parent is None:
            return
        geo = parent.geometry()
        x = geo.x() + max(0, (geo.width() - self.width()) // 2)
        y = geo.y() + max(0, (geo.height() - self.height()) // 2)
        self.move(x, y)

    def _init_sounds(self):
        """Best-effort: short cooperate/defect cues. Never fatal — if the
        audio backend isn't available on this machine, we just play silent."""
        try:
            coop_path, defect_path = sounds_gen.ensure_sound_files()
            self.coop_sound = QSoundEffect(self)
            self.coop_sound.setSource(QUrl.fromLocalFile(coop_path))
            self.coop_sound.setVolume(0.35)
            self.defect_sound = QSoundEffect(self)
            self.defect_sound.setSource(QUrl.fromLocalFile(defect_path))
            self.defect_sound.setVolume(0.35)
        except Exception:
            self.coop_sound = None
            self.defect_sound = None
            self.sound_enabled = False

    def _play_move_sound(self, move):
        if not self.sound_enabled:
            return
        m1, m2 = move
        effect = self.coop_sound if (m1 == 0 and m2 == 0) else self.defect_sound
        if effect is not None:
            effect.play()

    def _toggle_sound(self, checked):
        self.sound_enabled = checked
        self.sound_btn.setText("\U0001f50a  Sound" if checked else "\U0001f507  Muted")

    def _build_ui(self, speed_ms):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel(f'<span style="color:{COLORS["cyan"]}">{self.p1_name}</span>'
                        f'<span style="color:{COLORS["text_dim"]}">  \u2694  </span>'
                        f'<span style="color:{COLORS["magenta"]}">{self.p2_name}</span>')
        title.setStyleSheet("font-size:16px; font-weight:700;")
        header.addWidget(title)
        header.addStretch(1)
        close_btn = QPushButton("\u2715  Close")
        close_btn.setObjectName("GhostButton")
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)
        outer.addLayout(header)

        score_row = QHBoxLayout()
        self.p1_score_lbl = self._score_badge(score_row, self.p1_name, COLORS["cyan"])
        score_row.addStretch(1)
        self.p2_score_lbl = self._score_badge(score_row, self.p2_name, COLORS["magenta"], right=True)
        outer.addLayout(score_row)

        ctrl_card = QFrame()
        ctrl_card.setObjectName("Card")
        ctrl_layout = QHBoxLayout(ctrl_card)
        ctrl_layout.setContentsMargins(14, 12, 14, 12)

        ctrl_layout.addWidget(self._field_label("Speed"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(5, 300)
        self.speed_slider.setValue(speed_ms)
        self.speed_slider.setFixedWidth(140)
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        ctrl_layout.addWidget(self.speed_slider)
        ctrl_layout.addSpacing(16)

        self.pause_btn = QPushButton("\u275a\u275a  Pause")
        self.pause_btn.setObjectName("GhostButton")
        self.pause_btn.clicked.connect(self.toggle_pause)
        ctrl_layout.addWidget(self.pause_btn)

        self.step_btn = QPushButton("\u23ed  Step")
        self.step_btn.setObjectName("GhostButton")
        self.step_btn.clicked.connect(self.step_once)
        self.step_btn.setEnabled(False)
        ctrl_layout.addWidget(self.step_btn)

        ctrl_layout.addStretch(1)

        self.live_btn = QPushButton("\u23e9  Jump to Live")
        self.live_btn.setObjectName("GhostButton")
        self.live_btn.clicked.connect(self.jump_to_live)
        self.live_btn.hide()
        ctrl_layout.addWidget(self.live_btn)

        self.sound_btn = QPushButton("\U0001f50a  Sound")
        self.sound_btn.setObjectName("GhostButton")
        self.sound_btn.setCheckable(True)
        self.sound_btn.setChecked(True)
        self.sound_btn.toggled.connect(self._toggle_sound)
        ctrl_layout.addWidget(self.sound_btn)

        self.status_pill = StatusPill()
        self.status_pill.set_state("running")
        ctrl_layout.addWidget(self.status_pill)

        outer.addWidget(ctrl_card)

        disp_card = QFrame()
        disp_card.setObjectName("Card")
        disp_layout = QVBoxLayout(disp_card)
        disp_layout.setContentsMargins(14, 14, 14, 14)

        head_row = QHBoxLayout()
        head_lbl = QLabel("LIVE TIMELINE & SCORE")
        head_lbl.setObjectName("FieldLabel")
        head_row.addWidget(head_lbl)
        head_row.addStretch(1)
        head_row.addWidget(legend_dot(COLORS["coop"], "Cooperate"))
        head_row.addWidget(legend_dot(COLORS["defect"], "Defect"))
        disp_layout.addLayout(head_row)

        self.canvas = TimelineCanvas(len(self.moves))
        self.scroll_area = TimelineScrollArea()
        self.scroll_area.setWidget(self.canvas)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(f"QScrollArea {{ background:{COLORS['void']}; "
                                        f"border: 1px solid {COLORS['border']}; border-radius: 8px; }}")
        self.scroll_area.horizontalScrollBar().sliderMoved.connect(self._on_manual_scroll)
        self.scroll_area.userScrolled.connect(self._on_manual_scroll)
        disp_layout.addWidget(self.scroll_area, 1)

        outer.addWidget(disp_card, 1)

        self._scroll_anim = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value", self)
        self._scroll_anim.setDuration(120)
        self._scroll_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    def _score_badge(self, layout, name, color, right=False):
        wrap = QWidget()
        col = QVBoxLayout(wrap)
        col.setContentsMargins(4, 0, 4, 0)
        col.setSpacing(0)
        align = Qt.AlignmentFlag.AlignRight if right else Qt.AlignmentFlag.AlignLeft
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"color:{color}; font-weight:700; font-size:11px;")
        name_lbl.setAlignment(align)
        col.addWidget(name_lbl)
        score_lbl = QLabel("0")
        score_lbl.setStyleSheet("font-size:22px; font-weight:700;")
        score_lbl.setAlignment(align)
        col.addWidget(score_lbl)
        layout.addWidget(wrap)
        return score_lbl

    # ---- playback -----------------------------------------------------
    def _start(self):
        if self._closed:
            return
        self.timer.start(int(self.speed_slider.value()))

    def _on_speed_changed(self, value):
        if self.timer.isActive():
            self.timer.setInterval(int(value))

    def toggle_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_btn.setText("\u25b6  Resume")
            self.step_btn.setEnabled(True)
            self.status_pill.set_state("paused")
        else:
            if self.canvas.current_step >= len(self.moves):
                return
            self.timer.start(int(self.speed_slider.value()))
            self.pause_btn.setText("\u275a\u275a  Pause")
            self.step_btn.setEnabled(False)
            self.status_pill.set_state("running")

    def step_once(self):
        if not self.timer.isActive():
            self._tick()

    def _tick(self):
        if self.canvas.current_step >= len(self.moves):
            self.timer.stop()
            self._finish()
            return
        move = self.moves[self.canvas.current_step]
        p1_score, p2_score, head_x = self.canvas.advance(move)
        self._play_move_sound(move)
        self.p1_score_lbl.setText(str(p1_score))
        self.p2_score_lbl.setText(str(p2_score))
        self._autoscroll_to(head_x)
        if self.canvas.current_step >= len(self.moves):
            self.timer.stop()
            self._finish()

    # ---- scroll-back ----------------------------------------------------
    def _on_manual_scroll(self, *_args):
        self.follow_playhead = False
        self.live_btn.show()

    def jump_to_live(self):
        self.follow_playhead = True
        self.live_btn.hide()
        self._autoscroll_to(self._last_head_x, animate=True)

    def _autoscroll_to(self, head_x, animate=True):
        self._last_head_x = head_x
        if not self.follow_playhead:
            return
        sb = self.scroll_area.horizontalScrollBar()
        viewport_w = self.scroll_area.viewport().width()
        margin = 160
        target = head_x - (viewport_w - margin)
        target = max(sb.minimum(), min(target, sb.maximum()))
        if animate:
            self._scroll_anim.stop()
            self._scroll_anim.setStartValue(sb.value())
            self._scroll_anim.setEndValue(target)
            self._scroll_anim.start()
        else:
            sb.setValue(target)

    # ---- finish / close -------------------------------------------------
    def _finish(self):
        self.pause_btn.setEnabled(False)
        self.step_btn.setEnabled(False)
        p1_final = self.canvas.p1_scores[-1]
        p2_final = self.canvas.p2_scores[-1]
        if p1_final > p2_final:
            res = f"\u2713 {self.p1_name} wins {p1_final} \u2013 {p2_final}"
        elif p2_final > p1_final:
            res = f"\u2713 {self.p2_name} wins {p2_final} \u2013 {p1_final}"
        else:
            res = f"\u2713 Tie {p1_final} \u2013 {p2_final}"
        self.status_pill.set_state("done", text=res)
        if callable(self.on_finish):
            try:
                self.on_finish(res)
            except Exception:
                pass

    def closeEvent(self, event):
        self._closed = True
        self.timer.stop()
        super().closeEvent(event)


# ======================================================================
# Main window
# ======================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPD ARENA \u2014 Iterated Prisoner's Dilemma Lab (Qt edition)")
        self.resize(1400, 900)
        self.setMinimumSize(1100, 720)

        self.strat_catalog = strategy_store.all_strategies()
        self.last_tournament_results = None

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        self.arena_page = self._build_arena_page()
        self.tournament_page = self._build_tournament_page()
        self.stack.addWidget(self.arena_page)
        self.stack.addWidget(self.tournament_page)

        self._init_player_selectors()

    # ------------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 22, 20, 18)
        layout.setSpacing(4)

        brand = QLabel("\u26a1 IPD ARENA")
        brand.setObjectName("Brand")
        layout.addWidget(brand)
        sub = QLabel("Strategy Simulation Lab (Qt)")
        sub.setObjectName("BrandSub")
        layout.addWidget(sub)
        layout.addSpacing(20)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        arena_btn = QPushButton("  \u2694   Match Arena")
        arena_btn.setObjectName("NavButton")
        arena_btn.setCheckable(True)
        arena_btn.setChecked(True)
        arena_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.nav_group.addButton(arena_btn)
        layout.addWidget(arena_btn)

        tourney_btn = QPushButton("  \U0001f3c6   Tournament")
        tourney_btn.setObjectName("NavButton")
        tourney_btn.setCheckable(True)
        tourney_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.nav_group.addButton(tourney_btn)
        layout.addWidget(tourney_btn)

        layout.addStretch(1)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background:{COLORS['border']};")
        line.setFixedHeight(1)
        layout.addWidget(line)

        self.sidebar_count_lbl = QLabel(f"{len(self.strat_catalog)} strategies loaded")
        self.sidebar_count_lbl.setObjectName("SidebarFooter")
        layout.addWidget(self.sidebar_count_lbl)

        return sidebar

    def _page_header(self, layout, title, subtitle):
        t = QLabel(title)
        t.setObjectName("PageTitle")
        layout.addWidget(t)
        s = QLabel(subtitle)
        s.setObjectName("PageSubtitle")
        layout.addWidget(s)
        layout.addSpacing(6)

    # ==================================================================
    # ARENA PAGE
    # ==================================================================
    def _build_arena_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(16)

        self._page_header(layout, "Match Arena",
                           "Set up both strategies, then launch the match to watch it play out")

        ctrl_card = QFrame()
        ctrl_card.setObjectName("Card")
        ctrl_layout = QHBoxLayout(ctrl_card)
        ctrl_layout.setContentsMargins(14, 12, 14, 12)

        ctrl_layout.addWidget(self._field_label("Rounds"))
        self.rounds_spin = QSpinBox()
        self.rounds_spin.setRange(1, 5000)
        self.rounds_spin.setValue(100)
        self.rounds_spin.setFixedWidth(80)
        ctrl_layout.addWidget(self.rounds_spin)
        ctrl_layout.addSpacing(20)

        ctrl_layout.addWidget(self._field_label("Speed"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(5, 300)
        self.speed_slider.setValue(100)
        self.speed_slider.setFixedWidth(140)
        ctrl_layout.addWidget(self.speed_slider)
        ctrl_layout.addSpacing(20)

        self.launch_btn = QPushButton("\u25b6  Launch Match")
        self.launch_btn.setObjectName("PrimaryButton")
        self.launch_btn.clicked.connect(self._launch_match)
        ctrl_layout.addWidget(self.launch_btn)

        ctrl_layout.addStretch(1)
        self.last_result_lbl = QLabel("No matches played yet")
        self.last_result_lbl.setObjectName("DescLabel")
        ctrl_layout.addWidget(self.last_result_lbl)

        layout.addWidget(ctrl_card)

        panels_row = QHBoxLayout()
        panels_row.setSpacing(16)
        self.p1_panel = PlayerPanel("PLAYER 1", COLORS["cyan"])
        self.p2_panel = PlayerPanel("PLAYER 2", COLORS["magenta"])
        panels_row.addWidget(self.p1_panel, 1)
        panels_row.addWidget(self.p2_panel, 1)
        layout.addLayout(panels_row, 1)

        for panel in (self.p1_panel, self.p2_panel):
            panel.combo.currentTextChanged.connect(lambda _text, p=panel: self._on_pick_strategy(p))
            panel.code_edit.textChanged.connect(lambda p=panel: self._mark_dirty(p))
            panel.name_edit.textChanged.connect(lambda _text, p=panel: self._mark_dirty(p))
            panel.save_btn.clicked.connect(lambda _checked=False, p=panel: self._save_panel_to_catalog(p))
            panel.reset_btn.clicked.connect(lambda _checked=False, p=panel: self._reset_panel(p))

        return page

    def _field_label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    # ---- strategy loading / editing helpers -------------------------
    def _init_player_selectors(self):
        self._refresh_strategy_lists()
        names = sorted(self.strat_catalog.keys())
        p1_default = names[0] if names else None
        p2_default = names[1] if len(names) > 1 else (names[0] if names else None)

        for panel, default in ((self.p1_panel, p1_default), (self.p2_panel, p2_default)):
            panel.combo.blockSignals(True)
            panel.combo.setCurrentText(default if default else NEW_STRAT_LABEL)
            panel.combo.blockSignals(False)
            self._on_pick_strategy(panel)

    def _refresh_strategy_lists(self):
        names = sorted(self.strat_catalog.keys())
        values = [NEW_STRAT_LABEL] + names
        for panel in (getattr(self, "p1_panel", None), getattr(self, "p2_panel", None)):
            if panel is None:
                continue
            current = panel.combo.currentText()
            panel.combo.blockSignals(True)
            panel.combo.clear()
            panel.combo.addItems(values)
            if current in values:
                panel.combo.setCurrentText(current)
            panel.combo.blockSignals(False)
        if hasattr(self, "sidebar_count_lbl"):
            self.sidebar_count_lbl.setText(f"{len(self.strat_catalog)} strategies loaded")

    def _on_pick_strategy(self, panel):
        choice = panel.combo.currentText()
        if choice == NEW_STRAT_LABEL:
            self._load_blank_template(panel, "custom_strategy")
        else:
            self._load_named_strategy(panel, choice)

    def _load_named_strategy(self, panel, name):
        func = self.strat_catalog.get(name)
        if func is None:
            return
        doc = STRATEGY_DESCRIPTIONS.get(func.__name__, "No documentation provided.")
        src = getattr(func, "__source__", None)
        if src is None:
            try:
                src = inspect.getsource(func)
            except Exception:
                src = f"# Source unavailable for '{name}' \u2014 you can still edit and re-run it.\n"

        panel.name_edit.blockSignals(True)
        panel.name_edit.setText(name)
        panel.name_edit.blockSignals(False)
        panel.desc_lbl.setText(doc)
        panel.code_edit.blockSignals(True)
        panel.code_edit.setPlainText(src)
        panel.code_edit.blockSignals(False)
        panel.loaded_source = src
        panel.set_dirty(False)

    def _load_blank_template(self, panel, default_name):
        src = strategy_store.strategy_template(default_name)
        panel.name_edit.blockSignals(True)
        panel.name_edit.setText(default_name)
        panel.name_edit.blockSignals(False)
        panel.desc_lbl.setText("A fresh strategy \u2014 edit the code, then Save to Catalog to reuse it.")
        panel.code_edit.blockSignals(True)
        panel.code_edit.setPlainText(src)
        panel.code_edit.blockSignals(False)
        panel.loaded_source = src
        panel.set_dirty(False)

    def _mark_dirty(self, panel):
        panel.set_dirty(True)

    def _reset_panel(self, panel):
        choice = panel.combo.currentText()
        if choice == NEW_STRAT_LABEL:
            self._load_blank_template(panel, "custom_strategy")
        else:
            self._load_named_strategy(panel, choice)

    def _compile_panel_strategy(self, panel, label):
        code_str = panel.code_edit.toPlainText()
        func_name = panel.name_edit.text().strip()
        try:
            func = strategy_store.compile_strategy(code_str, func_name)
        except ValueError as e:
            raise ValueError(f"{label}: {e}")
        return func, func_name

    def _save_panel_to_catalog(self, panel):
        label = "Player 1" if panel is self.p1_panel else "Player 2"
        try:
            func, name = self._compile_panel_strategy(panel, label)
        except ValueError as e:
            QMessageBox.critical(self, "Strategy Error", str(e))
            return

        code_str = panel.code_edit.toPlainText()
        try:
            path = strategy_store.write_strategy_file(name, code_str)
        except (ValueError, OSError) as e:
            QMessageBox.critical(self, "Save Error", f"Could not write strategy file:\n\n{e}")
            return

        self.strat_catalog[name] = func
        panel.loaded_source = code_str
        panel.set_dirty(False)
        self._refresh_strategy_lists()
        panel.combo.blockSignals(True)
        panel.combo.setCurrentText(name)
        panel.combo.blockSignals(False)
        QMessageBox.information(self, "Saved", f"Strategy '{name}' saved to:\n{path}")

    # ---- match launch --------------------------------------------------
    def _launch_match(self):
        try:
            s1_func, s1_name = self._compile_panel_strategy(self.p1_panel, "Player 1")
            s2_func, s2_name = self._compile_panel_strategy(self.p2_panel, "Player 2")
        except ValueError as e:
            QMessageBox.critical(self, "Strategy Error", str(e))
            return

        rounds = self.rounds_spin.value()
        game = Game(strategies=[s1_func, s2_func], num_rounds=rounds)
        moves = game.play_round(s1_func, s2_func)
        speed = int(self.speed_slider.value())

        popup = MatchAnimationWindow(self, s1_name, s2_name, moves,
                                      speed_ms=speed, on_finish=self._on_match_finished)
        popup.show()

    def _on_match_finished(self, result_text):
        self.last_result_lbl.setText(result_text)
        self.last_result_lbl.setStyleSheet(f"color:{COLORS['success']}; font-weight:700;")

    # ==================================================================
    # TOURNAMENT PAGE
    # ==================================================================
    def _build_tournament_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 22, 24, 20)
        layout.setSpacing(16)

        self._page_header(layout, "Round Robin Tournament",
                           "Every saved strategy faces every other strategy \u2014 see who rises to the top")

        top_card = QFrame()
        top_card.setObjectName("Card")
        top_layout = QHBoxLayout(top_card)
        top_layout.setContentsMargins(14, 12, 14, 12)

        top_layout.addWidget(self._field_label("Rounds per match"))
        self.tourn_rounds_spin = QSpinBox()
        self.tourn_rounds_spin.setRange(1, 5000)
        self.tourn_rounds_spin.setValue(200)
        self.tourn_rounds_spin.setFixedWidth(90)
        top_layout.addWidget(self.tourn_rounds_spin)
        top_layout.addSpacing(16)

        run_btn = QPushButton("\U0001f680  Run Tournament")
        run_btn.setObjectName("PrimaryButton")
        run_btn.clicked.connect(self._run_tournament)
        top_layout.addWidget(run_btn)

        export_btn = QPushButton("\U0001f4be  Export JSON")
        export_btn.setObjectName("GhostButton")
        export_btn.clicked.connect(self._export_tournament_results)
        top_layout.addWidget(export_btn)

        top_layout.addStretch(1)
        self.tourney_status = QLabel("No results yet")
        self.tourney_status.setObjectName("DescLabel")
        top_layout.addWidget(self.tourney_status)

        layout.addWidget(top_card)

        self.tree = QTableWidget(0, 6)
        self.tree.setHorizontalHeaderLabels(
            ["Rank", "Strategy", "Avg Payout / Round", "Wins", "Ties", "Losses"])
        self.tree.verticalHeader().setVisible(False)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tree.setAlternatingRowColors(False)
        self.tree.itemDoubleClicked.connect(self._show_strategy_history)
        layout.addWidget(self.tree, 1)

        self.last_tournament_results = None
        self.last_tournament_match_history = {}
        return page

    def _build_match_history(self, results: dict) -> dict:
        history = {}
        for (s1, s2), (moves, (p1, p2)) in results.items():
            n1, n2 = s1.__name__, s2.__name__
            history.setdefault(n1, []).append({
                "opponent": n2,
                "moves": moves,
                "self_score": p1,
                "opponent_score": p2,
                "result": self._match_result(p1, p2),
            })
            history.setdefault(n2, []).append({
                "opponent": n1,
                "moves": moves,
                "self_score": p2,
                "opponent_score": p1,
                "result": self._match_result(p2, p1),
            })

        for matches in history.values():
            matches.sort(key=lambda entry: entry["opponent"])
        return history

    def _match_result(self, self_score: int, opp_score: int) -> str:
        if self_score > opp_score:
            return "win"
        if self_score < opp_score:
            return "loss"
        return "tie"

    def _show_strategy_history(self, item):
        if item is None:
            return
        strategy_item = self.tree.item(item.row(), 1)
        if strategy_item is None:
            return

        strategy_name = strategy_item.text()
        history = self.last_tournament_match_history.get(strategy_name, [])
        if not history:
            QMessageBox.information(self, "No History", f"No match history is available for {strategy_name}.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"{strategy_name} — Final Match Totals")
        dialog.resize(760, 620)
        dialog.setMinimumSize(720, 480)
        dialog.setStyleSheet(f"QDialog {{ background: {COLORS['bg']}; color: {COLORS['text']}; }}")

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        header = QFrame()
        header.setObjectName("Card")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(16, 16, 16, 16)
        header_layout.setSpacing(6)

        title = QLabel(f"{strategy_name}")
        title.setStyleSheet(f"color:{COLORS['cyan']}; font-size:20px; font-weight:700;")
        header_layout.addWidget(title)

        subtitle = QLabel("Final totals against every opponent in the tournament")
        subtitle.setObjectName("DescLabel")
        subtitle.setWordWrap(True)
        header_layout.addWidget(subtitle)
        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"QScrollArea {{ background: transparent; }}")

        body = QFrame()
        body.setObjectName("Card")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 16, 16, 16)
        body_layout.setSpacing(10)

        for entry in history:
            row = QFrame()
            row.setStyleSheet(f"QFrame {{ background: {COLORS['card_hi']}; border-radius: 10px; padding: 6px; }}")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(12, 10, 12, 10)

            left = QLabel(f"vs {entry['opponent']}")
            left.setStyleSheet(f"color:{COLORS['text']}; font-weight:700;")
            row_layout.addWidget(left, 1)

            result_label = QLabel(entry['result'].title())
            result_label.setStyleSheet(
                f"color:{COLORS['success'] if entry['result'] == 'win' else COLORS['magenta'] if entry['result'] == 'loss' else COLORS['gold']}; "
                f"font-weight:700;"
            )
            row_layout.addWidget(result_label)

            score_label = QLabel(f"{entry['self_score']} - {entry['opponent_score']}")
            score_label.setStyleSheet(f"color:{COLORS['cyan']}; font-weight:700;")
            row_layout.addWidget(score_label)

            body_layout.addWidget(row)

        scroll_area.setWidget(body)
        layout.addWidget(scroll_area, 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.setObjectName("GhostButton")
        close_btn.clicked.connect(dialog.accept)
        footer.addWidget(close_btn)
        layout.addLayout(footer)

        dialog.exec()

    def _run_tournament(self):
        active_strats = list(self.strat_catalog.values())
        if not active_strats:
            QMessageBox.warning(self, "Warning", "No strategies available to run tournament.")
            return

        rounds = self.tourn_rounds_spin.value()
        game = Game(strategies=active_strats, num_rounds=rounds)
        results = game.rank_strategies()
        self.last_tournament_results = results
        self.last_tournament_match_history = self._build_match_history(game.results)

        medal_colors = {1: COLORS["gold"], 2: "#d8dee9", 3: "#e0a875"}
        medal_icons = {1: "\U0001f947", 2: "\U0001f948", 3: "\U0001f949"}

        self.tree.setRowCount(0)
        for rank, (strat_name, data) in enumerate(results.items(), start=1):
            row = self.tree.rowCount()
            self.tree.insertRow(row)
            rank_text = f"{medal_icons.get(rank, '')} {rank}".strip()
            values = [rank_text, strat_name, f"{data['avg_payout']:.3f}",
                      str(data["wins"]), str(data["ties"]), str(data["losses"])]
            color = medal_colors.get(rank)
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col != 1:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if color:
                    item.setForeground(QColor(color))
                self.tree.setItem(row, col, item)

        self.tourney_status.setText(f"\u2713 {len(active_strats)} strategies \u00b7 {rounds} rounds/match")
        self.tourney_status.setStyleSheet(f"color:{COLORS['success']};")
        QMessageBox.information(self, "Tournament Complete",
                                 f"Successfully ran tournament across {len(active_strats)} strategies!")

    def _export_tournament_results(self):
        if not self.last_tournament_results:
            QMessageBox.warning(self, "Warning", "Run a tournament first before exporting.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export Results", "IPD_Results.json", "JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path, "w") as f:
                json.dump(self.last_tournament_results, f, indent=4)
            QMessageBox.information(self, "Export Successful", f"Saved leaderboard to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()