from java.awt import Graphics, Color, BasicStroke
from javax.swing import JComponent

class Canvas(JComponent):
    LINE_WIDTH = 4

    def __init__(self, images_dict, puzzle):
        self.images_dict = images_dict
        self.puzzle = puzzle
        self.selected = None
        self.initial_x = 0
        self.initial_y = 0

    def set_selected(self, sel):
        self.selected = sel

    def paintComponent(self, g):
        if self.puzzle == None:
            return

        width = self.images_dict[0].getWidth()
        height = self.images_dict[0].getHeight()

        self.initial_x = self.getWidth()/2 - (width * self.puzzle.level())/2
        self.initial_y = self.getHeight()/2 - (height * self.puzzle.level())/2
        current_y = self.initial_y
        level = self.puzzle.level()
        for i in range(level):
            current_x = self.initial_x
            for j in range (level):
                g.drawImage(self.images_dict[self.puzzle.get_pos(i, j) - 1], current_x, current_y, self)
                current_x = current_x + width
            current_y = current_y + height

        half_line_width = Canvas.LINE_WIDTH / 2
        g.setStroke(BasicStroke(Canvas.LINE_WIDTH))
        g.setColor(Color.BLUE)

        if self.selected != None:
            g.drawRect(self.initial_x + self.selected.x * width + half_line_width ,\
                self.initial_y + self.selected.y * height + half_line_width, width - Canvas.LINE_WIDTH, height - Canvas.LINE_WIDTH)

    def set_puzzle(self, puzzle):
        self.puzzle = puzzle
