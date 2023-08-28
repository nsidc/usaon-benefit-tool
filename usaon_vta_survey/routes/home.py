from usaon_vta_survey import app


@app.route("/home")
def root():
    return "Welcome!"
