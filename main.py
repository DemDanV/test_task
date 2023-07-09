import h5py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QItemDelegate, QFileDialog, QLabel, QPushButton
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
import numpy as np
import pyqtgraph as pg
import sys



class ComboBoxDelegate(QItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self, parent, option, index):
        """Меняем редактор 1 столбца в выпадающий список со значениями от 1 до 5"""
        if (index.column()==0):
            editor = QtWidgets.QComboBox(parent)
            editor.addItems([str(i) for i in range(1, 6)])
            return editor
        else:
            return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """Устанавливаем текст редактора в значение ячейки"""
        if (index.column()==0):
            value = index.model().data(index, Qt.DisplayRole)
            editor.setCurrentText(value)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        """Передаем введенное значение редактора модели"""
        if (index.column() == 0):
            value = editor.currentText()
            model.setData(index, value, Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)



class DataTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.dataChanged.connect(self.onDataChanged)
        self.arr = np.zeros((5, 5), dtype='f')
        
        
    def onDataChanged(self, startIndex, endIndex):
        """
        Проверяем нужно ли пресчитывать зависимые столбцы
        """
        
        # Проверяем внесены ли изменения в стобец от которого зависит значение другого столбца
        dependentColumn1 = 0
        if  self.checkInRange(dependentColumn1, startIndex, endIndex):
            if(self.columnCount() > 1):
                print("calculateSumColumn") 
                """Пересчитываем значения в зависимом столбце"""
                self.calculateSecondColumn(startIndex, endIndex)
                
        # Проверяем внесены ли изменения в стобец от которого зависит значение другого столбца
        dependentColumn1 = 1
        if  self.checkInRange(dependentColumn1, startIndex, endIndex):
            if(self.columnCount() > 2):
                print("calculateAccumulatedColumn") 
                # Пересчитываем значения в зависимом столбце
                self.calculateThirdColumn(startIndex, endIndex)

    def checkInRange(self, columnToCheck, startIndex, endIndex):
        """Проверка находится ли стобец в диапазоне

        Args:
            columnToCheck (int): проверяемый столбец
            startIndex (index): начало диапазона
            endIndex (index): конец диапазона

        Returns:
            bool: находится ли столбец в диапазоне
        """
        if  max(endIndex.column(), columnToCheck) == endIndex.column() and min(columnToCheck, startIndex.column()) == startIndex.column():
            return True
        else:
            return False
    
    def clear(self):
        """
        Очистка таблицы
        """
        self.arr = np.zeros((self.rowCount(), self.columnCount()), dtype='f')
        
        startIndex = self.index(0,0)
        endIndex = self.index(self.rowCount(), self.columnCount())
        print(self.rowCount(), self.columnCount())
        
        # Оповещение об изменении значений
        self.dataChanged.emit(startIndex, endIndex)
        # Оповещение об изменении размера таблицы
        self.layoutChanged.emit()
        
    
    def rowCount(self, index = None):
        """Возвращает количество строк"""
        return self.arr.shape[0]
        
    def columnCount(self, index = None):
        """Возвращает количество столбцов"""
        return self.arr.shape[1]
    
    def data(self, index, role):
        # Отображение данных
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return f"{self.arr[index.row(), index.column()]:.0f}"
            return str(self.arr[index.row(), index.column()])
        
        # Применение цвета к 3 столбцу
        if role == Qt.BackgroundRole and index.column() == 2:
            self.value = self.arr[index.row()][index.column()]
            if self.value >= 0.0:
                return QtGui.QColor(QtCore.Qt.green)
            else:
                return QtGui.QColor(QtCore.Qt.red)
            
    def setData(self, index, value, role=Qt.EditRole):
        """Устанавливаем значение в модели"""
        if role == Qt.EditRole and value:
            self.arr[index.row(), index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False
            
    def flags(self, index):
        col = index.column()
        #Нельзя редактировать 2 и 3 столбцы
        if col == 1 or col == 2:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
            
    def resize(self, rows, columns):
        """Изменить размер модели"""
        current_rows = self.rowCount()
        current_columns = self.columnCount()

        # Если текущий размер массива совпадает с новым размером, то не меняем
        if current_rows == rows and current_columns == columns: 
            return

        # Если текущее кол-во строк больше нового кол-ва строк, то удаляем лишние строки
        if current_rows > rows: 
            self.arr = np.delete(self.arr, np.s_[rows:], axis=0)
        # Если текущее кол-во строк меньше нового кол-ва строк, то добавляем новые строки с нулями
        elif current_rows < rows: 
            new_arr = np.zeros((rows - current_rows, current_columns))
            self.arr = np.concatenate((self.arr, new_arr), axis=0)

        # Если текущее кол-во cтолбцов больше нового кол-ва столбцов, то удаляем лишние столбцы
        if current_columns > columns:  
            self.arr = np.delete(self.arr, np.s_[columns:], axis=1)
        # Если текущее кол-во cтолбцов меньше нового кол-ва столбцов, то добавляем новые столбцы с нулями
        elif current_columns < columns:  
            new_arr = np.zeros((rows, columns - current_columns))
            self.arr = np.concatenate((self.arr, new_arr), axis=1)

        # Оповещение об изменении размера таблицы
        self.layoutChanged.emit()
        
        startIndex = self.index(current_rows,current_columns)
        endIndex = self.index(rows,columns)
        
        # Оповещение об изменении значений
        self.dataChanged.emit(startIndex, endIndex)
            
    def setRandom(self):
        """Заполнение таблицы случайными значениями выборки равномерно распределенной по полуоткрытому интервалу[-10, 10)"""
        rowsAmount = self.rowCount()
        columsAmount = self.columnCount()
        
        rng = np.random.default_rng()
        
        # Заполнение массива
        if(columsAmount > 0):
            self.arr[:,0] = rng.integers(low = 1, high= 5, size=(rowsAmount, ))
        if(columsAmount > 2):
            self.arr[:,3:] = rng.uniform(low= -10, high=10,size=(rowsAmount, columsAmount - 3))
        
        # Оповезение об изменении
        if(columsAmount > 0):
            startIndex = self.index(0, 0)
            endIndex = self.index(rowsAmount - 1, 0)
            self.dataChanged.emit(startIndex, endIndex)
        if(columsAmount > 2):
            startIndex = self.index(0,2)
            endIndex = self.index(rowsAmount - 1,columsAmount - 1)
            self.dataChanged.emit(startIndex, endIndex)
    
    def calculateSecondColumn(self, startIndex, endIndex):
        """Высчитывание значения второго столбца

        Args:
            startIndex (index): начало диапазона
            endIndex (index): конец диапазона
        """
        print("Calculated all")
        startRow = startIndex.row() 
        endRow = endIndex.row() 
        
        # Вычисление значений столбца
        if(self.columnCount() > 3):
            self.arr[startRow:(endRow + 1),1] = self.arr[startRow:(endRow + 1),0] + self.arr[startRow:(endRow + 1),3] 
        else:
            self.arr[startRow:(endRow + 1),1] = self.arr[startRow:(endRow + 1),0]
        
        startIndex = self.index(startRow,1)
        endIndex = self.index(endRow,1) 
        
        # Оповещение об изменении значений
        self.dataChanged.emit(startIndex, endIndex)
        
    def calculateThirdColumn(self, startIndex, endIndex):
        startRowIndex = startIndex.row()
        endRowIndex = endIndex.row()
        # Вычисление значений столбца
        self.arr[startRowIndex:(endRowIndex + 1),2] += self.arr[startRowIndex:(endRowIndex + 1),1]
        
        startIndex = self.index(startIndex.row(),2)
        endIndex = self.index(endIndex.row(),2)
        
        # Оповещение об изменении значений
        self.dataChanged.emit(startIndex, endIndex)
        
    def load(self, data):
        self.arr = data
        
        startIndex = self.index(0,0)
        endIndex = self.index(self.rowCount(), self.columnCount())
        
        # Оповещение об изменении размера таблицы
        self.layoutChanged.emit()
        # Оповещение об изменении значений
        self.dataChanged.emit(startIndex, endIndex)


        
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # Создание главного виджета
        self.verical_layout = QtWidgets.QVBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.verical_layout)
        self.setCentralWidget(self.main_widget)
        
        # Настройка окна
        self.setWindowTitle("Test Task")
        self.setGeometry(0,0, 1100, 900)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        # Создание таблицы
        self.data_table_view = QtWidgets.QTableView()
        self.verical_layout.addWidget(self.data_table_view)
        
        # Изменение поведения таблицы
        self.DTV_model = DataTableModel()
        self.DTV_delegate = ComboBoxDelegate()
        self.data_table_view.setModel(self.DTV_model)
        self.data_table_view.setItemDelegate(self.DTV_delegate) 

        # Создание виджета графика
        self.plotLabel = QLabel("Выберите два столбца для построения графика")
        self.plotLabel.setStyleSheet("color : grey;")
        self.verical_layout.addWidget(self.plotLabel)
        self.plotWidget = pg.plot(title="Three plot curves")
        self.verical_layout.addWidget(self.plotWidget)
        
        # Подписка графика на изменение таблицы
        self.data_table_view.selectionModel().selectionChanged.connect(self.checkToPlot)
        self.DTV_model.dataChanged.connect(self.checkToPlot)
        
        # Создание кнопок
        self.changeTableSizeButton = QPushButton("Изменить размер таблицы")
        self.loadButton = QPushButton("Загрузить")
        self.saveButton = QPushButton("Сохранить")
        self.randomButton = QPushButton("Заполнить случайными числами")
        self.resetButton = QPushButton("Сбросить")
        
        self.verical_layout.addWidget(self.changeTableSizeButton)
        self.verical_layout.addWidget(self.loadButton)
        self.verical_layout.addWidget(self.saveButton)
        self.verical_layout.addWidget(self.randomButton)
        self.verical_layout.addWidget(self.resetButton)
        
        # Добавление кнопкам функционал
        self.randomButton.clicked.connect(self.DTV_model.setRandom)
        self.resetButton.clicked.connect(self.DTV_model.clear)
        self.changeTableSizeButton.clicked.connect(self.resizeTable)
        self.loadButton.clicked.connect(self.loadFile)
        self.saveButton.clicked.connect(self.saveFile)
        
    def resizeTable(self):
        """Функция для изменения размера массива по клику кнопки"""
        # Получение нового размера массива от пользователя
        rows, rowsValid = QInputDialog.getInt(self, "Изменение размера", "Введите новое количество строк:")
        if rowsValid == False:
            return
        
        cols, columnsValid = QInputDialog.getInt(self, "Изменение размера", "Введите новое количество столбцов:")

        # Если пользователь нажал "ОК" в обоих диалоговых окнах
        if rowsValid and columnsValid:
            # Изменение размера модели данных
            self.DTV_model.resize(rows, cols)
        
        
    def loadFile(self):
        """
        Загрузка значений таблицы из файла
        """
        f_path = QFileDialog.getOpenFileName(self, "Выберите файл", "", "HDF5 Files (*.h5)")[0]
        if f_path:
            try:
                with h5py.File(f_path, 'r') as file:
                    data = file['matrix'][:]
                    self.DTV_model.load(data)
            except FileNotFoundError:
                pass

    def saveFile(self):
        """
        Сохранение значений таблицы в файл
        """
        f_path = QFileDialog.getSaveFileName(self, "Выберите файл", "", "HDF5 Files (*.h5)")[0]
        if f_path:
            try:
                with h5py.File(f_path, 'w') as file:
                    file.create_dataset('matrix', data=self.DTV_model.arr, dtype='f')
            except FileNotFoundError:
                pass
    
    def checkToPlot(self, selected, deselected):
        '''Находим индексы веделенных столбцов'''
        selectedColumns = self.data_table_view.selectionModel().selectedColumns()
        
        # Сравниваем количество выбранных столбцов
        if len(selectedColumns) == 2:
            # Строим график
            self.plotGraph()
        else:
            # Очищяем график
            self.plotWidget.clear()
        
    def plotGraph(self):
        """
        Построение графика зависимости второго выбранного столбца от первого
        """
        selectedColumns = self.data_table_view.selectionModel().selectedColumns()
        
        if len(selectedColumns) == 2:
            self.plotWidget.clear()
            self.plotWidget.plot(self.DTV_model.arr[:, selectedColumns[1].column()], self.DTV_model.arr[:, selectedColumns[0].column()], pen = 'red')
        
def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
    application()