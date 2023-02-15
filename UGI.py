from tkinter import *


def click():
    print('Привет')


root = Tk()
root.title('Вычисление внутренних напряжений')
root.geometry('600x600')  # размеры окна
root.resizable(width=False, height=False)  # нельзя изменить размер окна
root.iconbitmap('')  # изменение иконки, указать путь

root.config(bg='blue')  # изменение фона
root['bg'] = 'black'  # изменение фона

btn = Button(root,  # создание кнопки
             text='Кнопка',  # текст кнопки
             command=click,  # действие кнопки
             font=("Comic Sans MS", 20, 'italic', 'bold'),  # шрифт и масштаб текста
             width=6,  # ширина кнопки
             height=2,  # высота кнопки
             bg='Lime',  # фон кнопки
             activebackground='red',  # фон кнопки при нажатии
             activeforeground='white',  # фон шрифта при нажатии
             fg='brown'  # цвет шрифта
             )
btn.place(x=20, y=20)  # отображение кнопки

canvas = Canvas()

root.mainloop()
