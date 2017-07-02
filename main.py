from flask import Flask, request, redirect, render_template
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), "templates")  # creates path to templates file via splicing the current directory path (links to templates directory)
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)  # creates jinja2 environment to load templates from template folder

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    # encoded_error = request.args.get("error")
    return render_template("signup.html") #, watchlist=get_current_watchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

def is_filled(val):
    if val != "":  # if val == empty string
        return True  # return True
    else:  # if val == empty string
        return False  # return False

def no_whitespace(val):
    whitespace = " "
    if whitespace not in val:
        return True
    else:
        return False

def validate_email(val):
    # regex for e-mails: /[a-z0-9_]+\.?[a-z0-9_]+@[a-z]+\.[a-z]+/i
    # alternate: "[a-zA-Z0-9_]+\.?[a-zA-Z0-9_]+@[a-z]+\.[a-z]+"
    valid_email = re.compile("[a-zA-Z0-9_]+\.?[a-zA-Z0-9_]+@[a-z]+\.[a-z]+")
    if valid_email.match(val):
        return True
    else:
        return False

@app.route("/validate-form", methods=["POST"])
def validate():
    # ----------------- LOGIC -------------------
    # if any of the first three fields are empty:
        # display error message "This field cannot be empty" next to field

    # check username and password for validity:
        # if len(username) or len(password) < 3 or > 20:
            # display error message "Must be between 3 and 20 characters"
        # if username or password contains whitespace:
            # display error message "Spaces are not allowed"

    # check password and validation for identity:
        # if not same, display error message "Passwords must match"

    # if not empty, check email for validity:
        # if len(email) < 3 or > 20:
            # display error message "Must be between 3 and 20 characters"
        # if email contains whitespace:
            # display error message "Spaces are not allowed"
        # if number of . and number of @ != 1:
            # display error message "Email must contain exactly one '.' and one '@' symbol"

    # --------------- FUNCTION ------------------
    username_input = request.form['username']  # grabs user data from form field "username"
    password_input = request.form['password']  # grabs user data from form field "password"
    verify_input = request.form['verify']  # grabs user data from form field "verify"
    email_input = request.form['email']  # grabs user data from form field "email"

    username_error = ""  # create variable to hold error message for this field
    password_error = ""  # ditto
    verify_error = ""  # ditto
    email_error = ""  # ditto]

    # --------------- LONG FORM -----------------
    if not is_filled(username_input):
        username_error = "This field cannot be empty"
        username_input = ""
    else:
        username_len = len(username_input)
        if  username_len > 20 or username_len < 3:
            username_error = "Username must be between 3 and 20 characters"
            username_input = ""
        else:
            if not no_whitespace(username_input):
                username_error = "Spaces are not allowed"
                username_input = ""

    if not is_filled(password_input):
        password_error = "This field cannot be empty"
        password_input = ""
    else:
        password_len = len(password_input)
        if  password_len > 20 or password_len < 3:
            password_error = "Password must be between 3 and 20 characters"
            password_input = ""
        else:
            if not no_whitespace(username_input):
                password_error = "Spaces are not allowed"
                username_input = ""

    if not is_filled(verify_input):
        verify_error = "This field cannot be empty"
        verify_input = ""
    else:
        if verify_input != password_input:
            verify_error = "Passwords must match"
            verify_input = ""

    if not is_filled(email_input):
        email_error = "This field cannot be empty"
        email_input = ""
    else:
        email_len = len(email_input)
        if  email_len > 20 or email_len < 3:
            email_error = "Email must be between 3 and 20 characters"
            email_input = ""
        else:
            if not validate_email(email_input):
                email_error = "Not a valid email"
                email_input = ""

    # ------------ REFACTORING ATTEMPT ------------
    # fields = ["username", "password", "verify"]
    # for field in fields:
    #     field_input = field + "_input"
    #     field_len = len(field_input)
    #     field_error = field + "_error"
    #     if not is_filled(field_input):
    #         field_error = "This field cannot be empty"
    #         field_input = ""
    #     else:
    #         if field_len > 20 or field_len < 3:
    #             field_error = field + " must be between 3 and 20 characters"
    #             field_input = ""

    # -------------- ERROR CHECK ----------------
    if not username_error and not password_error and not verify_error and not email_error:  # if we don't have any error messages:
        return render_template("welcome.html", username=username_input)
    else:
        return render_template ("signup.html", username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error)

    # return render_template("welcome.html", username=username_input)

app.run()
