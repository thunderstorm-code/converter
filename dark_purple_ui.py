"""Standalone PySide6 UI mockup with dark-gray + purple accent theme.

Run:
    python dark_purple_ui.py
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

BG_COLOR = "#212121"
SURFACE_COLOR = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"
TEXT_PRIMARY = "#f2f2f2"
TEXT_SECONDARY = "#bfbfbf"
ACCENT = "#8046d9"
ACCENT_HOVER = "#9564df"


class StyledWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Converter — Modern Dark UI")
        self.resize(960, 620)

        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)

        sidebar = self._build_sidebar()
        content = self._build_content()

        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(content, 3)

        self._apply_palette()
        self._apply_styles()

    def _build_sidebar(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("sidebar")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("Инструменты")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        nav = QListWidget()
        nav.addItems(["Конвертер", "История", "Профили", "Настройки"])
        nav.setCurrentRow(0)
        layout.addWidget(nav)

        layout.addStretch(1)

        profile = QLabel("Профиль: Default")
        profile.setObjectName("secondaryText")
        layout.addWidget(profile)

        return panel

    def _build_content(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        header = QLabel("Красивый дизайн в тёмной теме")
        header.setObjectName("header")
        layout.addWidget(header)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(14)

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(10)

        lbl_from = QLabel("Из")
        inp_from = QLineEdit()
        inp_from.setPlaceholderText("Например: PNG")

        lbl_to = QLabel("В")
        inp_to = QLineEdit()
        inp_to.setPlaceholderText("Например: WEBP")

        lbl_quality = QLabel("Качество")
        quality = QSlider(Qt.Orientation.Horizontal)
        quality.setRange(1, 100)
        quality.setValue(82)

        grid.addWidget(lbl_from, 0, 0)
        grid.addWidget(inp_from, 0, 1)
        grid.addWidget(lbl_to, 1, 0)
        grid.addWidget(inp_to, 1, 1)
        grid.addWidget(lbl_quality, 2, 0)
        grid.addWidget(quality, 2, 1)

        card_layout.addLayout(grid)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        run_btn = QPushButton("Конвертировать")
        run_btn.setObjectName("primary")
        cancel_btn = QPushButton("Сбросить")

        actions.addWidget(run_btn)
        actions.addWidget(cancel_btn)
        actions.addStretch(1)

        card_layout.addLayout(actions)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 120))
        card.setGraphicsEffect(shadow)

        layout.addWidget(card)

        footer = QLabel("Тема: #212121 + #8046d9")
        footer.setObjectName("secondaryText")
        layout.addWidget(footer)

        layout.addStretch(1)
        return container

    def _apply_palette(self) -> None:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(BG_COLOR))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(SURFACE_COLOR))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(BG_COLOR))
        palette.setColor(QPalette.ColorRole.Text, QColor(TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(SURFACE_COLOR))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(ACCENT))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_PRIMARY};
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 13px;
            }}

            #sidebar {{
                background-color: {SURFACE_COLOR};
                border: 1px solid {BORDER_COLOR};
                border-radius: 14px;
            }}

            #sectionTitle {{
                font-size: 15px;
                font-weight: 600;
            }}

            #header {{
                font-size: 22px;
                font-weight: 700;
            }}

            #secondaryText {{
                color: {TEXT_SECONDARY};
            }}

            #card {{
                background-color: {SURFACE_COLOR};
                border: 1px solid {BORDER_COLOR};
                border-radius: 16px;
            }}

            QLineEdit {{
                background-color: #262626;
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
                padding: 8px 10px;
            }}

            QLineEdit:focus {{
                border: 1px solid {ACCENT};
            }}

            QListWidget {{
                background-color: #252525;
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
                padding: 6px;
                outline: none;
            }}

            QListWidget::item {{
                border-radius: 8px;
                padding: 8px;
                margin: 2px 0;
            }}

            QListWidget::item:selected {{
                background-color: {ACCENT};
                color: #ffffff;
            }}

            QPushButton {{
                background-color: #2f2f2f;
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
                padding: 9px 14px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                border-color: {ACCENT};
            }}

            QPushButton#primary {{
                background-color: {ACCENT};
                border: none;
                color: #ffffff;
            }}

            QPushButton#primary:hover {{
                background-color: {ACCENT_HOVER};
            }}

            QSlider::groove:horizontal {{
                height: 6px;
                background: #343434;
                border-radius: 3px;
            }}

            QSlider::handle:horizontal {{
                background: {ACCENT};
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            """
        )


def main() -> None:
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    window = StyledWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
