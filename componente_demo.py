from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from animated_toggle import AnimatedToggle

app = QApplication([])

window = QWidget()

# se define el check principal
mainToggle = AnimatedToggle()
# se define el check secundario y sus propiedades
secondaryToggle = AnimatedToggle(
        checked_color="#FFB000",
        pulse_checked_color="#44FFB000"
)
# definición del tamaño que ocupará la caja
mainToggle.setFixedSize(mainToggle.sizeHint())
secondaryToggle.setFixedSize(mainToggle.sizeHint())

#mainToggle.setFocusPolicy(Qt.NoFocus)
#secondaryToggle.setFocusPolicy(Qt.NoFocus)

# se define el layout que se usará para los checkbox
window.setLayout(QVBoxLayout())
window.layout().addWidget(QLabel("Main Toggle"))
window.layout().addWidget(mainToggle)

window.layout().addWidget(QLabel("Secondary Toggle"))
window.layout().addWidget(secondaryToggle)

#vinculas el check principal con el secundario
mainToggle.stateChanged.connect(secondaryToggle.setChecked)

window.show()
app.exec()