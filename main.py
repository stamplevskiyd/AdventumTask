from backend import app, db
from backend.views import *


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print(app.url_map)
    print(dir())
    app.run(debug=True)