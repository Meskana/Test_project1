from my_app import app, db


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #print("All tables created")

        # Drop all tables
        #db.drop_all()
        #print("All tables dropped")
    app.run(debug=True)
