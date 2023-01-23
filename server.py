from flask import Flask, request, jsonify
from flask.views import MethodView
from database import Session, UserModel

app = Flask('app')


class UserOps(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            return jsonify({
                'id': user.id,
                'email': user.email,
                'creation_time': user.creation_time.isoformat()
            })

    def post(self):
        user_data = request.json
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            session.commit()
            return jsonify({'id': new_user.id})

    def patch(self):
        pass

    def delete(self):
        pass


app.add_url_rule('/users/<int:user_id>/', view_func=UserOps.as_view('users'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserOps.as_view('create_users'), methods=['POST'])

if __name__ == '__main__':
    app.run()
