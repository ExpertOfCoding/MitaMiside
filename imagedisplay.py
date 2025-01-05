import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QPoint, QSequentialAnimationGroup
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QDesktopWidget,QWidget
import random

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animations = []  # Keep references to animations

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Label clicked!")
            self.show_floating_image(event.pos())

    def show_floating_image(self, click_position):
        # Create a new label for the floating image
        floating_label = QLabel(self.parent())
        floating_pixmap = QPixmap('kalp.png').scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Remove background from the pixmap
        transparent_pixmap = QPixmap(128, 128)
        transparent_pixmap.fill(Qt.transparent)
        painter = QPainter(transparent_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, floating_pixmap)
        painter.end()

        floating_label.setPixmap(transparent_pixmap)

        image_width = self.width()
        image_height = self.height()
    
        # Floating label'ın boyutlarını al
        label_width = floating_label.width()
        label_height = floating_label.height()
    
        # Resmin iç kısmında, kenarlara yakın bir alan belirle
        margin = 20  # Kenardan ne kadar uzaklıkta olacağını belirler
        min_x = margin
        max_x = image_width - label_width - margin
        min_y = margin
        max_y = image_height - label_height - margin
    
        # Belirlenen alan içinde rastgele bir nokta oluştur
        random_x = random.randint(min_x, max_x)
        random_y = random.randint(min_y, max_y)
        floating_label.setGeometry(random_x, random_y, 128, 128)
        floating_label.show()

        # Create animation for the floating image's upward movement with slight horizontal oscillation
        animation_group = QSequentialAnimationGroup(self)

        start_geometry = floating_label.geometry()
        for i in range(5):  # Add slight oscillations during upward movement
            x_offset = random.choice([-10, 10])
            target_rect = QRect(
                max(0, min(self.parent().width() - 128, start_geometry.x() + x_offset)),
                max(0, start_geometry.y() - 40 * (i + 1)),
                128, 128
            )
            movement_animation = QPropertyAnimation(floating_label, b'geometry')
            movement_animation.setDuration(400)  # Duration for each segment
            movement_animation.setStartValue(start_geometry)
            movement_animation.setEndValue(target_rect)
            animation_group.addAnimation(movement_animation)
            start_geometry = target_rect

        # Opacity animation
        opacity_animation = QPropertyAnimation(floating_label, b'windowOpacity')
        opacity_animation.setDuration(1000)
        opacity_animation.setStartValue(1.0)
        opacity_animation.setEndValue(0.0)
        animation_group.addAnimation(opacity_animation)

        # Start the animation group
        animation_group.finished.connect(floating_label.deleteLater)
        animation_group.start()

        # Keep a reference to the animation group
        self.animations.append(animation_group)

        # Clean up finished animations
        self.animations = [anim for anim in self.animations if anim.state() != QPropertyAnimation.Stopped]

app = QApplication(sys.argv)

window = QMainWindow()

window.setAttribute(Qt.WA_TranslucentBackground, True)
window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setWindowFlags(Qt.FramelessWindowHint)
desktop = QDesktopWidget()
screenRect = desktop.screenGeometry()
width, height = screenRect.width(), screenRect.height()

label = ClickableLabel(window)
pixmap = QPixmap('image.png')
label.setPixmap(pixmap)
window.setGeometry(width-pixmap.width(),height-pixmap.height(),pixmap.width(),pixmap.height())

label.setGeometry(0, 0, pixmap.width(), pixmap.height())

window.label = label

window.resize(pixmap.width(), pixmap.height())

window.show()
sys.exit(app.exec_())
