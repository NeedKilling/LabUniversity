import flet as ft

class loginWindow(ft.Container):
    def __init__ (self):
        super().__init__()
        self.content: ft.Text = ft.Text("button")
        self.border = ft.Border.all(1, ft.Colors.BLACK_54)
        self.border_radius = 3
        self.bgcolor = "0x09000000"
        self.padding = 10
        self.visible = False