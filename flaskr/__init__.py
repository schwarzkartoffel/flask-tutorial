import os
from flask import Flask, Response, request
import json
from bson.objectid import ObjectId

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.mongo')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # import db
    from . import db

    # Need to call this method with the app context
    with app.app_context():
        client = db.get_db()

    collection = client.school.students

    # CREATE
    @app.route('/student', methods=["POST"])
    def create_student():
        try:
            student = {
                "name" : request.form["name"],
                "roll": request.form["roll"],
                "age": request.form["age"]
            }
            db_response = collection.insert_one(student)
            return Response(
                response= json.dumps(
                    {
                        "message" : "Student created",
                        "id" : f"{db_response.inserted_id}"
                    }
                ),
                status=200,
                mimetype="application/json"
            )
        except Exception as ex:
            print("-----------------")
            print(ex)
            print("-----------------")
            return Response(
                response= json.dumps(
                    {
                        "message" : "Could not create student",
                    }
                ),
                status=500,
                mimetype="application/json"
            )
        finally:
            db.close_db()
    
    # READ
    @app.route("/student", methods=["GET"])
    def get_all_students():
        try:
            data = list(collection.find())
            for student in data:
                student["_id"] = str(student["_id"])
            return Response(
                response= json.dumps(data),
                status=200,
                mimetype="application/json"
            )
        except Exception as ex:
            print("-----------------")
            print(ex)
            print("-----------------")
            return Response(
                response= json.dumps(
                    {
                        "message" : "Could not get students",
                    }
                ),
                status=500,
                mimetype="application/json"
            )
        finally:
            db.close_db()
    
    # UPDATE
    @app.route("/student/<id>", methods=["PUT"])
    def update_student(id):
        try:
            db_response = collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"name": request.form["name"]}}
            )
            if db_response.modified_count < 1:
                return Response(
                    response=json.dumps({"message": "No students modified"}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Student updated"}),
                    status=200,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("-----------------")
            print(ex)
            print("-----------------")
            return Response(
                response= json.dumps(
                    {
                        "message" : "Could not update student",
                    }
                ),
                status=500,
                mimetype="application/json"
            )
        finally:
            db.close_db()

    # DELETE
    @app.route("/student/<id>", methods=["DELETE"])
    def delete_student(id):
        try:
            db_response = collection.delete_one(
                {"_id": ObjectId(id)},
            )
            if db_response.deleted_count < 1:
                return Response(
                    response=json.dumps({"message": "No students deleted"}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Student deleted", "id": id}),
                    status=200,
                    mimetype="application/json"
                )
        except Exception as ex:
            print("-----------------")
            print(ex)
            print("-----------------")
            return Response(
                response= json.dumps(
                    {
                        "message" : "Could not delete student",
                    }
                ),
                status=500,
                mimetype="application/json"
            )
        finally:
            db.close_db()

    return app
