from PyQt5.QtCore import QPropertyAnimation, QPoint, QSequentialAnimationGroup, QTimer, Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QDialog, QPlainTextEdit, QTextEdit)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPainter, QTextFormat, QImage
from PyQt5.QtCore import (QEvent, QSize, QRect)
import time
import base64
import os
import tempfile
from controllers.exam_tasks_controller import ExamTasksController

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

        question_label = QLabel("Сіз шынымен шыққыңыз келеді ме?\n Мүмкін тапсырма жауаптарын бір тексеріп шығарсыз!")
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setStyleSheet("QLabel { font-size: 16px; color: #333333; }")
        layout.addWidget(question_label)

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

        no_button = QPushButton("Өзіме сенімді емеспін,\n Тағы бір тексеріп алайын")
        no_button.setStyleSheet("""
            QPushButton { background-color: #1E90FF; color: white; border-radius: 10px; padding: 8px 20px; font-size: 14px; border: 1px solid #1E90FF; }
            QPushButton:hover { background-color: #104E8B; }
        """)
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)

    def exec(self):
        result = super().exec()
        return result == QDialog.DialogCode.Accepted

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
        self.temp_image_paths = []  # Список для хранения путей к временным файлам
        self.exam_controller.set_task_data(self.task_data)
        self.exam_controller.start_monitoring()
        print(f"Room ID: {self.exam_controller.room_id}, Task Option ID: {self.exam_controller.task_option_id}")

        # Создаём временные файлы из Base64
        self.save_base64_images()

        self.blue_widget = QWidget(self)
        self.blue_widget.resize(700, 1000)
        self.blue_widget.setStyleSheet("background-color: #252c30;")
        self.blue_widget.move(-700, -700)

        sidebar_layout = QVBoxLayout(self.blue_widget)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)

        sidebar_tasks_layout = QHBoxLayout()
        sidebar_tasks_layout.setSpacing(20)

        sidebar_title = QLabel("Тапсырмалар тізімі")
        sidebar_title.setStyleSheet("QLabel { color: white; font-size: 18px; font-weight: bold; }")
        sidebar_tasks_layout.addWidget(sidebar_title, stretch=2)

        self.sidebar_exit_button = QPushButton()
        self.sidebar_exit_button.resize(100, 10)
        self.sidebar_exit_button.setIcon(QIcon('exam_window/icons/x.svg'))
        self.sidebar_exit_button.setStyleSheet("""
            QPushButton { background-color: #343c42; color: white; border-radius: 15px; padding: 12px; font-size: 16px; border: none; }
            QPushButton:hover { background-color: #4f565c; }
            QPushButton:pressed { background-color: #808a91; }
        """)
        self.sidebar_exit_button.clicked.connect(self.sidebar_blue_widget)
        sidebar_tasks_layout.addWidget(self.sidebar_exit_button)

        self.task_list_font = QFont("", 20)
        self.task_list = QListWidget()
        self.task_list.setFont(self.task_list_font)
        self.task_list.setStyleSheet("""
            QListWidget { background-color: #343c42; color: white; border-radius: 10px; padding: 5px; }
            QListWidget::item:hover { background-color: #4f565c; }
            QListWidget::item:selected { background-color: #808a91; }
        """)
        for i, task in enumerate(self.task_files, 1):
            self.task_list.addItem(f"Тапсырма {i}")
        self.task_list.currentRowChanged.connect(self.change_task)

        sidebar_layout.addLayout(sidebar_tasks_layout)
        sidebar_layout.addWidget(self.task_list)

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
        self.sidebar_button.setIcon(QIcon('exam_window/icons/show-sidebar-horiz.svg'))
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

        self.image_label = ImageLabel()
        if self.temp_image_paths:
            pixmap = QPixmap(self.temp_image_paths[0])
            if pixmap and not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio))
            else:
                self.image_label.setText("Сурет табылмады")
        else:
            self.image_label.setText("Сурет табылмады")
        self.image_label.mousePressEvent = self.show_fullscreen_image
        image_text_layout.addWidget(self.image_label)

        self.notepad = CodeEditor()
        self.notepad.setPlaceholderText("Тапсырманы жазыңыз")
        self.notepad.textChanged.connect(self.save_notepad_text)
        image_text_layout.addWidget(self.notepad, stretch=1)

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()

        self.exit_button = QPushButton("Аяқтау")
        self.exit_button.setIcon(QIcon("exam_window/icons/free-exit-icon-2860-thumb.png"))
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

    def save_base64_images(self):
        """Сохраняем изображения из file_base64 во временные файлы"""
        if not self.task_files:
            return
        for i, task in enumerate(self.task_files):
            base64_data = task.get("file_base64")
            if not base64_data:
                print(f"Base64 данные отсутствуют для задачи {i + 1}")
                self.temp_image_paths.append(None)
                continue
            try:
                # Предполагаем, что file_base64 — список, берём первый элемент
                if isinstance(base64_data, list) and len(base64_data) > 0:
                    base64_string = base64_data[0]  # Берём первую строку из списка
                else:
                    base64_string = base64_data  # Если не список, используем как есть

                # Если строка с префиксом "data:image/...", убираем его
                if isinstance(base64_string, str):
                    if base64_string.startswith("data:image"):
                        base64_string = base64_string.split(",")[1]
                    image_data = base64.b64decode(base64_string)
                    # Определяем расширение из file_path
                    extension = ".jpeg" if "jpeg" in task["file_path"].lower() else ".png"
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
                    temp_file.write(image_data)
                    temp_file.close()
                    self.temp_image_paths.append(temp_file.name)
                    print(f"Сохранено изображение: {temp_file.name}")
                else:
                    raise ValueError("Base64 данные не являются строкой")
            except Exception as e:
                print(f"Ошибка декодирования Base64 для задачи {i + 1}: {e}")
                self.temp_image_paths.append(None)

    def cleanup_temp_files(self):
        """Удаляем временные файлы"""
        for path in self.temp_image_paths:
            if path and os.path.exists(path):
                try:
                    os.unlink(path)
                    print(f"Удалён файл: {path}")
                except Exception as e:
                    print(f"Ошибка удаления файла {path}: {e}")

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

    def save_notepad_text(self):
        current_index = self.task_list.currentRow()
        if current_index >= 0:
            text = self.notepad.toPlainText()
            self.notes[current_index] = text
            self.exam_controller.add_answer(current_index + 1, text)

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
        if exit_window.exec():
            self.submit_and_close()

    def submit_and_close(self):
        self.exam_controller.stop_monitoring()
        token = self.controller.get_token()
        if not token:
            print("Ошибка: Токен не найден")
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
        self.cleanup_temp_files()  # Удаляем файлы перед закрытием
        self.close()

    def show_fullscreen_image(self, event):
        current_index = self.task_list.currentRow()
        if current_index >= 0 and self.temp_image_paths[current_index]:
            fullscreen_window = FullaImageWindow(self.temp_image_paths[current_index], self)
            fullscreen_window.show()

    def closeEvent(self, event):
        self.exam_controller.stop_monitoring()
        self.cleanup_temp_files()  # Удаляем файлы при любом закрытии окна
        super().closeEvent(event)