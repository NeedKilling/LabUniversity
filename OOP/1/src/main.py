import flet as ft
from pages.login import loginWindow   

def main(page: ft.Page):
    page.title = "hello"
    page.window.width = 1000

    login:loginWindow = loginWindow()
    page.add(login.page)


if __name__ == "__main__":
    ft.run(main)
