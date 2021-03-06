#!/usr/bin/env python

# The Python version of qwt-*/examples/curvdemo2


from lib import *

Size=15
USize=13

class CurveDemo(QFrame):

    def __init__(self, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.setMidLineWidth(3)

        p = QPalette()
        p.setColor(self.backgroundRole(), QColor(30, 30, 50))
        self.setPalette(p)
        # make curves and maps
        self.tuples = []
        # curve 1
        curve = Qwt.QwtPlotCurve()
        curve.setPen(QPen(QColor(150, 150, 200), 2))
        curve.setCurveType(Qwt.QwtPlotCurve.Xfy)
        curve.setStyle(Qwt.QwtPlotCurve.Lines)
        curveFitter = Qwt.QwtSplineCurveFitter()
        curveFitter.setSplineSize(150)
        curve.setCurveFitter(curveFitter)
        curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.XCross,
                                      QBrush(),
                                      QPen(Qt.yellow, 2),
                                      QSize(7, 7)))
        self.tuples.append((curve,
                            Qwt.QwtScaleMap(0, 100, -1.5, 1.5),
                            Qwt.QwtScaleMap(0, 100, 0.0, 2*pi)))
        # curve 2
        curve = Qwt.QwtPlotCurve()
        curve.setPen(QPen(QColor(200, 150, 50),
                                1,
                                Qt.DashDotDotLine))
        curve.setStyle(Qwt.QwtPlotCurve.Sticks)
        curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,
                                      QBrush(Qt.blue),
                                      QPen(Qt.yellow),
                                      QSize(5, 5)))
        self.tuples.append((curve,
                            Qwt.QwtScaleMap(0, 100, 0.0, 2*pi),
                            Qwt.QwtScaleMap(0, 100, -3.0, 1.1)))
        # curve 3
        curve = Qwt.QwtPlotCurve()
        curve.setPen(QPen(QColor(100, 200, 150)))
        curve.setStyle(Qwt.QwtPlotCurve.Lines)
        curve.setCurveAttribute(Qwt.QwtPlotCurve.Fitted)
        curveFitter = Qwt.QwtSplineCurveFitter()
        curveFitter.setFitMode(Qwt.QwtSplineCurveFitter.ParametricSpline)
        curveFitter.setSplineSize(200)
        curve.setCurveFitter(curveFitter)
        self.tuples.append((curve,
                            Qwt.QwtScaleMap(0, 100, -1.1, 3.0),
                            Qwt.QwtScaleMap(0, 100, -1.1, 3.0)))
        # curve 4
        curve = Qwt.QwtPlotCurve()
        curve.setPen(QPen(Qt.red))
        curve.setStyle(Qwt.QwtPlotCurve.Lines)
        curve.setCurveAttribute(Qwt.QwtPlotCurve.Fitted)
        curveFitter = Qwt.QwtSplineCurveFitter()
        curveFitter.setSplineSize(200)
        curve.setCurveFitter(curveFitter)
        self.tuples.append((curve,
                            Qwt.QwtScaleMap(0, 100, -5.0, 1.1),
                            Qwt.QwtScaleMap(0, 100, -1.1, 5.0)))
        # data
        self.phase = 0.0
        self.base = arange(0.0, 2.01*pi, 2*pi/(USize-1))
        self.uval = cos(self.base)
        self.vval = sin(self.base)
        self.uval[1::2] *= 0.5
        self.vval[1::2] *= 0.5
        self.newValues()
        # start timer
        self.tid = self.startTimer(250)

    # __init__()

    def paintEvent(self, event):
        QFrame.paintEvent(self,event)
        painter = QPainter(self)
        #painter.setRenderHint(QPainter.Antialiasing)
        painter.setClipRect(self.contentsRect())
        self.drawContents(painter)

    # paintEvent()

    def drawContents(self, painter):
        r = self.contentsRect()
        for curve, xMap, yMap in self.tuples:
            xMap.setPaintInterval(r.left(), r.right())
            yMap.setPaintInterval(r.top(), r.bottom())
            curve.draw(painter, xMap, yMap, r)

    # drawContents()

    def timerEvent(self, event):
        self.newValues()
        self.repaint()
        
    def newValues(self):
        phase = self.phase
        
        self.xval = arange(0, 2.01*pi, 2*pi/(Size-1))
        self.yval = sin(self.xval - phase)
        self.zval = cos(3*(self.xval + phase))
    
        s = 0.25 * sin(phase)
        c = sqrt(1.0 - s*s)
        u = self.uval
        self.uval = c*self.uval-s*self.vval
        self.vval = c*self.vval+s*u

        self.tuples[0][0].setData(self.yval, self.xval)
        self.tuples[1][0].setData(self.xval, self.zval)
        self.tuples[2][0].setData(self.yval, self.zval)
        self.tuples[3][0].setData(self.uval, self.vval)
        
        self.phase += 2*pi/100
        if self.phase>2*pi:
            self.phase = 0.0


def make():
    demo = CurveDemo()
    demo.resize(300, 300)
    demo.show()
    return demo

# make()


def main(args):
    app = QApplication(args)
    demo = make()
    sys.exit(app.exec_())

# main()

 
# Admire!         
if __name__ == '__main__':
    main(sys.argv)

# Local Variables: ***
# mode: python ***
# End: ***
