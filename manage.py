from flask_migrate import Migrate
from index import app, db  # import your app and db from app.py

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
