from website import create_app

app = create_app()

if __name__ == "__main__":
    # app.run is going run flask app
    # debug=True is going rerun the
    # server everytime we make any change
    app.run(debug=True)
