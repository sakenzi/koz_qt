# koz_qt

pyinstaller --add-data "views/exam_window/icons;views/exam_window/icons" --add-data "views/waiting_for_window/images;views/waiting_for_window/images" --onefile window.

-ts translations/kz.ts translations/en.ts

lrelease en.ts

pylupdate5 example.py -ts eng-ru.ts