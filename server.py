from flask import Flask, request, jsonify
from flask.views import MethodView
from database import Session, UserModel
from errors import HttpException
from sqlalchemy.exc import IntegrityError
from schema import validate, CreateUserSchema, PatchUserSchema

app = Flask('app')


@app.errorhandler(HttpException)
def error_handler(error: HttpException):
    http_response = jsonify({
        'status': 'error',
        'message': error.message
    })
    http_response.status_code = error.status_code
    return http_response


class UserOps(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise HttpException(
                    status_code=404,
                    message='user not found'
                )
            return jsonify({
                'id': user.id,
                'email': user.email,
                'creation_time': user.creation_time.isoformat()
            })

    def post(self):
        user_data = validate(request.json, CreateUserSchema)
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpException(
                    status_code=409,
                    message='user with such email already exists'
                )
            return jsonify({'id': new_user.id})

    def patch(self):
        pass

    def delete(self):
        pass


app.add_url_rule('/users/<int:user_id>/', view_func=UserOps.as_view('users'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserOps.as_view('create_users'), methods=['POST'])

if __name__ == '__main__':
    app.run()
