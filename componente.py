from PySide6.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    Slot, Property)

from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter


class AnimatedToggle(QCheckBox):
    #defines la forma de los checkbox usando propiedades de la clase QPen
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    # se define los atributos y características de la clase
    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE"
        ):
        super().__init__(parent)
        # lo crea como barras
        self._bar_brush = QBrush(bar_color)
        # le da color cuando es checkeada
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())
        # hace que sean checkeables las barras
        self._handle_brush = QBrush(handle_color)
        # hace que la bola cambie de posición al ser checkeada y tenga su nuevo color
        self._handle_checked_brush = QBrush(QColor(checked_color))
        # hace que al deschekearse vuelva a su forma normal
        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        # hace el efecto del circulo parpadeante
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))
        #define margen
        self.setContentsMargins(8, 0, 8, 0)
        #marcas la posición que poseerá al principio el checkbox
        self._handle_position = 0
        #marcas el radio que poseerá el checkbox
        self._pulse_radius = 0
        # se define el cambio y efecto que se produce en la animación, que en este caso es la posición de la bola del check
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        # define como será el movimiento de la bola
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        # define el tiempo que tardará en producirse
        self.animation.setDuration(200)
        # defines la animación del parpadeo que realiza la bola al llegar a un extremo
        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        # defines el tiempo qur tardará en realizarlo
        self.pulse_anim.setDuration(350)
        # estableces desde donde comienza el parpadeo
        self.pulse_anim.setStartValue(10)
        # establece donde acaba el parpadeo
        self.pulse_anim.setEndValue(20)
        # metes las dos animaciones en una agrupación secuencial, que significa que primero hará una y luego la otra
        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)
        # conectas el estado con la función setup_animation para que haga el movimiento de la bola
        self.stateChanged.connect(self.setup_animation)
    # recibe el tamaño
    def sizeHint(self):
        return QSize(58, 45)
    # permite la pulsación del botón
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    #permite el movimiento de la bola dependiendo del estado de la animación, tras pulsarse el check
    # detecta si el movimiento es de desactivarse o activarse, y según la opción hace un movimiento u otro
    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        #defines el dibujo y la posición
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())
        # se define el recorrido de dibujo que hará
        p = QPainter(self)
        # se establece el recorrido
        p.setRenderHint(QPainter.Antialiasing)
        # se hace transparente los bordes
        p.setPen(self._transparent_pen)
        # se define la barra con sus características
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        # defines como será la barra al realizarse el movimiento
        barRect.moveCenter(contRect.center())
        # sacas variables matemáticas útiles para la animación del movimiento utilizando la posición, la barra, etc
        rounding = barRect.height() / 2
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position
        # hace que si la barra principal se desactiva, también desactiva la secundaria si estaba activada
        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)
        # da color y forma cuando se activa el check a la barra
        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
        # da color y forma antes de activar el check a la barra
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)
        # defines las características del dibujo
        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()
    # da forma al desactivar el check
    @Property(float)
    def handle_position(self):
        return self._handle_position
    # retorna la posición para que se mueva la bola
    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()
    # las dos funciones sirven para retornar la posición para el parpadeo de la bola
    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius
    
    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()