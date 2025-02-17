from flask import make_response

class CreatePlayerService:
    def __init__(self, dbHelper):
        self._dbHelper = dbHelper

    def create_account(self, request):
        db = self._dbHelper.get_db()
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Ensure name, email, and password are provided
        if not name or not email or not password:
            return make_response('Name, email and password are required', 400)

        # Insert data into the Player table
        result = db['Player'].insert({
            'name': name,
            'email': email,
            'password': password
        })
        return make_response('Account created successfully', 201)