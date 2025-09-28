from flask import Flask, request, render_template_string

app = Flask(__name__)

# ------------------------------
# User class with getter/setter
# ------------------------------
class User:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    # Getter
    @property
    def age(self):
        return self._age

    # Setter
    @age.setter
    def age(self, value):
        if value >=self._age :
            self._age = value
        else:
            raise ValueError("Age cannot be negative!")

# ------------------------------
# Routes
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    user = User("Sharana", 25)  # default user

    if request.method == "POST":
        try:
            new_age = int(request.form["age"])
            user.age = new_age  # Setter validates the age
            message = f"User age updated to {user.age}"
        except ValueError as e:
            message = str(e)

    return render_template_string("""
        <h2>User: {{ user._name }}</h2>
        <h3>Current Age: {{ user.age }}</h3>
        <form method="POST">
            <input type="number" name="age" placeholder="Enter new age">
            <button type="submit">Update Age</button>
        </form>
        <p>{{ message }}</p>
    """, user=user, message=message)


if __name__ == "__main__":
    app.run(debug=True)
