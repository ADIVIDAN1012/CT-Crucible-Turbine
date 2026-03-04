# This file is the entry point for the Gunicorn server.
from form_backend import app

if __name__ == "__main__":
    app.run()
