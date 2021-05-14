from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
import pymysql.cursors

db_string = "postgresql://prczzswgxxrnvc:17476a67504bca1a6b3cbd653480d6bd814bce82df26bce7b1a1671826a652c2@ec2-54-197-100-79.compute-1.amazonaws.com:5432/d4bsdrtg9i2j5d"
Builder.load_file('design.kv')


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screeen_success'
        else:
            anim = Animation(color=(0.6, 0.7, 0.1, 1))
            anim.start(self.ids.login_wrong)
            self.ids.login_wrong.text = "Wrong username or password!"


class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword,
                        'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"


class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in
                              available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding='utf8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

    def feed_back(self):
        self.manager.current = "feedback_screen"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class FeedbackScreen(Screen):
    def send_feed(self, feed):
        print(feed)
        # connection = psycopg2.connect(user="prczzswgxxrnvc",
        #                               password="17476a67504bca1a6b3cbd653480d6bd814bce82df26bce7b1a1671826a652c2",
        #                               host="ec2-54-197-100-79.compute-1.amazonaws.com",
        #                               port="5432",
        #                               database="d4bsdrtg9i2j5d")
        # db = create_engine(db_string)
        #
        # postgres_insert_query = """INSERT INTO feed(feed_info) VALUES (%s)"""
        #
        # db.execute(postgres_insert_query, feed)
        # print("Record inserted successfully into feed table")
        try:

            mydb = pymysql.connect(
                host="freedb.tech",
                user="freedbtech_reds",
                password="Raskol@786",
                database="freedbtech_redsdb"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO feed (feed_info) VALUES (%s)"
            val = (feed,)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "Record inserted successfully into feed table")

            self.manager.current = 'login_screen'
        except pymysql.Error as err:
            print("Something went wrong: {}".format(err))


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
