from Window import Window

root = Window()

while not root.closing:
    root.draw_screen()
    root.update_idletasks()
    root.update()
