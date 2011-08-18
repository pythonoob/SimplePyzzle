# -*- coding: UTF-8 -*-

from gui.Canvas import Canvas
from java.awt import BorderLayout, Point, ScrollPane, Dimension
from java.awt.event import MouseAdapter
from java.awt.image import BufferedImage
from java.io import File, IOException
from javax.imageio import ImageIO, IIOException
from javax.swing import JFrame, JLabel, JTextArea, JPanel, JTextField, \
    JOptionPane, JButton, JScrollPane, JFileChooser, UIManager, JComboBox
from puzzle.SimplePyzzle import SimplePyzzle
from img.Resizer import resize_image
from img.Splitter import split_image
import math

class Gui(MouseAdapter):
    IMG_MIN_SIZE = 200
    IMG_MAX_SIZE = 500

    def __init__(self):
        self.pos1 = None
        self.puzzle = None

    def mouseEntered(self, event):
        self.in_canvas = True

    def mouseExited(self, event):
        self.in_canvas = False

    def mouseReleased(self, event):
        if not self.in_canvas or self.puzzle == None:
            return

        width = self.images_dict[0].getWidth()
        height = self.images_dict[0].getHeight()

        def valid_pos(pos):
            return pos >= 0 and pos < self.puzzle.level()

        x = (event.getX() - self.canvas.initial_x) / width
        y = (event.getY() - self.canvas.initial_y) / height

        if not valid_pos(x) or not valid_pos(y):
            return

        pos = Point(x, y)
        if self.pos1 != None: #then is second click
            if self.pos1.equals(pos):
                self.pos1 = None
            else:
                self.play_event(self.pos1.y, self.pos1.x, pos.y, pos.x)
                self.pos1 = None
        else:
            self.pos1 = pos
        self.canvas.set_selected(self.pos1)
        self.canvas.repaint()

    def draw(self):

        try:
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        except:
            pass

        self.images_dict = dict()
        self.canvas = Canvas(self.images_dict, None)
        self.canvas.addMouseListener(self)

        self.frame = JFrame("SimplePyzzle", visible = 1)
        self.frame.setMinimumSize(Dimension(300, 300))
        self.frame.setLocationRelativeTo(None)
        self.generate_button = JButton("Generate Puzzle")
        self.bottom_panel = JPanel()

        self.combo_box_list = [9, 16, 25, 36, 49]
        self.combo_box = JComboBox(self.combo_box_list)

        self.frame.contentPane.add(self.canvas, BorderLayout.CENTER)
        self.frame.contentPane.add(self.bottom_panel, BorderLayout.SOUTH)
        self.bottom_panel.add(self.generate_button, BorderLayout.EAST)
        self.bottom_panel.add(self.combo_box, BorderLayout.WEST)

        self.generate_button.actionPerformed = self.generate_board

        self.frame.setSize(500, 500)
        self.frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE;
        self.frame.pack()

    def generate_board(self, event):

        chooser = JFileChooser()
        status = chooser.showOpenDialog(self.frame)
        if status != JFileChooser.APPROVE_OPTION:
            return

        imageFile = chooser.getSelectedFile()

        self.puzzle = SimplePyzzle(float(int(self.combo_box.getSelectedItem())))
        self.draw_board()
        self.load_images(imageFile, self.puzzle.level())
        self.canvas.set_puzzle(self.puzzle)
        width = self.images_dict[0].getWidth()
        height = self.images_dict[0].getHeight()
        size = Dimension(width * self.puzzle.level(), height * self.puzzle.level())
        self.frame.setPreferredSize(size)
        self.frame.setSize(size)

    def show_error(self, error):
        JOptionPane.showMessageDialog(self.frame, \
                                    error, \
                                    "Error!", \
                                    JOptionPane.ERROR_MESSAGE)

    def load_images(self, file, length):

        try:
            image = ImageIO.read(file);
        except IIOException:
            self.show_error(u"You have to pick an image!")
            return

        image_biggest_side = image.getWidth() if image.getWidth() > image.getHeight\
            else image.getHeight()
        imageSize = image_biggest_side
        if image_biggest_side > Gui.IMG_MAX_SIZE:
            imageSize = Gui.IMG_MAX_SIZE

        if image_biggest_side < Gui.IMG_MIN_SIZE:
            imageSize = Gui.IMG_MIN_SIZE

        resized_image = resize_image(image, imageSize, imageSize)

        images = split_image(resized_image, length)
        self.images_dict.clear()
        for i in range(len(images)):
            self.images_dict[i] = images[i]

    def play_event(self, x1, y1, x2, y2):
          status = self.puzzle.play(x1, y1, x2, y2)
          self.draw_board()
          if status == SimplePyzzle.END_GAME:
              JOptionPane.showMessageDialog (None, \
                                  "Grats! You solved the puzzle", \
                                  "Puzzle solved!", \
                                   JOptionPane.INFORMATION_MESSAGE);

    def draw_board(self):
        self.canvas.repaint()
