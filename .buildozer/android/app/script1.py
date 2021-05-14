import pymysql.cursors

mydb = pymysql.connect(
    host="freedb.tech",
    user="freedbtech_reds",
    password="Raskol@786",
    database = "freedbtech_redsdb"
)

mycursor = mydb.cursor()

sql = "INSERT INTO feed (feed_info) VALUES (%s)"
val = ("feed",)
mycursor.execute(sql, val)


