import instaloader
import datetime
import sys
import time
from mysql.connector import connect,Error

if __name__ == "__main__":
    robot_id = sys.argv[1]
    insta_login = sys.argv[2]
    insta_pass = sys.argv[3]

class WorkWithDB:

    def __init__(self,base,host,user,password):
        self.base = base
        self.host = host
        self.user = user
        self.password = password
        
    def connectDB(self):
        try:
            cnx = connect(
                user = self.user, 
                password = self.password,
                host = self.host,
                database = self.base)
            self.cnx = cnx
        except Error as e:
            print(e)

    def queryDB(self, query, typequery):
        query = query
        typequery = typequery
        try:
            with self.cnx.cursor(buffered=True) as cursor:
                cursor.execute(query)
                self.cnx.commit()
                if(typequery == 'select'):
                    result_list = cursor.fetchall()
                    if not result_list:
                        return "None"
                    else:
                        return result_list[0][0]
                elif(typequery == 'select_list'):
                    groups = []
                    result_list = cursor.fetchall()
                    z = 0
                    for row in result_list:
                        groups.append(result_list[z][0])
                        z+=1
                    return groups         
        except Error as e:
            print(e)

class IParser:
    
    def __init__(self,login,password,groups):
        self.login = login
        self.password = password
        self.groups = groups

    def authinsta(self):
        strId = 0
        while True:
            try:
                self.loader = instaloader.Instaloader()
                self.loader.login(self.login, self.password)
            except:
                print("error")
            finally:
                break

    def parser(self):
        for group in self.groups:
            profile = instaloader.Profile.from_username(self.loader.context,group)
            posts = profile.get_posts()
            uniquerow = dbwork.queryDB("SELECT link FROM posts WHERE acc_name = '"+group+"' ORDER BY id DESC LIMIT 1", "select")
            if(str(uniquerow) == 'None'):
                y = 0
                for post in posts:
                    y+=1
                    dbwork.queryDB("INSERT INTO posts (caption, link, image_link, acc_name, date_create, date_add) VALUES ('"+str(post.caption)+"','"+str(post.shortcode)+"','"+str(post.url)+"','"+str(group)+"','"+str(post.date)+"','"+str(datetime.datetime.now())+"')", "insert")
                    post_comments = post.get_comments()
                    for comment in post_comments:
                        dbwork.queryDB("INSERT INTO comments(author,caption,date_create,date_add,post_link) VALUES ('"+str(comment.owner.username)+"','"+str(comment.text)+"','"+str(comment.created_at_utc)+"','"+str(datetime.datetime.now())+"','"+str(post.shortcode)+"')", "insert")
                    if(y==1):
                        break
            else:
                for post in posts:
                    if(str(post.shortcode) == str(uniquerow)):
                        break
                    else:
                        dbwork.queryDB("INSERT INTO posts (caption, link, image_link, acc_name, date_create, date_add) VALUES ('"+str(post.caption)+"','"+str(post.shortcode)+"','"+str(post.url)+"','"+str(group)+"','"+str(post.date)+"','"+str(datetime.datetime.now())+"') ", "insert")
                        post_comments = post.get_comments()
                        for comment in post_comments:
                            dbwork.queryDB("INSERT INTO comments(author,caption,date_create,date_add,post_link) VALUES ('"+str(comment.owner.username)+"','"+str(comment.text)+"','"+str(comment.created_at_utc)+"','"+str(datetime.datetime.now())+"','"+str(post.shortcode)+"')", "insert")

dbwork = WorkWithDB("","","","")
dbwork.connectDB()
#groups_to_check = dbwork.queryDB("SELECT name FROM accounts WHERE robot_id = "+robot_id+"", "select_list")
groups_to_check = dbwork.queryDB("SELECT name FROM accounts", "select_list")
iparser = IParser(insta_login, insta_pass, groups_to_check)
iparser.authinsta()

for i in range(0,100,+1):
    iparser.parser()
    print("Парсинг под номером " + str(i) + " закончен. Спящий режим на 1 минут")
    time.sleep(60)
