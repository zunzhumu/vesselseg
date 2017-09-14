import sys

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QObject
from mainwindow import MainWindow
from managers import ImageManager, ViewManager, SegmentManager, TubeManager

class VesselSegApp(QObject):

    def __init__(self, parent=None):
        super(VesselSegApp, self).__init__(parent)

        self.qapp = QApplication(sys.argv)
        self.window = MainWindow()
        self.imageManager = ImageManager()
        self.tubeManager = TubeManager()
        self.viewManager = ViewManager(self.window)
        self.segmentManager = SegmentManager()

        self.viewManager.setSegmentScale(self.segmentManager.scale())

        self.viewManager.fileSelected.connect(self.loadFile)
        self.viewManager.imageVoxelSelected.connect(self.segmentTube)
        self.viewManager.scaleChanged.connect(self.segmentManager.setScale)
        self.imageManager.imageLoaded.connect(self.viewManager.displayImage)
        self.imageManager.imageLoaded.connect(self.segmentManager.setImage)
        self.imageManager.imageLoaded.connect(
                lambda _: self.tubeManager.reset())
        self.segmentManager.tubeSegmented.connect(
                self.tubeManager.addSegmentedTube)

    def run(self):
        '''Runs the application.

        Returns:
            An integer representing the termination state.
        '''
        self.window.show()
        return self.qapp.exec_()

    def loadFile(self, qfilename):
        filename = qfilename.toLatin1().data()
        if self.imageManager.loadImage(filename):
            return
        else:
            self.viewManager.alert('File %s could not opened' % filename)

    def segmentTube(self, x, y, z):
        if self.viewManager.isSegmentEnabled():
            self.segmentManager.segmentTube(x, y, z)

if __name__ == '__main__':
    app = VesselSegApp()
    sys.exit(app.run())
