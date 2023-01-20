from flask import Flask
from flask.views import MethodView

app = Flask('app')


class UserOps(MethodView):

    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


app.add_url_rule('/users/<int:user_id>/', view_func=UserOps.as_view('users'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserOps.as_view('create_users'), methods=['POST'])

if __name__ == '__main__':
    app.run()
