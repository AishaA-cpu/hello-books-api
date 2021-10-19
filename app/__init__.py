from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    from .routes import hello_world_bp # essentially, we are telling the flask framework to import the blueprint we created

    app.register_blueprint(hello_world_bp) # we are telling flask to register the blueprint we created so the server knows about it so it knows to use
                                        # the blue print we created for our routes/endpoints

    from .routes import books_bp       # here  use the same create app because its all for the same app project
    app.register_blueprint(books_bp)  

    return app 





















# def revolve(list, shift):
#     list = list[-shift:] + list[:-shift]
#     print(list)

# arr = [1, 2, 3, 4, 5, 6, 7]

# revolve(arr, 3)
