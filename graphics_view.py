from PyQt5 import QtCore, QtGui, QtWidgets

class GraphicsView(QtWidgets.QGraphicsView):

    def __init__(self, *argv, **keywords):
        super(GraphicsView, self).__init__(*argv, **keywords)
        self._numScheduledScalings = 0
        self.x0, self.y0, self.x1, self.y1 = 0, 0, 0, 0

    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15
        self._numScheduledScalings += numSteps
        if self._numScheduledScalings * numSteps < 0:
            self._numScheduledScalings = numSteps
        anim = QtCore.QTimeLine(350, self)
        anim.setUpdateInterval(20)
        anim.valueChanged.connect(self.scalingTime)
        anim.finished.connect(self.animFinished)
        anim.start()

    def scalingTime(self, x):
        factor = 1.0 + float(self._numScheduledScalings) / 300.0
        self.scale(factor, factor)

    def animFinished(self):
        if self._numScheduledScalings > 0:
            self._numScheduledScalings -= 1
        else:
            self._numScheduledScalings += 1
        
    def setScrollHandDragMode(self):
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def setRubberBandDragMode(self):
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        
    def exec_context_menu(self, point):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction('Pan mode', self.setScrollHandDragMode)
        self.menu.addAction('Select mode', self.setRubberBandDragMode)
        self.menu.exec( self.focusWidget().mapToGlobal(point) )
