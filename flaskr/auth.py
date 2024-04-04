from flask import Blueprint, render_template, request, redirect, session

# create blueprint
auth = Blueprint('auth', __name__)

# routes 


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # check for post request
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        print(email, pw)
        # need to figure out how to access the remember me checkbox
        # next steps are to incorporate the database and setup credential validation
        # from here redirect to the main page which is search page
        # next steps for the redirect would be to include a payload to dynamically display public user data like their username
        return redirect('/search')
        
    return render_template('login.html')

@auth.route('/notifications', methods=['GET','POST'])
def addNotificaton():
    if request.method == 'POST':
        location = request.form.get('location')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
        radius = request.form.get('radius')
        minMagnitude = request.form.get('minMagnitude')
        maxMagnitude = request.form.get('maxMagnitude')
        userID = session.get('userid')  # get user id from session
        sql = "INSERT INTO notifications (location, longitude, latitude, radius, minMagnitude, maxMagnitude, userid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        #add database functionality here
        con = sqlite3.connect("flaskr/main.db")
        cursor = con.cursor()
        cursor.execute(sql, (location, longitude, latitude, radius, minMagnitude, maxMagnitude, userID))
        con.commit()
        con.close()
        return redirect('/notifications')
    return render_template('manageNotifications.html')

@auth.route('/admin')
def admin_page():
    return render_template('Admin.html')

@auth.route('/signup', methods =['GET', 'POST'])
def signup_page():
     if request.method == 'POST':
         return redirect('/search')
     return render_template('Signup.html')

@auth.route('/account')
def accountmanager_page():
    return render_template('manageAccount.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        #add database functionality here  
        return redirect('/search')
     return render_template('Signup.html')

@auth.route('/notifications')
def nottificationmanager_page():
    return render_template('manageNotifications.html')

