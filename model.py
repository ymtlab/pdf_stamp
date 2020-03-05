# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui

class Model(QtCore.QAbstractItemModel):
    def __init__(self, parent_=None, root_item=None):
        super(Model, self).__init__(parent_)
        self.root_item = root_item
        self._columns = []

    def columns(self):
        return self._columns

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._columns)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            return item.data( self._columns[index.column()] )
        if role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            data = item.data( self._columns[index.column()] )
            return data
        return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, i, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._columns[i]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return i + 1
 
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()
 
    def insertColumns(self, start_column, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns( parent, start_column, start_column + len(columns) - 1 )
        self._columns[ start_column : start_column + len(columns) - 1 ] = columns
        self.endInsertColumns()

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent == QtCore.QModelIndex():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        self.beginInsertRows(parent, row, row + count - 1)
        parent_item.insert_children(row, count)
        self.endInsertRows()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.root_item:
            return QtCore.QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)
        
    def removeColumns(self, column, count, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, column, column + count - 1)
        del self._columns[column : column + count]
        self.endRemoveColumns()

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        self.beginRemoveRows(parent, row, row + count - 1)
        parent_item.remove_children(row, count)
        self.endRemoveRows()
 
    def rowCount(self, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if value == 'None':
                index.internalPointer().clear(self._columns[index.column()])
            else:
                index.internalPointer().set_data( self._columns[index.column()], value )
            return True
        return False

class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, setModelDataEvent=None):
        super(Delegate, self).__init__(parent)
        self.setModelDataEvent = setModelDataEvent
 
    def createEditor(self, parent, option, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        if value is None:
            return QtWidgets.QLineEdit(parent)
        if type(value) in [ str, int, float ]:
            return QtWidgets.QLineEdit(parent)
        return
 
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        if value is None:
            editor.setText(str(value))
            return
        if type(value) in [ str, int, float ]:
            editor.setText(str(value))
            return
        return
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        if not self.setModelDataEvent is None:
            self.setModelDataEvent()
        
    def paint(self, painter, option, index):
        data = index.model().data(index)
        if type(data) is QtGui.QPixmap:
            # cell size
            r = option.rect
            x, y, w, h = r.x(), r.y(), r.width(), r.height()
            
            # image size
            w2, h2 = data.size().width(), data.size().height()
            
            # aspect rasio
            r1, r2 = w / h, w2 / h2
            
            if r1 < r2:
                h = w / r2
            else:
                w = h * r2
            
            pixmap2 = data.scaled(w, h, QtCore.Qt.KeepAspectRatio)
            rect = QtCore.QRect(x, y, w, h)
            painter.drawPixmap(rect, pixmap2)
        super(Delegate, self).paint(painter, option, index)
