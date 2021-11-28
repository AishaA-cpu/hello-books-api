from flask import Blueprint, jsonify, make_response, request # python supports comma separated importing
from app import db
from app.models.book import Book
from app.models.author import Author

# create the blue print in routes.py
# define the function to create the app in __init__.py 
# create the flask object in __init__.py in the function
# import the blue print object in the function from routes.py
# register the blue print we have created with the flask object
# define an end point using the blueprint we have created as a decorator 
# . route holds all our end points
# you can see errors in the log in terminal
# you can put that endpoint in a browser to see the error 
# the error can show up nicely in a browser if we have debugging mode turned on 
# to activate debugging mode 
# terminal export FLASK_ENV = development , this sets the flask environment variable to development
# flask run 
# this shows us the error in development code 
# we can also do FLASK_ENV="development" && flask run
# another benefit to using dev environment is that it does a hot reload. essentially it reloads when you save and restarts 
# you dont have to kill and restart the server 
# we can also use the debugger with flask 
# jsonify, flask utility that turns its args into a JSON. 
# jsonify will turn list of books dict into a response object
# if you have a dictionary, you can alwys just return a dict, since it looks like a json, but if you have something else you may need jsonify


books_bp = Blueprint("books_bp", __name__,url_prefix="/books")# blueprint instance names books_bp use it to group routes that stsrat with
#                                                         # /books. __name__ provides info bp uses for aspects of routing
#                                                         # use this BP for all RESTful routes that start with /books.
#                                                         # we add the optional url_prefic so all endpoints relating to books uses this prefix
#                                     # by adding /books we dont have to add that prefix for every route, it will adopt this,
#                                     # it is typical for all restful routes to have a url prefix
#                                     # define an end point

authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@books_bp.route("", methods=["POST" , "GET"])
def handle_books():
    request_body = request.get_json() # this allows us access the body in the request sent
    if request.method == "POST":
        #request_body = request.get_json() # makes sense to try to retrieve RB inside a post request?
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid request, you must include a title and description", 400)
        
        new_book = Book(
            title = request_body["title"],
            description = request_body["description"] # if we left out description in the body of our request
        )  # we get a key error becase new book will be trying to access description when there is non
                # think of error handling, handle the code, error, etc 
                # it is important to do error handling and request handling because we dont want garbage in out DB
        db.session.add(new_book) # staging the changes we are making i.e the new book instance
        db.session.commit() #commit the changes made to the database

        return make_response(
            #{"key": "value"}, 201
            f"Book {new_book.title} created", 201 # this returns None when tested, why? 
            # #confirm to user that request was created and successful
        ) # message can also be returned without using the "make_response object"
        # default is 200 for successful request so if we left of 201 the response will carry 200 status code
        # 201 says request was created 

#@books_bp.route("", methods = ["GET"])
#def handle_books(): # dint pass book in here, because books is already definied as a global variable
    elif request.method == "GET":
        books_response = []

        title_query = request.args.get("title") # get query params from request, 
        if title_query != None: # check if there is a title, this works for checking with title 
            books = Book.query.filter_by(title = title_query) # filter by title column and assign to books 
        else:
            books = Book.query.all() # book is using th query.all method inherited from the db.Model
        #book_json_object = {}
        
        for book in books:
            # book_json_object["id"] = book.id
            # book_json_object["title"] = book.title
            # book_json_object["description"] = book.description
            # books_response.append(book_json_object)

            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                }
            )
        
        return jsonify(books_response) # here, jsonify turns a list into a json object which still looks like a list tbh.


@books_bp.route("/<book_id>", methods = ["GET", "PUT", "DELETE"]) # in flask we use <> to specifiy params in the route method, here we spec. that route should take the book is, per  
def handle_one_book(book_id):
                # RESTful convensions this says that we want to get one item from a resource, the name in the funct should match

    #request_body = request.get_json()                                                # the params def, note that the data passed into the param on line 72 will be a string we must convert or else
    #book_id = int(book_id)   # get method takes a parameter and handles the id as a string     # line 77 wont eval to true remeber you can use type() as a debugger
    # for book in books:
    #     if book.id == book_id:
    #         return {
    #             "title" : book.title,
    #             "id" : book.id,
    #             "description" : book.description
    #         }, 200
    #try:
    # if book == None:
    #     return f"the book is not available"
    # else:
    book = Book.query.get(book_id) 
    if request.method == "GET":
        try:
            return {
                    "title" : book.title,
                    "id" : book.id,
                    "description" : book.description
            }
        except:
            book is None
            return make_response(f" Book {book_id} is not found", 404)

    if request.method == "PUT":
        form_data = request.get_json() 
        if "title" not in form_data or "description" not in form_data:
            return make_response(f"Invalid request, requires both a title and description", 400)
        else:
            try:
                book.title = form_data["title"]
                book.description = form_data["description"]

                # save action
                #db.session.add(book)
                db.session.commit()
                return make_response(f"Book #{book.id} successfully updated", 200)
            except:
                book == None
                return make_response(f"{book.id} does not exist", 404)
        
    if request.method == "DELETE":
        try:
            book_to_delete = book

            # update and save action 
            db.session.delete(book_to_delete)
            db.session.commit()
            return make_response(f"Book #{book.id} successfully deleted", 200)
        except:
            book is None
            return make_response(f" Book {book_id} is not found", 404)

@authors_bp.route("", methods=["POST" , "GET"])
def handle_authors():
    request_body = request.get_json() 
    if request.method == "POST":
        
        if "name" not in request_body:
            return make_response("Invalid request, you must include a name and description", 400)
        
        new_author = Author(
            name = request_body["name"],
            description = request_body["description"] 
        )  
        db.session.add(new_author) 
        db.session.commit() 

        return make_response(
            f"Book {new_author.name} created", 201 
        ) 


    elif request.method == "GET":
        author_response = []

        name_query = request.args.get("name") 
        if name_query != None: 
            authors = Author.query.filter_by(title = name_query) 
        else:
            authors  = Author.query.all() 

        
        for author in authors:
            author_response.append(
                {
                    "id": author.id,
                    "name": author.name,
                }
            )
        
        return jsonify(author_response)

# @books_bp.route("/<book_id>", methods = ["GET"]) # in flask we use <> to specifiy params in the route method, here we spec. that route should take the book is, per  
# def handle_one_book(book_id):
#                 # RESTful convensions this says that we want to get one item from a resource, the name in the funct should match
#     book = Book.query.get(book_id)                                                   # the params def, note that the data passed into the param on line 72 will be a string we must convert or else
#     #book_id = int(book_id)   # get method takes a parameter and handles the id as a string     # line 77 wont eval to true remeber you can use type() as a debugger






















# hello_world_bp = Blueprint("hello_world", __name__) # hello_world is the name of the blueprint
# # __name__ is the import name helps flask identify where the root folder of the project is 



# id = 1
# #route = "/" + str(id)
# #@books_bp.route(route, methods = ["GET"])
# @books_bp.route("/<book_id>", methods = ["GET"]) # in flask we use <> to specifiy params in the route method, here we spec. that route should take the book is, per  
# def handle_book(book_id):                              # RESTful convensions this says that we want to get one item from a resource, the name in the funct should match
#     #book_by_ id = {}                                     # the params def, note that the data passed into the param on line 72 will be a string we must convert or else
#     #book_id = id                                          # line 77 wont eval to true remeber you can use type() as a debugger
#     for book in books:
#         if str(book.id) == book_id:
#             return {
#                 "title" : book.title,
#                 "id" : book.id,
#                 "description" : book.description
#             }, 200
#     return ("oh oh! the book is not available homie")




# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description                             



# books = [ # temp hard coded database
#     Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]



# @hello_world_bp.route("/hello-world", methods = ["GET"]) # define the name of your end point as the first arg. remeber it needs to align with the resource
# def get_hello_world():                                  # hellow_world_bp here remember is an instance of BP and has a method route that helps set the end point
#     my_response = "Hello World"         # define the method, here we use a GET because we want client to only be able to get from this endpoint
#     return my_response            # to run it, you need to run the server with "flask run"
                            



# @hello_world_bp.route("/hello-world-json", methods = ["GET"]) 
# def get_hello_world_json():                                                         
#     return {
#         "name": "Aisha",
#         "task": "her first json",
#         "project": "flask Api",
#         "mood": "Whoop!"
#     }, 200  