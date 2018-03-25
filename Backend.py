<<<<<<< HEAD
from gmplot import gmplot
import gmaps
import googlemaps

from flask import Flask, request, render_template

class ListGardens:
    def __init__(self):
        self.dict_garden = {}

    def create_gard(self, name, owner):
        if name in self.dict_garden:
            print("Garden already exists")
        else:
            new_gard = Garden(name,owner)
            self.dict_garden[name] = (new_gard,owner)  # This tuple holds the object, so if we want to call name, make sure to specify.
            owner.add_garden(new_gard)

    def find_garden(self, name_gard):
        if name_gard in self.dict_garden:
            return self.dict_garden[name_gard][0].name
        else:
            print("Garden does not exist")
    def display(self):
        garden_string =""
        for key in self.dict_garden:
            garden_string += self.dict_garden[key][0].name
            garden_string += " "
        print (garden_string)


global_list = ListGardens()

global_users = {}

class Ratings:
    def __init__(self):
        self.num_ratings = 0
        self.total_rating = 0
        self.raters= {}

    def rating_calculator(self, new_rating):
        self.total_rating = ((self.total_rating * self.num_ratings) + new_rating) / (self.num_ratings + 1)
        self.num_ratings += 1

class User:
    def __init__(self, name=""):
        global global_users
        if(name in global_users):
            print("Username already taken")
            return
        self.name = name
        self.password = ""
        self.actual_name = ""
        self.gardensowned = {}
        self.gardensmember = {}
        # self.stock = []
        # self.need = []
        self.comment = ""
        # self.rating =
        self.rating = Ratings()
        global_users[name] = self

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def edit_real_name(self,new_name):
        self.actual_name = new_name

    def get_owned(self):
        return list(self.gardensowned.keys())

    def update_address(self,garden,address):
        garden.add_location(address)

    def member_of(self):
        return list(self.gardensmember.keys())

    def create_garden(self, gard_name):
        var = self
        global global_list
        global_list.create_gard(gard_name,var)

        # def remove_garden(self,garden): # Get rid of garden that is owned
        #    if (garden in self.gardensowned):
        #       self.gardensowned.remove(garden)
        #   else:
        #      print("You do not own that garden")

    def add_garden(self, garden):  # Use this for garden creation,
        self.gardensowned[garden.name] = garden
        # if (garden not in self.gardensowned):
        #  self.gardensowned.append(garden)
        # else:
        #   print("Garden already owned")


    def join_garden(self, garden):  # Join a garden you're not the owner of
        if garden not in self.gardensmember:
            self.gardensmember[garden.name]= garden
            self.gardensmember[garden.name].add_member(self)
        else:
            print("Already member of garden")

            # def leave_garden(self,gardenname): #Leave a garden

            #   if(garden in self.gardensmember):
            #      self.gardensmember.remove(garden)
            # else:
            #  	print("You are not a member of this garden")

    def leave_garden(self,garden_name):
        del(self.gardensmember[garden_name])
        print("Successfully left ",garden_name)


    def addcomment(self, comment):  # this is intended for extremely long comments, like one long string
        self.comment = comment

    def everything(self): #gets everything from this
        name = self.name
        garden_owned  = list(self.gardensowned.keys()) # List of all keys, aka gardens this guy owns
        member_of = list(self.gardensmember.keys()) #List of all gardens member of
        rating = str(self.rating.total_rating)
        rating_count = str(self.rating.num_ratings)
        return [name,garden_owned,member_of,rating,rating_count]
    def display(self):
        display_string = ""
        for key in self.gardensowned:
            display_string += self.gardensowned[key].name
        print (self.name, " Is a member of", display_string)

    def rate(self,to_rate,r8ting):

        to_rate.rating.rating_calculator(r8ting)

    def post(self,garden_to_post):
        self.gardensowned[garden_to_post].post_new(input("Insert your post"), input("Image file name?"))



class Coordinate:
    def __init__(self,):
        self.lat = ""
        self.long = ""

    def set_coordinates(self,lat,long):
        self.lat = lat
        self.long = long
class Garden:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.produce = {}
        self.members = []
        self.rating = Ratings()
        self.posts = []
        self.coordinate = Coordinate()
        self.address = ""

    def everything(self):
        return[self.name,self.owner.name,self.produce,self.members,self.address,self.rating.total_rating,self.rating.num_ratings]

    def add_location(self,address = ''):
        self.address = address
        gmaps = googlemaps.Client(key="AIzaSyBpXBfHdEabuTSvmFki2eIfS5A1-zomBCo")
        results = gmaps.geocode(self.address)
        for result in results:
            geo = result['geometry']
            lat, lng = geo['location']['lat'], geo['location']['lng']
            self.coordinate.set_coordinates(lat,lng)

    def get_loc(self):
        return (self.coordinate.lat,self.coordinate.long)
    def add_member(self,new_member):
        self.members.append(new_member)

    def remove_member(self,old_member):
        self.members.remove(old_member)

    def add_stock(self, produce_to_add):
        if produce_to_add not in self.produce:
            self.produce[produce_to_add] = [produce_to_add.name, 0]
        else:
            self.produce[produce_to_add][1] += 1

    def post_new (self,content,image):
        self.posts.append(content,image) # need to add date time functionality


class Produce:
    def __init__(self, name):
        self.name = name

def create_user(user_name):
    user = User(user_name)
    return user

def user_name(user):
    return user.getname()

def get_owner_list(user):
    return list(user.gardensowned.keys())

def get_member_list(user):
    return list(user.gardensmember.keys())

def create_new_garden(owner,garden_name):
    owner.create(garden_name)

def print_rating(subject):
    print(subject.rating.total_rating)

def join_garden(user,garden):
    user.join_garden(garden)

def leave_garden(user,garden_name):
    user.leave_garden(garden_name)

def rate(user,subject,r8ting):
    if (subject.name in global_list.dict_garden or subject.name in global_users):
        if (user.name in subject.rating.raters): # Update rating to new rating, if user already rated once
            subject.rating.total_rating = ((subject.rating.total_rating * subject.rating.num_ratings) - subject.rating.raters[user.name] +r8ting ) /subject.rating.num_ratings
            subject.rating.raters[user.name] = r8ting
        else:
            subject.rating.raters[user.name] = r8ting
            user.rate(subject,r8ting)
    else:
        print("Subject does not exist")

def get_user_data(username):
    return global_users[username]

def get_garden_data(gardenname):
    return global_list.dict_garden[gardenname][0]

def update_garden_loc(user,gardenname,address):
    garden = get_garden_data(gardenname)
    user.update_address(garden,address)

def draw_map(address):
    gmaps = googlemaps.Client(key="AIzaSyBpXBfHdEabuTSvmFki2eIfS5A1-zomBCo")
    results = gmaps.geocode(address)
    for result in results:
        geo = result['geometry']
        lat, lng = float(geo['location']['lat']), float(geo['location']['lng'])

    gmap = gmplot.GoogleMapPlotter(lat,lng, 16)

    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    gmap.marker(lat,lng,"red")
    for garde in global_list.dict_garden:
        if(global_list.dict_garden[garde][0].address != ""):
            current_loc = global_list.dict_garden[garde][0].get_loc()
            gmap.marker(current_loc[0], current_loc[1], "#008000")
    gmap.draw("map3.html")

def add_produce(garden,fruit,count,price):
    if (fruit in garden.produce):
        garden.produce[fruit][0] += count
        garden.produce[fruit][1] = price
    else:
        garden.produce[fruit] = (count,price)

Bob = User("Bob")
Bob.create_garden("Avenue U")
Bob.display()
Bob.create_garden ("Prospect Park")
Bob.display()
Bob2 = User("Bob")
Joe = User("Joe")
Joe.create_garden("Prospect Park")
Joe.create_garden("Joe's Garden")
Joe.display()
Bob.join_garden(Joe.gardensowned["Joe's Garden"])
Bob.leave_garden("Joe's Garden")
garde_boy = get_garden_data("Joe's Garden")

garde_boy.add_location("6 Metrotech  Brooklyn")

garde_boy = get_garden_data("Prospect Park")

garde_boy.add_location("Cadman Plaza Brooklyn ")

Joe.create_garden("Ave_B")

garde_boy = get_garden_data("Ave_B")

add_produce(garde_boy,"Lettuce",5,.45)
add_produce(garde_boy, "Potato", 10, 2.50)
add_produce(garde_boy,"Watermelon" , 7, 4.99)

garde_boy.add_location("Fort Greene Brooklyn New York")

Joe.create_garden("Ave C")

garde_boy = get_garden_data("Ave C")

garde_boy.add_location("Building 92 Brooklyn New York")



Joe.create_garden("Ave D")
Joe.join_garden(get_garden_data("Prospect Park"))
garde_boy = get_garden_data("Ave D")

garde_boy.add_location("Brooklyn Heights Promenade Brooklyn New York")

draw_map("2 Metrotech Brooklyn")
print(Joe.rating.total_rating,Joe.rating.num_ratings)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def loginPage():
    return render_template('LoginPage.html')

@app.route('/member/<user>')
def memberprof(user):
    member = get_user_data(user)
    user_info = member.everything()
    return render_template('Member_Activities.html',name = user_info[0],owned = user_info[1][0], member = user_info[2][0],rating = "7",rating_count = "4")

@app.route('/garden/<garden>')
def gardenprof(garden):
    gard = get_garden_data((garden))
    gard_info = gard.everything()
    print(gard_info[2])
    print(gard_info[2])
    return render_template("Garden_Info.html", name = gard_info[0],owned = gard_info[1],produce1 ='Lettuce',produce2 =  'Potato',produce3 = 'Watermelon',members = str(len(gard_info[3])),address=gard_info[4],rating=str(gard_info[5]),rating_count=str(gard_info[6]))

if __name__=="__main__":
    app.run()
    
print("RAN")
=======
from gmplot import gmplot
import gmaps
import googlemaps

from flask import Flask, request, render_template

class ListGardens:
    def __init__(self):
        self.dict_garden = {}

    def create_gard(self, name, owner):
        if name in self.dict_garden:
            print("Garden already exists")
        else:
            new_gard = Garden(name,owner)
            self.dict_garden[name] = (new_gard,owner)  # This tuple holds the object, so if we want to call name, make sure to specify.
            owner.add_garden(new_gard)

    def find_garden(self, name_gard):
        if name_gard in self.dict_garden:
            return self.dict_garden[name_gard][0].name
        else:
            print("Garden does not exist")
    def display(self):
        garden_string =""
        for key in self.dict_garden:
            garden_string += self.dict_garden[key][0].name
            garden_string += " "
        print (garden_string)


global_list = ListGardens()

global_users = {}

class Ratings:
    def __init__(self):
        self.num_ratings = 0
        self.total_rating = 0
        self.raters= {}

    def rating_calculator(self, new_rating):
        self.total_rating = ((self.total_rating * self.num_ratings) + new_rating) / (self.num_ratings + 1)
        self.num_ratings += 1

class User:
    def __init__(self, name=""):
        global global_users
        if(name in global_users):
            print("Username already taken")
            return
        self.name = name
        self.password = ""
        self.actual_name = ""
        self.gardensowned = {}
        self.gardensmember = {}
        # self.stock = []
        # self.need = []
        self.comment = ""
        # self.rating =
        self.rating = Ratings()
        global_users[name] = self

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def edit_real_name(self,new_name):
        self.actual_name = new_name

    def get_owned(self):
        return list(self.gardensowned.keys())

    def update_address(self,garden,address):
        garden.add_location(address)

    def member_of(self):
        return list(self.gardensmember.keys())

    def create_garden(self, gard_name):
        var = self
        global global_list
        global_list.create_gard(gard_name,var)

        # def remove_garden(self,garden): # Get rid of garden that is owned
        #    if (garden in self.gardensowned):
        #       self.gardensowned.remove(garden)
        #   else:
        #      print("You do not own that garden")

    def add_garden(self, garden):  # Use this for garden creation,
        self.gardensowned[garden.name] = garden
        # if (garden not in self.gardensowned):
        #  self.gardensowned.append(garden)
        # else:
        #   print("Garden already owned")


    def join_garden(self, garden):  # Join a garden you're not the owner of
        if garden not in self.gardensmember:
            self.gardensmember[garden.name]= garden
            self.gardensmember[garden.name].add_member(self)
        else:
            print("Already member of garden")

            # def leave_garden(self,gardenname): #Leave a garden

            #   if(garden in self.gardensmember):
            #      self.gardensmember.remove(garden)
            # else:
            #  	print("You are not a member of this garden")

    def leave_garden(self,garden_name):
        del(self.gardensmember[garden_name])
        print("Successfully left ",garden_name)


    def addcomment(self, comment):  # this is intended for extremely long comments, like one long string
        self.comment = comment

    def everything(self): #gets everything from this
        name = self.name
        garden_owned  = list(self.gardensowned.keys()) # List of all keys, aka gardens this guy owns
        member_of = list(self.gardensmember.keys()) #List of all gardens member of
        rating = str(self.rating.total_rating)
        rating_count = str(self.rating.num_ratings)
        return [name,garden_owned,member_of,rating,rating_count]
    def display(self):
        display_string = ""
        for key in self.gardensowned:
            display_string += self.gardensowned[key].name
        print (self.name, " Is a member of", display_string)

    def rate(self,to_rate,r8ting):

        to_rate.rating.rating_calculator(r8ting)

    def post(self,garden_to_post):
        self.gardensowned[garden_to_post].post_new(input("Insert your post"), input("Image file name?"))



class Coordinate:
    def __init__(self,):
        self.lat = ""
        self.long = ""

    def set_coordinates(self,lat,long):
        self.lat = lat
        self.long = long
class Garden:

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.produce = {}
        self.members = []
        self.rating = Ratings()
        self.posts = []
        self.coordinate = Coordinate()
        self.address = ""


    def add_location(self,address = ''):
        self.address = address
        gmaps = googlemaps.Client(key="AIzaSyBpXBfHdEabuTSvmFki2eIfS5A1-zomBCo")
        results = gmaps.geocode(self.address)
        for result in results:
            geo = result['geometry']
            lat, lng = geo['location']['lat'], geo['location']['lng']
            self.coordinate.set_coordinates(lat,lng)

    def get_loc(self):
        return (self.coordinate.lat,self.coordinate.long)
    def add_member(self,new_member):
        self.members.append(new_member)

    def remove_member(self,old_member):
        self.members.remove(old_member)

    def add_stock(self, produce_to_add):
        if produce_to_add not in self.produce:
            self.produce[produce_to_add] = [produce_to_add.name, 0]
        else:
            self.produce[produce_to_add][1] += 1

    def post_new (self,content,image):
        self.posts.append(content,image) # need to add date time functionality


class Produce:
    def __init__(self, name):
        self.name = name

def create_user(user_name):
    user = User(user_name)
    return user

def user_name(user):
    return user.getname()

def get_owner_list(user):
    return list(user.gardensowned.keys())

def get_member_list(user):
    return list(user.gardensmember.keys())

def create_new_garden(owner,garden_name):
    owner.create(garden_name)

def print_rating(subject):
    print(subject.rating.total_rating)

def join_garden(user,garden):
    user.join_garden(garden)

def leave_garden(user,garden_name):
    user.leave_garden(garden_name)

def rate(user,subject,r8ting):
    if (subject.name in global_list.dict_garden or subject.name in global_users):
        if (user.name in subject.rating.raters): # Update rating to new rating, if user already rated once
            subject.rating.total_rating = ((subject.rating.total_rating * subject.rating.num_ratings) - subject.rating.raters[user.name] +r8ting ) /subject.rating.num_ratings
            subject.rating.raters[user.name] = r8ting
        else:
            subject.rating.raters[user.name] = r8ting
            user.rate(subject,r8ting)
    else:
        print("Subject does not exist")

def get_user_data(username):
    return global_users[username]

def get_garden_data(gardenname):
    return global_list.dict_garden[gardenname][0]

def update_garden_loc(user,gardenname,address):
    garden = get_garden_data(gardenname)
    user.update_address(garden,address)

def draw_map(address):
    gmaps = googlemaps.Client(key="AIzaSyBpXBfHdEabuTSvmFki2eIfS5A1-zomBCo")
    results = gmaps.geocode(address)
    for result in results:
        geo = result['geometry']
        lat, lng = float(geo['location']['lat']), float(geo['location']['lng'])

    gmap = gmplot.GoogleMapPlotter(lat,lng, 16)

    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    gmap.marker(lat,lng,"red")
    for garde in global_list.dict_garden:
        if(global_list.dict_garden[garde][0].address != ""):
            current_loc = global_list.dict_garden[garde][0].get_loc()
            gmap.marker(current_loc[0], current_loc[1], "#008000")
    gmap.draw("map3.html")

Bob = User("Bob")
Bob.create_garden("Avenue U")
Bob.display()
Bob.create_garden ("Prospect Park")
Bob.display()
Bob2 = User("Bob")
Joe = User("Joe")
Joe.create_garden("Prospect Park")
Joe.create_garden("Joe's Garden")
Joe.display()
Bob.join_garden(Joe.gardensowned["Joe's Garden"])
Bob.leave_garden("Joe's Garden")
garde_boy = get_garden_data("Joe's Garden")

garde_boy.add_location("6 Metrotech  Brooklyn")

garde_boy = get_garden_data("Prospect Park")

garde_boy.add_location("Cadman Plaza Brooklyn ")

Joe.create_garden("Ave B")

garde_boy = get_garden_data("Ave B")

garde_boy.add_location("Fort Greene Brooklyn New York")

Joe.create_garden("Ave C")

garde_boy = get_garden_data("Ave C")

garde_boy.add_location("Building 92 Brooklyn New York")



Joe.create_garden("Ave D")
Joe.join_garden(get_garden_data("Prospect Park"))
garde_boy = get_garden_data("Ave D")

garde_boy.add_location("Brooklyn Heights Promenade Brooklyn New York")

draw_map("2 Metrotech Brooklyn")
print(Joe.rating.total_rating,Joe.rating.num_ratings)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def loginPage():
    return render_template('LoginPage.html')

@app.route('/member/<user>')
def memberprof(user):
    member = get_user_data(user)
    user_info = member.everything()
    return render_template('Member_Activities.html',name = user_info[0],owned = user_info[1][0], member = user_info[2][0],rating = "7",rating_count = "4")
if __name__=="__main__":
    app.run()
    
print("RAN")
>>>>>>> 1599892e0808b9b503ec22ac8d2e1509623e2547
