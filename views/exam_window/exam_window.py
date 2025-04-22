from PyQt5.QtCore import QPropertyAnimation, QPoint, QSequentialAnimationGroup, QTimer, Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QLabel, QListWidget, QVBoxLayout, 
                             QHBoxLayout, QDialog, QPlainTextEdit, QTextEdit, QLineEdit, QComboBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPainter, QTextFormat, QKeyEvent
from PyQt5.QtCore import (QEvent, QSize, QRect, QProcess, QTextStream)
import time
import base64
import os
import sys
import tempfile
from controllers.exam_tasks_controller import ExamTasksController
from pathlib import Path


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TimerLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setGeometry(750, 300, 300, 300)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QLabel:hover { background-color: #4f565c; }
        """)


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 925)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QLabel:hover { background-color: #4f565c; }
            QLabel:pressed { background-color: #808a91; }
        """)


class ExitWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Растау")
        self.setGeometry(750, 300, 300, 300)
        self.setStyleSheet("""
            QDialog { background-color: #F5F5F5; border: 1px solid #E0E0E0; border-radius: 10px; }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        self.question_label = QLabel("Сіз шынымен шыққыңыз келеді ме?\n Мүмкін тапсырма жауаптарын бір тексеріп шығарсыз!")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setStyleSheet("QLabel { font-size: 16px; color: #333333; }")
        layout.addWidget(self.question_label)

        button_layout = QHBoxLayout(self)
        button_layout.setSpacing(10)

        self.yes_button = QPushButton("Иә, аяқтағым келеді\n Мен өзіме сенімдімін!")
        self.yes_button.setStyleSheet("""
            QPushButton { background-color: #FF4040; color: white; border-radius: 10px; padding: 8px 20px; font-size: 14px; border: 1px solid #FF4040; }
            QPushButton:hover { background-color: #c93a40; }
            QPushButton:pressed { background-color: #e80e17; }
        """)
        self.yes_button.clicked.connect(self.accept)
        button_layout.addWidget(self.yes_button)

        self.no_button = QPushButton("Өзіме сенімді емеспін,\n Тағы бір тексеріп алайын")
        self.no_button.setStyleSheet("""
            QPushButton { background-color: #1E90FF; color: white; border-radius: 10px; padding: 8px 20px; font-size: 14px; border: 1px solid #1E90FF; }
            QPushButton:hover { background-color: #104E8B; }
        """)
        self.no_button.clicked.connect(self.reject)
        button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)

    def exec(self):
        result = super().exec()
        return result == QDialog.DialogCode.Accepted

    def update_ui_texts(self):
        self.setWindowTitle(self.tr("Растау"))
        self.question_label.setText(self.tr("Сіз шынымен шыққыңыз келеді ме?\n Мүмкін тапсырма жауаптарын бір тексеріп шығарсыз!"))
        self.yes_button.setText(self.tr("Иә, аяқтағым келеді\n Мен өзіме сенімдімін!"))
        self.no_button.setText(self.tr("Өзіме сенімді емеспін,\n Тағы бір тексеріп алайын"))

class FullaImageWindow(QMainWindow):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.showFullScreen()
        self.setWindowTitle("Толық экранды сурет")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.image_label = QLabel(central_widget)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")
        pixmap = QPixmap(image_path)
        if pixmap and not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_label.setText("Сурет табылмады")
        layout.addWidget(self.image_label)
        self.image_label.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.image_label and event.type() == QEvent.Type.MouseButtonPress:
            self.close()
            return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)
        self.setStyleSheet("""
            QPlainTextEdit { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
        """)

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#343c42"))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.white)
                painter.drawText(
                    QPoint(self.line_number_area.width() - 5 - self.fontMetrics().horizontalAdvance(number),
                           int(top + self.fontMetrics().height())),
                    number
                )
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#343c42")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)


class ExamWindow(QMainWindow):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.controller = self.app_manager.get_controller()
        self.exam_controller = ExamTasksController(auth_controller=self.controller)

        self.setWindowTitle("Экзамен алаңы")
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setGeometry(50, 40, 1850, 800)
        self.setStyleSheet("""
            QMainWindow { background-color: #0c1214; border: thick double #32a1ce; border-radius: 20px; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.task_data = self.controller.get_task_data()
        self.task_files = self.task_data.option_file if self.task_data else []
        self.total_time = self.task_data.duration * 60 if self.task_data else 200
        self.notes = {}
        self.temp_image_paths = []
        self.exam_controller.set_task_data(self.task_data)
        self.exam_controller.start_monitoring()
        print(f"Room ID: {self.exam_controller.room_id}, Task Option ID: {self.exam_controller.task_option_id}")

        self.save_base64_images()

        self.image_label = ImageLabel()

        self.blue_widget = QWidget(self)
        self.blue_widget.resize(700, 1000)
        self.blue_widget.setStyleSheet("background-color: #252c30;")
        self.blue_widget.move(-700, -700)

        self.sidebar_layout = QVBoxLayout(self.blue_widget)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(10)

        self.sidebar_tasks_layout = QHBoxLayout()
        self.sidebar_tasks_layout.setSpacing(20)

        self.sidebar_title = QLabel("Тапсырмалар тізімі")
        self.sidebar_title.setStyleSheet("QLabel { color: white; font-size: 18px; font-weight: bold; }")
        self.sidebar_tasks_layout.addWidget(self.sidebar_title, stretch=2)

        self.sidebar_exit_button = QPushButton()
        self.sidebar_exit_button.resize(100, 10)
        self.sidebar_exit_button.setIcon(QIcon(resource_path('views/exam_window/icons/x.svg')))
        self.sidebar_exit_button.setStyleSheet("""
            QPushButton { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QPushButton:hover { background-color: #4f565c; }
            QPushButton:pressed { background-color: #808a91; }
        """)
        self.sidebar_exit_button.clicked.connect(self.sidebar_blue_widget)
        self.sidebar_tasks_layout.addWidget(self.sidebar_exit_button)

        self.task_list_font = QFont("", 20)
        self.task_list = QListWidget()
        self.task_list.setFont(self.task_list_font)
        self.task_list.setStyleSheet("""
            QListWidget { background-color: #343c42; color: white; border-radius: 10px; padding: 5px; }
            QListWidget::item:hover { background-color: #4f565c; }
            QListWidget::item:selected { background-color: #808a91; }
        """)
        for i, task in enumerate(self.task_files, 1):
            self.task_list.addItem(f"Тапсырма/Задание {i}")
        self.task_list.currentRowChanged.connect(self.change_task)

        self.sidebar_layout.addLayout(self.sidebar_tasks_layout)
        self.sidebar_layout.addWidget(self.task_list)

        tasks_exit_timer_layout = QHBoxLayout()
        timer_tasks_layout = QHBoxLayout()
        timer_tasks_layout.setSpacing(10)

        self.start_time = time.time()
        self.timer_label = TimerLabel(f"Тайминг: {self.total_time // 60}:{self.total_time % 60:02d}")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        timer_tasks_layout.addWidget(self.timer_label)

        self.sidebar_button = QPushButton(" Тапсырмалар")
        self.sidebar_button.setIcon(QIcon(resource_path('views/exam_window/icons/show-sidebar-horiz.svg')))
        self.sidebar_button.setStyleSheet("""
            QPushButton { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QPushButton:hover { background-color: #4f565c; }
            QPushButton:pressed { background-color: #808a91; }
        """)
        self.sidebar_button.clicked.connect(self.sidebar_blue_widget)
        timer_tasks_layout.addWidget(self.sidebar_button)
        timer_tasks_layout.addStretch()

        image_text_layout = QHBoxLayout()
        image_text_layout.setSpacing(20)

        notepad_layout = QVBoxLayout()
        notepad_layout.setSpacing(10)

        notepads_layout = QVBoxLayout()

        self.tab_bar = QWidget()
        self.tab_bar.setFixedHeight(30)
        self.tab_bar.setStyleSheet("""
            QWidget { background-color: #252526; border-bottom: 1px solid #3c3c3c; }
        """)
        tab_layout = QHBoxLayout(self.tab_bar)
        tab_layout.setContentsMargins(5, 0, 0, 0)
        tab_layout.setSpacing(5)

        self.tabs = []
        self.current_file = None
        self.add_tab("1.py")

        self.new_file_button = QPushButton("+")
        self.new_file_button.setFixedSize(30, 24)
        self.new_file_button.setStyleSheet("""
            QPushButton {
                background-color: #252526; 
                color: #d4d4d4; 
                border: none; 
                font-size: 14px; 
            }
            QPushButton:hover { background-color: #3c3c3c; }
            QPushButton:pressed { background-color: #4f565c; }
            }
        """)
        self.new_file_button.clicked.connect(self.toggle_new_file_combobox)
        tab_layout.addWidget(self.new_file_button)

        self.new_file_combobox = QComboBox()
        self.new_file_combobox.addItems(["New .py file", "New .txt file"])
        self.new_file_combobox.setFixedWidth(150)
        self.new_file_combobox.setStyleSheet("""
            QComboBox (
                background-color: #252526; 
                color: #d4d4d4; 
                border: 1px solid #3c3c3c; 
                padding: 5px; 
            }
            QComboBox::drop-down { border: none; }
            QComboBox::down-arrow { image: none; }
        """)
        self.new_file_combobox.setVisible(False)
        self.new_file_combobox.activated.connect(self.create_new_file)
        tab_layout.addWidget(self.new_file_combobox)
        tab_layout.addStretch()

        terminal_layout = QVBoxLayout()
        terminal_input_and_button_layout = QHBoxLayout()
        terminal_input_layout = QHBoxLayout()
        terminal_button_layout = QHBoxLayout()

        image_layout = QHBoxLayout()
        image_layout.setSpacing(10)

        if self.temp_image_paths:
            pixmap = QPixmap(self.temp_image_paths[0])
            if pixmap and not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio))
            else:
                self.image_label.setText("Сурет табылмады")
        else:
            self.image_label.setText("Сурет табылмады")
        self.image_label.mousePressEvent = self.show_fullscreen_image
        image_layout.addWidget(self.image_label)

        self.notepad = CodeEditor()
        self.notepad.setPlaceholderText("Тапсырманы жазыңыз")
        self.load_python_file("1.py")
        self.notepad.textChanged.connect(self.save_notepad_text)
        notepad_layout.addWidget(self.tab_bar)
        notepads_layout.addWidget(self.notepad, stretch=1)

        self.process = QProcess()
        self.output = QTextEdit()
        self.output.setStyleSheet("""
            QTextEdit { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QTextEdit:hover { background-color: #4f565c; }
            QTextEdit:pressed { background-color: #808a91; }
        """
        )
        self.input = QLineEdit()
        self.input.setStyleSheet("""
            QLineEdit { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QLineEdit:hover { background-color: #4f565c; }
            QLineEdit:pressed { background-color: #808a91; }
        """)
        self.run_command_button = QPushButton("run", self)
        self.run_command_button.setStyleSheet("""
            QPushButton { background-color: #7ccf80; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QPushButton:hover { background-color: #195c1c; }
            QPushButton:pressed { background-color: #166e1a; }
        """)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.run_command_button.clicked.connect(self.run_command)
        self.process.start("cmd.exe")

        terminal_input_layout.addWidget(self.input)
        terminal_button_layout.addWidget(self.run_command_button)
        terminal_input_and_button_layout.addLayout(terminal_input_layout)
        terminal_input_and_button_layout.addLayout(terminal_button_layout)
        terminal_layout.addLayout(terminal_input_and_button_layout)  
        terminal_layout.addWidget(self.output)

        image_text_layout.addLayout(image_layout)
        image_text_layout.addLayout(notepad_layout)
        notepad_layout.addLayout(notepads_layout)
        notepads_layout.addLayout(terminal_layout)

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()

        self.exit_button = QPushButton("Аяқтау")
        self.exit_button.setIcon(QIcon(resource_path("views/exam_window/icons/free-exit-icon-2860-thumb.png")))
        self.exit_button.setStyleSheet("""
            QPushButton { background-color: #c42329; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QPushButton:hover { background-color: #c93a40; }
            QPushButton:pressed { background-color: #e80e17; }
        """)
        self.exit_button.clicked.connect(self.on_exit_clicked)
        exit_layout.addWidget(self.exit_button)

        tasks_exit_timer_layout.addLayout(timer_tasks_layout)
        tasks_exit_timer_layout.addLayout(exit_layout)
        main_layout.addLayout(tasks_exit_timer_layout)
        main_layout.addLayout(image_text_layout, stretch=1)

        if self.task_files:
            self.task_list.setCurrentRow(0)
            self.change_task(0)

        self.update_ui_texts()

    def add_tab(self, file_name):
        tab_label = QLabel(file_name)
        tab_label.setStyleSheet("""
            QLabel {
                background-color: #252526; 
                color: #d4d4d4; 
                padding: 5px 15px; 
                font-family: 'Consolas', 'Courier New', monospace; 
                font-size: 12px; 
                border-right: 1px solid #3c3c3c;
                border-top: 2px solid #007acc;
            }
        """)
        tab_label.mousePressEvent = lambda event: self.switch_tab(file_name)
        self.tabs.append((file_name, tab_label))
        tab_layout = self.tab_bar.layout()
        tab_layout.insertWidget(len(self.tabs) - 1, tab_label)
        self.current_file = file_name

    def switch_tab(self, file_name):
        self.current_file = file_name
        self.load_python_file(file_name)
        for fname, label in self.tabs:
            if fname == file_name:
                label.setStyleSheet("""
                    QLabel { 
                        background-color: #252526; 
                        color: #d4d4d4; 
                        padding: 5px 15px; 
                        font-family: 'Consolas', 'Courier New', monospace; 
                        font-size: 12px; 
                        border-right: 1px solid #3c3c3c;
                        border-top: 2px solid #007acc;
                    }
                """)
            else:
                label.setStyleSheet("""
                    QLabel { 
                        background-color: #252526; 
                        color: #858585; 
                        padding: 5px 15px; 
                        font-family: 'Consolas', 'Courier New', monospace; 
                        font-size: 12px; 
                        border-right: 1px solid #3c3c3c;
                        border-top: none;
                    }
                """)
    
    def toggle_new_file_combobox(self):
        self.new_file_combobox.setVisible(not self.new_file_combobox.isVisible())
        if self.new_file_combobox.isVisible():
            self.new_file_combobox.showPopup()

    def create_new_file(self, index):
        file_type = ".py" if index == 0 else ".txt"
        home_dir = Path.home()
        project_folder = home_dir / "koz_project"
        project_folder.mkdir(exist_ok=True)

        i = 1
        while (project_folder / f"file{i}{file_type}").exists():
            i += 1
        new_file = project_folder / f"file{i}{file_type}"

        try: 
            new_file.touch()
            print(f"created file: {new_file}")  
            self.add_tab(new_file.name)
            self.load_python_file(new_file.name)
        except Exception as e:
            print(f"Error creating file {new_file}: {e}")
        self.new_file_combobox.setVisible(False)
    
    def load_python_file(self, file_name):
        home_dir = Path.home()
        project_folder = home_dir / "koz_project"
        file_path = project_folder / file_name
        try:
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.notepad.setPlainText(content)
                print(f"File 1.py: {file_path}")
            else:
                self.notepad.setPlainText("")
                print(f"File 1.py not found: {file_path}")
            self.current_file = file_name
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")

    def save_notepad_text(self):
        if not self.current_file:
            return
        current_index = self.task_list.currentRow()
        if current_index >= 0:
            text = self.notepad.toPlainText()
            self.notes[current_index] = text
            self.exam_controller.add_answer(current_index + 1, text)
            home_dir = Path.home()
            project_folder  =home_dir / "koz_project"
            file_path = project_folder / self.current_file
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"File saved: {file_path}")
            except Exception as e:
                print(f"Error saving file: {file_path}: {e}")

    def update_ui_texts(self):
        self.setWindowTitle(self.tr("Экзамен алаңы"))
        self.sidebar_title.setText(self.tr("Тапсырмалар тізімі"))
        self.sidebar_button.setText(self.tr(" Тапсырмалар"))
        self.notepad.setPlaceholderText(self.tr("Тапсырманы жазыңыз"))
        self.exit_button.setText(self.tr("Аяқтау"))
        
    def read_output(self):
        stream = QTextStream(self.process)
        self.output.append(stream.readAll())

    def run_command(self):
        command = self.input.text() + "\n"
        self.process.write(command.encode())
        
    def save_base64_images(self):
        if not self.task_files:
            return
        for i, task in enumerate(self.task_files):
            base64_data = task.get("file_base64")
            if not base64_data:
                self.temp_image_paths.append(None)
                continue
            try:
                if isinstance(base64_data, list) and len(base64_data) > 0:
                    base64_string = base64_data[0]
                else:
                    base64_string = base64_data

                if isinstance(base64_string, str):
                    if base64_string.startswith("data:image"):
                        base64_string = base64_string.split(",")[1]
                    image_data = base64.b64decode(base64_string)
                    extension = ".jpeg" if "jpeg" in task["file_path"].lower() else ".png"
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
                    temp_file.write(image_data)
                    temp_file.close()
                    self.temp_image_paths.append(temp_file.name)
                else:
                    raise ValueError("Base64 данные не являются строкой")
            except Exception as e:
                print(f"Ошибка декодирования Base64 для задачи {i + 1}: {e}")
                self.temp_image_paths.append(None)

    def cleanup_temp_files(self):
        for path in self.temp_image_paths:
            if path and os.path.exists(path):    
                os.unlink(path)

    def change_task(self, index):
        if 0 <= index < len(self.temp_image_paths):
            pixmap = QPixmap(self.temp_image_paths[index])
            if pixmap and not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio))
            else:
                self.image_label.setText(f"Сурет табылмады: {self.task_files[index]['file_path']}")
            self.notepad.blockSignals(True)
            self.notepad.setPlainText(self.notes.get(index, ""))
            self.notepad.blockSignals(False)

    def sidebar_blue_widget(self):
        anim_group = QSequentialAnimationGroup(self)
        if self.blue_widget.x() < 0:
            anim = QPropertyAnimation(self.blue_widget, b"pos")
            anim.setDuration(700)
            anim.setStartValue(QPoint(-700, 0))
            anim.setEndValue(QPoint(0, 0))
            anim_group.addAnimation(anim)
        else:
            anim = QPropertyAnimation(self.blue_widget, b"pos")
            anim.setDuration(700)
            anim.setStartValue(QPoint(0, 0))
            anim.setEndValue(QPoint(-700, 0))
            anim_group.addAnimation(anim)
        anim_group.start(QPropertyAnimation.DeleteWhenStopped)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        remaining_time = self.total_time - elapsed
        if remaining_time >= 0:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.timer_label.setText(f"Тайминг: {minutes}:{seconds:02d}")
        else:
            self.timer_label.setText("Тайминг: 0:00")
            self.timer.stop()
            self.submit_and_close()

    def on_exit_clicked(self):
        exit_window = ExitWindow(self)
        exit_window.update_ui_texts()
        if exit_window.exec():
            self.submit_and_close()

    def submit_and_close(self):
        self.exam_controller.stop_monitoring()
        token = self.controller.get_token()
        if not token:
            self.cleanup_temp_files()
            self.close()
            return

        exam_result = self.exam_controller.get_exam_result()
        data_to_send = exam_result.to_dict()
        print("Фактически отправляемые данные:", data_to_send)
        
        if self.exam_controller.submit_result(token):
            print("Результаты отправлены успешно")
        else:
            print("Ошибка при отправке результатов")
        self.cleanup_temp_files()
        self.close()

    def show_fullscreen_image(self, event):
        current_index = self.task_list.currentRow()
        if current_index >= 0 and self.temp_image_paths[current_index]:
            fullscreen_window = FullaImageWindow(self.temp_image_paths[current_index], self)
            fullscreen_window.show()

    def closeEvent(self, event):
        self.exam_controller.stop_monitoring()
        self.cleanup_temp_files()
        super().closeEvent(event)