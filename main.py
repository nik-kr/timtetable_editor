import os
import json
import platform
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import font

version = 'v1.0'

class Timetable(Frame):
    
    def __init__(self, parent=None, group_name = '', load=False, load_data = {}):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.group_name = group_name

        self.data_template = {
            'group' : 'Учебная Группа',
            'Mondey' :      {'content': dict},
            'Tuesday':      {'content': dict},
            'Wednesday':    {'content': dict},
            'Thursday':     {'content': dict},
            'Friday':       {'content': dict},
            'Saturday':     {'content': dict},
            'Sunday':       {'content': dict}
        }

        self.tab_list = []
        self.day_list   = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        self.day_listEN = ['Mondey', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        label = Label(self, text='РАСПИСАНИЕ', font=('Arial', 20))
        label.pack()

        self.tabs = ttk.Notebook(self, width=1500)
        self.tabs.pack(expand=True, fill=BOTH)
        
        for i in range(7):
            self.tab_list.append(TimetableTable(self.tabs, day=i+1))
            self.tab_list[i].pack(fill=BOTH, expand=True)
            self.tabs.add(self.tab_list[i], text=self.day_list[i])

    def load_timetable(self, data: dict):
        for i in range(7):
            self.tab_list[i].load_data(data[self.day_listEN[i]])
        pass
    
    def save_timetable(self):
        file_name = fd.asksaveasfilename(
            initialdir = "./",
            title = "Выберите файл",
            filetypes=[("TIMETABLE JSON file", "*.timetablejson")])
        data = self.get_timetable_data()
        with open(file_name, 'w') as write_file:
            json.dump(data, write_file)
        
        pass

    def get_timetable_data(self):
        self.data_template['group'] = self.group_name
        for i in range(7):
            self.data_template[self.day_listEN[i]] = self.tab_list[i].upload_data()
        return self.data_template
        
    
class TimetableTable(ttk.Frame):

    def __init__(self ,parent=None, day = 1, day_count = 2):

        self.day_list   = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        self.day_listEN = ['Mondey', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        tkinter.Frame.__init__(self, parent)

        self.START_COUNT = 2
        self.MAX_COUNT   = 12
        self.COUNT = day_count
        
        countLessonFrame    = Frame(self)
        countLessonLabel    = Label(countLessonFrame, text='Кол-во занятий:')
        countLessonLabel.pack(side=LEFT)
        self.countLessonVar = IntVar()
        self.countLessonVar.set(self.START_COUNT)
        self.countLessonScale    = Scale(countLessonFrame, from_=self.START_COUNT, to=self.MAX_COUNT, command=self.update_scale, orient=HORIZONTAL)
        self.countLessonScale.pack(side=LEFT)
        self.countLessonOutpootLabel    = Label(countLessonFrame, textvariable=self.countLessonVar)
        self.countLessonOutpootLabel.pack(side=LEFT, padx=5)
        countLessonFrame.pack(side=TOP)

        timetable_frame = Frame(self)
        
        font=('Arial', 12)

        start_time      = Label(timetable_frame, text='Время начала', font=font)
        start_time.grid(column=0, row=0)
        lesson_name     = Label(timetable_frame, text='Предмет', font=font)
        lesson_name.grid(column=1, row=0)
        classroom       = Label(timetable_frame, text='Кабинет', font=font)
        classroom.grid(column=2, row=0)
        teacher         = Label(timetable_frame, text='Преподаватель', font=font)
        teacher.grid(column=3, row=0)

        self.start_time_list = []

        for i in range(4):
            self.start_time_list.append([])
            for j in range(self.MAX_COUNT):
                self.start_time_list[i].append([])
                self.start_time_list[i][j].append(StringVar())
                self.start_time_list[i][j].append(Entry(timetable_frame, textvariable=self.start_time_list[i][j][0]))
                self.start_time_list[i][j][1].grid(column=i, row=j+1)
        
        step = self.MAX_COUNT-1

        while step != self.COUNT-1:
            for i in range(4):
                self.start_time_list[i][step][1].grid_forget()
            step -= 1
        

        timetable_frame.pack(padx=20)
    
    def load_data(self, data):
        self.COUNT = len(data)
        self.update_scale(self.COUNT)
        self.countLessonVar.set(self.COUNT)
        self.countLessonScale.set(self.COUNT)

        for i in range(self.COUNT):
            for j in range(4):
                self.start_time_list[j][i][0].set(data[i][j])
    
    def upload_data(self):
        content = []
        
        for i in range(self.COUNT):
            content.append([])
            for j in range(4):
                content[i].append(self.start_time_list[j][i][0].get())
        
        return content

    def update_scale(self, value):
        self.countLessonVar.set(value)
        self.countLessonOutpootLabel['text'] = value

        value = (int(value))

        if value >= self.COUNT:
            for i in range(value):
                for j in range(4):
                    self.start_time_list[j][i][1].grid(column=j, row=i+1)
        elif value <= self.COUNT:
            for i in range(value-1):
                for j in range(4):
                    try:
                        self.start_time_list[j][i+value][1].grid_forget()
                    except:
                        pass
        self.COUNT = value

def init_ui():
    mktimetable_win = Tk()
    mktimetable_win.title('Создать Расписание')
    mktimetable_win.geometry('250x130')
    mktimetable_win.resizable(False, False)
    lableProgrammName = Label(mktimetable_win, text='Расписание ' + version, font=('Arial', 20))
    lableProgrammName.pack()
    buttonOpenTimetable = Button(mktimetable_win, text='Редактровать расписание', command=lambda: edit_timetable(mktimetable_win), width=26)
    buttonOpenTimetable.pack(side=BOTTOM)
    buttonNewTimetable = Button(mktimetable_win, text='Создать новое расписание', command=lambda : (win_group_name(mktimetable_win)), width=26)
    buttonNewTimetable.pack(side=BOTTOM)

    mktimetable_win.mainloop()

def edit_timetable_win(group_name = 'Тестовая группа', load = False, load_data = {}):
    edittimetable_win = Tk()
    edittimetable_win.title('Открыто расписание: ' + group_name)
    edittimetable_win.geometry('600x600')
    

    if platform.system() == 'Linux':
        edittimetable_win.attributes('-zoomed', True)
    elif platform.system() == 'Windows':
        edittimetable_win.attributes('-fullscreen', True)
    
    timetable = Timetable(edittimetable_win, group_name=group_name)

    mainmenu = Menu(edittimetable_win)

    edittimetable_win.config(menu=mainmenu)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label='Сохранить', command=timetable.save_timetable)
    filemenu.add_command(label='Выход', command=lambda: (edittimetable_win.destroy(), exit()))

    mainmenu.add_cascade(label='Файл', menu=filemenu)

    timetable.pack()
    

    if load == True and load_data.get('group'):
        timetable.group_name = load_data['group']
        edittimetable_win.title(load_data['group'])
        timetable.load_timetable(load_data)
        pass
    elif load==False:
        pass
    else:
        error_msg = mb.showerror(
            'Ошибка!', 'Файл повреждён', 
        )
        edittimetable_win.destroy()
        exit()

    edittimetable_win.mainloop()

def win_group_name(window: Tk):
    window.destroy()
    root = Tk()
    root.title('Введите имя группы')
    root.geometry('200x100')
    root.resizable(False, False)
    
    lbl = Label(root, text='Введите имя группы', font=('Arial', 12))
    lbl.pack()
    groupNameVar    = StringVar(root)
    groupNameEntry  = Entry(root, textvariable=groupNameVar)
    groupNameEntry.pack()
    btnNext = Button(root, text='<Далее>', command=lambda: (new_timetable(root, groupNameVar.get())))
    btnNext.pack()

def new_timetable(window : Tk, group_name):
    window.destroy()
    edit_timetable_win(group_name=group_name, load=False)
    print('Создание нового расписания')

def edit_timetable(window: Tk):
    data : dict
    file_name = fd.askopenfilename(
            initialdir = "./",
            title = "Выберите файл",
            filetypes=[("TIMETABLE JSON file", "*.timetablejson")])
    with open(file_name, 'r') as read_file:
        data = json.load(read_file)
    window.destroy()
    edit_timetable_win(load=True, load_data=data)
    

if __name__ == "__main__":
    init_ui()
    pass