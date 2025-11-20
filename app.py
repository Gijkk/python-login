from flask import Flask, request, render_template_string

app = Flask(__name__)

# Fake database
users = {
    "admin": "123456"
}

login_page = """
<!DOCTYPE html>
<html>
<body>
    <h2>Login</h2>
    <form method="POST">
        <label>Username:</label><br>
        <input type="text" name="username"><br>
        <label>Password:</label><br>
        <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    <p>{{ message }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            message = "Login successful!"
        else:
            message = "Invalid username or password!"

    return render_template_string(login_page, message=message)

if __name__ == "__main__":
    app.run(debug=True)
