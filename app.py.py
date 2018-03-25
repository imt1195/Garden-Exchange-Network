from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def loginPage():
return render_template('LoginPage.html')

@app.route('/map')
def map():
return render_template('map.html')

@app.route('/member')
def memberActivities():
return render_template('Member_Actvities.html')

@app.route('/test')
def testingPage():
return render_template('TestingPage.html')


if __name__=="__main__":
    app.run()
    
    
