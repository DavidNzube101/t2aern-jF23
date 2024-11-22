from website import initialize_app

app = initialize_app()

if __name__ == '__main__':
    # app.run()
    app.run(port=3450, debug=True)