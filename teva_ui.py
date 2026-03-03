from __future__ import annotations


from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

BG_COLOR = "#212121"
SURFACE = "#2a2a2a"
SURFACE_ALT = "#262626"
TEXT = "#f4f4f4"
MUTED = "#b4b4b4"
ACCENT = "#8046d9"
ACCENT_HOVER = "#9361e0"
BORDER = "#3a3a3a"


class AnimatedStack(QStackedWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._effect)
        self._anim = QPropertyAnimation(self._effect, b"opacity", self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def switch_to(self, index: int) -> None:
        if index == self.currentIndex():
            return

        self._anim.stop()
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(0.0)

        def fade_in() -> None:
            self.setCurrentIndex(index)
            self._anim.finished.disconnect(fade_in)
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(1.0)
            self._anim.start()

        self._anim.finished.connect(fade_in)
        self._anim.start()


class TevaWindow(QMainWindow):
    convert_requested = Signal(str, str, int)
    batch_requested = Signal(str, str, int)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Teva")
        self.resize(860, 560)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)

        title = QLabel("Teva")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("Стильный конвертер файлов")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(8)
        tabs_row.addStretch(1)
        self.single_tab_btn = QPushButton("Один файл")
        self.single_tab_btn.setObjectName("tabActive")
        self.batch_tab_btn = QPushButton("Папка")
        self.batch_tab_btn.setObjectName("tab")
        tabs_row.addWidget(self.single_tab_btn)
        tabs_row.addWidget(self.batch_tab_btn)
        tabs_row.addStretch(1)

        self.stack = AnimatedStack()
        self.stack.addWidget(self._build_single_page())
        self.stack.addWidget(self._build_batch_page())

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(tabs_row)
        layout.addWidget(self._wrap_card(self.stack), 1)

        self.single_tab_btn.clicked.connect(lambda: self._switch_tab(0))
        self.batch_tab_btn.clicked.connect(lambda: self._switch_tab(1))

        self._apply_styles()

    def _wrap_card(self, child: QWidget) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.addWidget(child)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 130))
        card.setGraphicsEffect(shadow)
        return card

    def _build_single_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Выберите файл")

        choose_btn = QPushButton("Обзор")
        choose_btn.clicked.connect(self._pick_file)

        file_row = QHBoxLayout()
        file_row.addWidget(self.file_input, 1)
        file_row.addWidget(choose_btn)

        self.format_box = QComboBox()
        self.format_box.addItems(["png", "jpg", "webp", "bmp"])

        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(90)

        convert_btn = QPushButton("Конвертировать")
        convert_btn.setObjectName("primary")
        convert_btn.clicked.connect(self._emit_single_convert)

        self.status_single = QLabel("Готово к конвертации")
        self.status_single.setObjectName("muted")

        layout.addWidget(QLabel("Файл"))
        layout.addLayout(file_row)
        layout.addWidget(QLabel("Формат"))
        layout.addWidget(self.format_box)
        layout.addWidget(QLabel("Качество"))
        layout.addWidget(self.quality_slider)
        layout.addWidget(convert_btn)
        layout.addWidget(self.status_single)
        layout.addStretch(1)
        return page

    def _build_batch_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Выберите папку")

        choose_btn = QPushButton("Обзор")
        choose_btn.clicked.connect(self._pick_folder)

        folder_row = QHBoxLayout()
        folder_row.addWidget(self.folder_input, 1)
        folder_row.addWidget(choose_btn)

        self.batch_format_box = QComboBox()
        self.batch_format_box.addItems(["png", "jpg", "webp", "bmp"])

        self.batch_quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.batch_quality_slider.setRange(1, 100)
        self.batch_quality_slider.setValue(90)

        convert_btn = QPushButton("Конвертировать папку")
        convert_btn.setObjectName("primary")
        convert_btn.clicked.connect(self._emit_batch_convert)

        self.status_batch = QLabel("Выберите папку для пакетной конвертации")
        self.status_batch.setObjectName("muted")

        layout.addWidget(QLabel("Папка"))
        layout.addLayout(folder_row)
        layout.addWidget(QLabel("Формат"))
        layout.addWidget(self.batch_format_box)
        layout.addWidget(QLabel("Качество"))
        layout.addWidget(self.batch_quality_slider)
        layout.addWidget(convert_btn)
        layout.addWidget(self.status_batch)
        layout.addStretch(1)
        return page

    def _switch_tab(self, index: int) -> None:
        self.stack.switch_to(index)
        if index == 0:
            self.single_tab_btn.setObjectName("tabActive")
            self.batch_tab_btn.setObjectName("tab")
        else:
            self.single_tab_btn.setObjectName("tab")
            self.batch_tab_btn.setObjectName("tabActive")
        self.style().unpolish(self.single_tab_btn)
        self.style().polish(self.single_tab_btn)
        self.style().unpolish(self.batch_tab_btn)
        self.style().polish(self.batch_tab_btn)

    def _pick_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if path:
            self.file_input.setText(path)

    def _pick_folder(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if path:
            self.folder_input.setText(path)

    def _emit_single_convert(self) -> None:
        self.convert_requested.emit(
            self.file_input.text().strip(),
            self.format_box.currentText(),
            self.quality_slider.value(),
        )

    def _emit_batch_convert(self) -> None:
        self.batch_requested.emit(
            self.folder_input.text().strip(),
            self.batch_format_box.currentText(),
            self.batch_quality_slider.value(),
        )

    def set_single_status(self, message: str, error: bool = False) -> None:
        self.status_single.setText(message)
        self.status_single.setProperty("error", error)
        self.style().unpolish(self.status_single)
        self.style().polish(self.status_single)

    def set_batch_status(self, message: str, error: bool = False) -> None:
        self.status_batch.setText(message)
        self.status_batch.setProperty("error", error)
        self.style().unpolish(self.status_batch)
        self.style().polish(self.status_batch)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            f"""
            QMainWindow, QWidget {{
                background: {BG_COLOR};
                color: {TEXT};
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 13px;
            }}
            #title {{
                font-size: 30px;
                font-weight: 800;
                color: white;
            }}
            #subtitle {{
                color: {MUTED};
                margin-bottom: 8px;
            }}
            #card {{
                background: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 18px;
            }}
            QLabel {{
                font-weight: 600;
            }}
            QLabel#muted {{
                color: {MUTED};
                font-weight: 500;
            }}
            QLabel#error="true" {{
                color: #ff7373;
            }}
            QLineEdit, QComboBox {{
                background: {SURFACE_ALT};
                border: 1px solid transparent;
                border-radius: 12px;
                padding: 10px 12px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 1px solid {ACCENT};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QPushButton {{
                background: {SURFACE_ALT};
                border: 1px solid transparent;
                border-radius: 12px;
                padding: 10px 14px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                border: 1px solid {ACCENT};
            }}
            QPushButton#primary {{
                background: {ACCENT};
                color: white;
            }}
            QPushButton#primary:hover {{
                background: {ACCENT_HOVER};
                border: none;
            }}
            QPushButton#tab, QPushButton#tabActive {{
                min-width: 120px;
            }}
            QPushButton#tabActive {{
                background: {ACCENT};
                color: white;
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                border-radius: 3px;
                background: #393939;
            }}
            QSlider::handle:horizontal {{
                background: {ACCENT};
                border: none;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            """
        )
