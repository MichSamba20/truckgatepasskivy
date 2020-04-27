from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from sqlalchemy import create_engine
import pandas as pd
from kivy.core.window import Window


#connect to Mysql database via SQLALCHEMY
engine = create_engine('mysql+pymysql://root:mydbkey20@localhost/entrextaqr20')
#dbconnect = engine.connect()


#MENU PAGE
class SeleView(Screen):
    pass

class SeleExview(Screen):
    pass

#ENTRANCE VIEW PAGE
class EntView(Screen):


    def __init__(self, **kwargs):
        super(EntView, self).__init__(**kwargs)
        self.print_data_frame1()
        scroll = self.ids['scroll_view']
        scroll.size = Window.width, Window.height

    #Table of Truck Entrance
    def print_data_frame1(self):
        self.df = pd.read_sql('SELECT no,DATE, DRIVER, TRUCK, SECURITY, TIME FROM entrdtl ORDER BY datecheck DESC',engine)
        self.ids.cl6.text = str(self.df.no.to_string(index=False))
        self.ids.cl1.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl2.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl3.text = str(self.df.TRUCK.to_string(index=False))
        self.ids.cl4.text = str(self.df.SECURITY.to_string(index=False))
        self.ids.cl5.text = str(self.df.TIME.to_string(index=False))

    def set_layout(self):
        pass



#View Exit Page
class ExtView(Screen):

    def __init__(self, **kwargs):
        super(ExtView, self).__init__(**kwargs)
        self.print_dataframe2()
        scroll = self.ids['scroll_view']
        scroll.size = Window.width, Window.height

    #Exit view Table for current day
    def print_dataframe2(self):
        self.df = pd.read_sql('SELECT ROW_NUMBER() OVER(ORDER BY datecheck DESC) AS num,TIME,DISTRIBUTOR,COST,DRIVER,SECURITY,DATE FROM exitdtl WHERE datecheck > date_sub(now(), interval 1 day)', engine)
        self.ids.cl1.text = str(self.df.num.to_string(index=False))
        self.ids.cl2.text = str(self.df.TIME.to_string(index=False))
        self.ids.cl7.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl3.text = str(self.df.DISTRIBUTOR.to_string(index=False))
        self.ids.cl4.text = str(self.df.COST.to_string(index=False))
        self.ids.cl5.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl6.text = str(self.df.SECURITY.to_string(index=False))

        self.df1 = pd.read_sql('SELECT SUM(COST) FROM exitdtl WHERE datecheck > date_sub(now(), interval 1 day)', engine)
        self.ids.tsum.text = str(self.df1.to_string(index=False))

    # Exit view Table for past 48 hours
    def print_dataframe2day(self):
        self.df = pd.read_sql('SELECT ROW_NUMBER() OVER(ORDER BY datecheck DESC) AS num,TIME,DISTRIBUTOR,COST,DRIVER,SECURITY,DATE FROM exitdtl WHERE datecheck > date_sub(now(), interval 2 day)', engine)
        self.ids.cl1.text = str(self.df.num.to_string(index=False))
        self.ids.cl2.text = str(self.df.TIME.to_string(index=False))
        self.ids.cl7.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl3.text = str(self.df.DISTRIBUTOR.to_string(index=False))
        self.ids.cl4.text = str(self.df.COST.to_string(index=False))
        self.ids.cl5.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl6.text = str(self.df.SECURITY.to_string(index=False))

        self.df1 = pd.read_sql('SELECT SUM(COST) FROM exitdtl WHERE datecheck > date_sub(now(), interval 2 day)', engine)
        self.ids.tsum.text = str(self.df1.to_string(index=False))

    #Exit view Table for past 3 days
    def print_dataframe3day(self):
        self.df = pd.read_sql('SELECT ROW_NUMBER() OVER(ORDER BY datecheck DESC) AS num,TIME,DISTRIBUTOR,COST,DRIVER,SECURITY,DATE FROM exitdtl WHERE datecheck > date_sub(now(), interval 3 day)', engine)
        self.ids.cl1.text = str(self.df.num.to_string(index=False))
        self.ids.cl2.text = str(self.df.TIME.to_string(index=False))
        self.ids.cl7.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl3.text = str(self.df.DISTRIBUTOR.to_string(index=False))
        self.ids.cl4.text = str(self.df.COST.to_string(index=False))
        self.ids.cl5.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl6.text = str(self.df.SECURITY.to_string(index=False))

        self.df1 = pd.read_sql('SELECT SUM(COST) FROM exitdtl WHERE datecheck > date_sub(now(), interval 3 day)', engine)
        self.ids.tsum.text = str(self.df1.to_string(index=False))

    #Exit view Table for past 1 week
    def print_dataframe7day(self):
        self.df = pd.read_sql('SELECT ROW_NUMBER() OVER(ORDER BY datecheck DESC) AS num,TIME,DISTRIBUTOR,COST,DRIVER,SECURITY,DATE FROM exitdtl WHERE datecheck > date_sub(now(), interval 7 day)', engine)
        self.ids.cl1.text = str(self.df.num.to_string(index=False))
        self.ids.cl2.text = str(self.df.TIME.to_string(index=False))
        self.ids.cl7.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl3.text = str(self.df.DISTRIBUTOR.to_string(index=False))
        self.ids.cl4.text = str(self.df.COST.to_string(index=False))
        self.ids.cl5.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl6.text = str(self.df.SECURITY.to_string(index=False))

        self.df1 = pd.read_sql('SELECT SUM(COST) FROM exitdtl WHERE datecheck > date_sub(now(), interval 7 day)', engine)
        self.ids.tsum.text = str(self.df1.to_string(index=False))


#Exit view page via date range
class Range_View(Screen):
    start_date = ObjectProperty(None)
    end_date = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(Range_View, self).__init__(**kwargs)

    #Exit view Table via date range
    def check_range(self):
        r_query=  """SELECT ROW_NUMBER() OVER(ORDER BY datecheck DESC) AS num,TIME,DISTRIBUTOR,COST,DRIVER,SECURITY,DATE FROM exitdtl WHERE day between %s and %s"""
        self.df = pd.read_sql(r_query, engine, params=(self.start_date.text, self.end_date.text,))
        self.ids.cl1.text = str(self.df.num.to_string(index=False))
        self.ids.cl2.text = str(self.df.TIME.to_string(index=False))
        self.ids.cl7.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl3.text = str(self.df.DISTRIBUTOR.to_string(index=False))
        self.ids.cl4.text = str(self.df.COST.to_string(index=False))
        self.ids.cl5.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl6.text = str(self.df.SECURITY.to_string(index=False))
        scroll = self.ids['scroll_view']
        scroll.size = Window.width, Window.height

#Exit view page via driver name/ Truck number
class Check_Truck(Screen):
    drivernam = ObjectProperty(None)
    trucknum = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Check_Truck, self).__init__(**kwargs)


    def not_found(self):
        pass

    def show_truck_dtl(self):
        select_query = """SELECT ROW_NUMBER() OVER(ORDER BY datecheck) AS num,TIME,DISTRIBUTOR,COST,DRIVER,SECURITY,DATE FROM exitdtl WHERE DRIVER = %s OR TRUCK = %s"""
        self.df = pd.read_sql(select_query, engine, params=(self.drivernam.text, self.trucknum.text,))
        self.ids.cl1.text = str(self.df.num.to_string(index=False))
        self.ids.cl2.text = str(self.df.DATE.to_string(index=False))
        self.ids.cl3.text = str(self.df.DISTRIBUTOR.to_string(index=False))
        self.ids.cl4.text = str(self.df.COST.to_string(index=False))
        self.ids.cl5.text = str(self.df.DRIVER.to_string(index=False))
        self.ids.cl6.text = str(self.df.TIME.to_string(index=False))
        self.ids.cl7.text = str(self.df.SECURITY.to_string(index=False))
        scroll = self.ids['scroll_view']
        scroll.size = Window.width, Window.height




class MainScrn(ScreenManager):
    pass

kv = Builder.load_file("viewgatepass.kv")
sm = MainScrn()

sm.add_widget(EntView(name="entview"))
sm.add_widget(SeleExview(name="extviewselect"))
sm.add_widget(ExtView(name="extview"))
sm.add_widget(Range_View(name="timerange"))
sm.add_widget(Check_Truck(name="checktruck"))
sm.add_widget(SeleView(name="selectview"))

sm.current = 'selectview'

class TestApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()
