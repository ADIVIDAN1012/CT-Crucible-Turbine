from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Orbit Project Manager</title></head>
    <body style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h1>Orbit Project Manager</h1>
        <p>Deployment successful! Database setup in progress.</p>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
