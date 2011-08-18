# -*- coding: utf-8 -*-
from java.awt import EventQueue
from java.lang import Runnable
from gui.Gui import Gui

class AwtRun(Runnable):
	def run(self):
		gui = Gui()
		gui.draw()

if __name__ == '__main__':
	EventQueue.invokeLater(AwtRun())
