# -*- coding: utf-8 -*-
import datetime
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from item import Item
from mainwindow import Ui_MainWindow
from model import Model, Delegate
from circle_stamp import circle_stamp
from py_poppler import pdftocairo, pdfinfo
from stamp import stamp

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        self.model_file = Model(self, Item())
        self.model_file.insertColumns(0, ['Name', 'Page size', 'Pixmap'])
        self.ui.tableViewFile.setModel(self.model_file)
        self.ui.tableViewFile.setItemDelegate(Delegate())
        
        self.model_stamp = Model(self, Item())
        self.model_stamp.insertColumns(0, ['Pixmap', 'x', 'y', 'width', 'height', 'Page size'])
        self.ui.tableViewStamp.setModel(self.model_stamp)
        self.ui.tableViewStamp.setItemDelegate(Delegate())
        for n, w in enumerate([50, 15, 15, 43, 43]):
            self.ui.tableViewStamp.setColumnWidth(n, w)
        
        self.ui.lineEdit_2.setText( str(datetime.date.today()) )

        self.preview_circle_stamp()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            suffixes = [ url for url in event.mimeData().urls() if not Path(url.toLocalFile()).suffix == '.pdf' ]
            if len(suffixes) == 0:
                event.accept()
                return
            event.ignore()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        self.paths_to_items([ Path(url.toLocalFile()) for url in event.mimeData().urls() ])

    def open_files(self):
        filenames = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open PDF file', '', 'PDF File (*.pdf)')
        if not filenames[0]:
            return
        self.paths_to_items( [ Path(filename) for filename in filenames[0] ])

    def paths_to_items(self, paths):
        # add file list
        self.model_file.removeRows(0, self.model_file.rowCount())
        self.model_file.insertRows(0, len(paths))
        for r, path in enumerate(paths):
            self.model_file.root_item.child(r).set_dict( pdfinfo(path) )
        
        # add stamp list
        page_sizes = set([ item.data('Page size') for item in self.model_file.root_item.children() ])
        self.model_stamp.removeRows(0, self.model_stamp.rowCount())
        self.model_stamp.insertRows(0, len(page_sizes))
        for r, page_size in enumerate(page_sizes):
            s = page_size.strip().split()
            w, h = int( float(s[0]) / 72.0*300.0 ), int( float(s[2]) / 72.0*300.0 )
            d = {'Page size':page_size, 'x':w/2.0, 'y':h/2.0, 'width':w, 'height':h}
            self.model_stamp.root_item.child(r).set_dict(d)

    def preview_circle_stamp(self):
        w, h = self.ui.doubleSpinBox_width.value(), self.ui.doubleSpinBox_height.value()
        circle_stamp('__temp__.pdf', (w+2.0, h+2.0), (w, h), ((w+2.0)/2.0, (h+2.0)/2.0), self.stamp_texts())
        pdftocairo(Path('__temp__.pdf'), '__temp__')
        
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QtGui.QPixmap('__temp__-1.png', 'PNG')
        scene.addPixmap(pixmap)
        Path('__temp__-1.png').unlink()
        Path('__temp__.pdf').unlink()

        self.ui.graphicsView_circle_stamp.setScene(scene)
        self.ui.graphicsView_circle_stamp.scale(1.0, 1.0)

    def preview_pdf(self):
        # pdf to pixmap
        index = self.ui.tableViewFile.selectedIndexes()[0]
        path = Path(index.internalPointer().data('Path'))
        scene = QtWidgets.QGraphicsScene(self)
        pdftocairo(path, path.stem)
        scene.addPixmap( QtGui.QPixmap(path.stem+'-1.png', 'PNG'))
        Path(path.stem+'-1.png').unlink()

        # stamp on view
        page_size = index.internalPointer().data('Page size')
        for item in self.model_stamp.root_item.children():
            if page_size == item.data('Page size'):
                if item.data('Pixmap') is None:
                    continue
                pixmap_item = scene.addPixmap(item.data('Pixmap'))
                pixmap_item.setPos(float(item.data('x')), float(item.data('y')))
                break

        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def stamp_texts(self):
        f = Path('C:/Windows/Fonts/msgothic.ttc')
        return [
            {'font_path':f, 'font_size':self.ui.doubleSpinBox.value(), 'text':self.ui.lineEdit.text()},
            {'font_path':f, 'font_size':self.ui.doubleSpinBox_2.value(), 'text':self.ui.lineEdit_2.text()},
            {'font_path':f, 'font_size':self.ui.doubleSpinBox_3.value(), 'text':self.ui.lineEdit_3.text()}
        ]

    def save_files(self):
        stamps = {}
        children = self.model_stamp.root_item.children()
        for n, item in enumerate(children):
            page_size = item.data('Page size')
            ps = page_size.strip().split()
            stamp_name = '__stamp' + str(n) + '__.pdf'
            circle_stamp(
                stamp_name, ( float(ps[0]), float(ps[2]) ), 
                ( self.ui.doubleSpinBox_width.value(), self.ui.doubleSpinBox_height.value() ), 
                ( float(item.data('x'))/300.0*72.0, (float(item.data('height'))-float(item.data('y')))/300.0*72.0 ), 
                self.stamp_texts()
            )
            stamps[page_size] = stamp_name
        
        # stamp to pdfs
        children = self.model_file.root_item.children()
        for item in children:
            file_path = Path(item.data('Path'))
            stamp_path = Path(stamps[item.data('Page size')])
            stamp(file_path, stamp_path, Path('output/'))
        
        # delete stamps
        for key in stamps:
            Path(stamps[key]).unlink()

    def set_stamp(self):
        # create stamp
        w, h = self.ui.doubleSpinBox_width.value(), self.ui.doubleSpinBox_height.value()
        circle_stamp('__temp__.pdf', (w+2.0, h+2.0), (w, h), ((w+2.0)/2.0, (h+2.0)/2.0), self.stamp_texts())
        pdftocairo(Path('__temp__.pdf'), '__temp__')
        pixmap = QtGui.QPixmap('__temp__-1.png', 'PNG')
        Path('__temp__-1.png').unlink()
        Path('__temp__.pdf').unlink()

        # update view
        scene = QtWidgets.QGraphicsScene(self)
        scene.addPixmap(pixmap)
        self.ui.graphicsView_circle_stamp.setScene(scene)
        self.ui.graphicsView_circle_stamp.scale(1.0, 1.0)

        # set item
        items = set([ index.internalPointer() for index in self.ui.tableViewStamp.selectedIndexes() ])
        for item in items:
            item.set_data('Pixmap', pixmap)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()
 
if __name__ == '__main__':
    main()
