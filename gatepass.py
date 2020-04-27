import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import mysql.connector
from mysql.connector import Error
import datetime
from datetime import date
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# Login page
class LoginWind(Screen):
    sname = ObjectProperty(None)
    passcode = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        # open Text FILE
        self.file = open('secfile.txt', 'w')

    # Users Validation
    def check_user(self, sname):
        self.sname = sname
        self.users = dict(admin="12345", security01="54321", EBUKA="12345", AZUKA="1234")
        if self.sname.text in self.users and self.users[self.sname.text] == self.passcode.text:
            # Write Security Name to Text File
            self.file.write(str(sname.text))
            self.file.close()
            sm.current = "entrexit"
            self.reset()

        else:
            wronglog()
            self.reset()

    def reset(self):
        self.sname.text = ""
        self.passcode.text = ""


# MENU(SElECT ENTRANCE/EXIT)
class EntrExit(Screen):
    pass


#ENTRANCE DETAIL PAGE
class EntrWind(Screen):
    #connect to database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mydbkey20",
        database="entrextaqr20"
    )

    trkcursor = db.cursor()
    drivernm = ObjectProperty(None)
    trucknum = ObjectProperty(None)

    # Submit Entry
    def submit_ent(self):
        t = datetime.datetime.now()
        t1 = t.strftime("%H:%M")
        t2 = t.strftime("%a, %b %d")
        if self.drivernm.text != "" and self.trucknum.text != "":
            try:
                # Submit to table 1
                self.trkcursor.execute(
                    "INSERT INTO entrdtl (TIME, DRIVER, TRUCK, SECURITY, DATE, datecheck) VALUES (%s,%s,%s,%s,%s,%s)",
                    (t1, self.drivernm.text, self.trucknum.text, self.call_sec(), t2, t))
                self.db.commit()
                # Submit to table 2
                self.trkcursor.execute(
                    "INSERT INTO entrdtl2 (TIME, DRIVER, TRUCK, SECURITY, DATE, datecheck) VALUES (%s,%s,%s,%s,%s,%s)",
                    (t1, self.drivernm.text, self.trucknum.text, self.call_sec(), t2, t))
                self.db.commit()
                self.pop_entered()
                self.reset()
            except mysql.connector.Error as err:
                print("something went wrong: {}".format(err))
                self.already_entered()
                self.reset()


        else:
            self.pop_empty()

    # return security name
    def call_sec(self):
        self.file = open('secfile.txt', 'r')
        self.secname = self.file.read()
        return self.secname
        self.file.close()

    def reset(self):
        self.drivernm.text = ""
        self.trucknum.text = ""

    def drvnam(self):
        return self.drivernm.text

    def trknum(self):
        return self.trucknum.text

    #popup for incomplete detail
    def pop_empty(self):
        pop = Popup(title='Check',
                    content=Label(text='Enter Driver Name and Truck Number'),
                    size_hint=(None, None), size=(400, 200))
        pop.open()

    #popup for entrance confirmation
    def pop_entered(self):

        box = BoxLayout(orientation='vertical')
        label = Label(text="DRIVER :  " + self.drivernm.text + "\n" + "TRUCK NUMBER:  " + self.trucknum.text,
                      font_size=15, bold=True)
        btn = Button(text="Close", size_hint=(1, 0.2))
        box.add_widget(label)
        box.add_widget(btn)

        pop = Popup(title='ENTRY SUBMITTED',
                    content=box, auto_dismiss=False,
                    size_hint=(None, None), size=(300, 300))
        btn.bind(on_press=pop.dismiss)
        pop.open()

    #Popup for duplicate entry
    def already_entered(self):

        box = BoxLayout(orientation='vertical')
        label = Label(text="You have already entered " + self.drivernm.text + "\n" + "TRUCK NUMBER: " + self.trucknum.text,
                      font_size=15, bold=True)
        btn = Button(text="Close", size_hint=(1, 0.2))
        box.add_widget(label)
        box.add_widget(btn)

        pop = Popup(title='DRIVER ALREADY ENTERED',
                    content=box, auto_dismiss=False,
                    size_hint=(None, None), size=(300, 300))
        btn.bind(on_press=pop.dismiss)
        pop.open()

    def b_login(self):
        sm.current = "loginp"

    def b_entrext(self):
        sm.current = "entrexit"


# EXIT PAGE
class ExitWind(Screen):
    # database connection
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mydbkey20",
        database="entrextaqr20"
    )

    trkcursor = db.cursor()
    drivernm = ObjectProperty(None)
    trucknum = ObjectProperty(None)
    ledger = ObjectProperty(None)
    tcost = ObjectProperty(None)

    #submit exit detail
    def pssbtn(self):
        t3 = date.today()
        t = datetime.datetime.now()
        t1 = t.strftime("%H:%M")
        t2 = t.strftime("%a, %b %d")
        if self.drivernm.text != "" and self.trucknum.text != "" and self.ledger.text != "" and self.tcost.text != "":
            try:
                self.trkcursor.execute(
                    "INSERT INTO exitdtl (TIME, DRIVER, TRUCK, DISTRIBUTOR, COST, SECURITY, DATE, datecheck, day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (t1, self.drivernm.text, self.trucknum.text, self.ledger.text, self.tcost.text, self.call_sec(), t2, t, t3))
                self.db.commit()
                # delete Truck from entry table after exit
                delete_query = """DELETE FROM entrdtl WHERE DRIVER = %s"""
                self.trkcursor.execute(delete_query, (self.drivernm.text,))
                self.db.commit()
                # extracheck delete
                delete_query2 = """DELETE FROM entrdtl WHERE TRUCK = %s"""
                self.trkcursor.execute(delete_query2, (self.trucknum.text,))
                self.db.commit()
                # reset auto incremenet COLUNM NUMBERING on entry table
                self.trkcursor.execute("SET @num := 0")
                self.trkcursor.execute("UPDATE entrdtl SET no = @num := (@num+1)")
                self.trkcursor.execute("ALTER TABLE entrdtl AUTO_INCREMENT = 1")
                self.db.commit()
                self.pop_entered()
                self.reset()
            except mysql.connector.DataError:
                self.long_data()
        else:
            self.pop_empty()

    def call_sec(self):  # return security name 
        self.file = open('secfile.txt', 'r')
        self.secname = self.file.read()
        return self.secname
        self.file.close()

    def reset(self):
        self.drivernm.text = ""
        self.trucknum.text = ""
        self.ledger.text = ""
        self.tcost.text = ""

    def pop_entered(self):
        box = BoxLayout(orientation='vertical')
        label = Label(text="CUSTOMER :  " + self.ledger.text + "\n" + "COST:  " + self.tcost.text + "\n" + "DRIVER: " +
                           self.drivernm.text + "\n" + "TRUCK: " + self.trucknum.text,
                      font_size=15, bold=True)
        btn = Button(text="Close", size_hint=(1, 0.2))
        box.add_widget(label)
        box.add_widget(btn)

        pop = Popup(title='ENTRY SUBMITTED',
                    content=box, auto_dismiss=False,
                    size_hint=(None, None), size=(300, 300))
        btn.bind(on_press=pop.dismiss)
        pop.open()

    def b_login(self):
        sm.current = "loginp"

    def b_entrext(self):
        sm.current = "entrexit"

    def pop_empty(self):
        pop = Popup(title='Check',
                    content=Label(text='Empty not Allowed', bold=True),
                    size_hint=(None, None), size=(250, 200))
        pop.open()

    def use_number(self):
        pop = Popup(title='Use Numbers only',
                    content=Label(text='ENTER ONLY NUMBERS FOR COST \n' 'Do not enter Space between numbers', bold=True),
                    size_hint=(None, None), size=(260, 200))
        pop.open()

    def long_data(self):
        pop = Popup(title='Too Long',
                    content=Label(text='DISTRIBUTORS NAME should be less than 30 characters', bold=True),
                    size_hint=(None, None), size=(260, 200))
        pop.open()

class WindManager(ScreenManager):
    pass


def wronglog():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid Name or Password \n' + 'Try Again', bold=True, halign='center'),
                size_hint=(None, None), size=(200, 200))
    pop.open()


kv = Builder.load_file("mainwind.kv")
sm = WindManager()

sm.add_widget(LoginWind(name="loginp"))
sm.add_widget(EntrExit(name="entrexit"))
sm.add_widget(EntrWind(name="entrancecheck"))
sm.add_widget(ExitWind(name="exitcheck"))

sm.current = "loginp"


class MainwindApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MainwindApp().run()
