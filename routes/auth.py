from flask import Blueprint, request
from utils.auth_utils import token_required, generate_token
from utils.factory import createPlayerController

auth_bp = Blueprint('auth', __name__)
playerController = createPlayerController()

@auth_bp.route('/create-account', methods=["POST"])
def create_account():
    res = playerController.create_account(request)
    email = request.form.get('email')
    if res.status_code == 201:
        token = generate_token(email)
        res.set_cookie('auth_token', token, httponly=True, secure=True, samesite='none')
    return res

@auth_bp.route('/login', methods=["POST"])
def login():
    res = playerController.login(request)
    email = request.form.get('email')
    if res.status_code == 202:
        token = generate_token(email)
        res.set_cookie('auth_token', token, httponly=True, secure=True, samesite='none')
    return res

@auth_bp.route('/logout', methods=["POST"])
@token_required
def logout():
    return playerController.logout()

@auth_bp.route('/check-auth')
@token_required
def check_auth():
    return 'This is a check auth route'