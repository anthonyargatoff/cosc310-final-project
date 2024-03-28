from flask import Blueprint, render_template, request, redirect

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

@auth.route('/admin')
def admin_page():
    return render_template('Admin.html')

@auth.route('/accountmanagement')
def accountmanager_page():
    return render_template('accountManagement.html')