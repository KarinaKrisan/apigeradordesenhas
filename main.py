from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import random
import string
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)

# Configuração do JWT
app.config[
    'JWT_SECRET_KEY'] = 'alterar_aqui'  # Em um cenário real, guarde essa chave em um local seguro.
jwt = JWTManager(app)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={'app_name': "API de Gerador de Senhas"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/login', methods=['POST'])
def login():
  """
    Autenticar um usuário e obter um token JWT.
    """
  user = request.json.get('usuario', None)
  password = request.json.get('senha', None)

  if not user or not password:
    return jsonify({"msg": "Usuário e senha são necessários!"}), 401

  access_token = create_access_token(identity=user)
  return jsonify(access_token=access_token)


@app.route('/generate-password', methods=['POST'])
@jwt_required()
def generate_password():
  """
    Gerar uma senha aleatória.
    """
  data = request.json
  quantidade = data.get('quantidade', 8)
  password = ''.join(
      random.choice(string.ascii_letters + string.digits)
      for _ in range(quantidade))
  return jsonify({"password": password})


@app.route('/swagger.json')
def swagger_json():
  with open('swagger.json', 'r') as f:
    data = json.load(f)  # Carregar o arquivo como JSON
  return jsonify(data)

@app.route('/')
def home():
  return '''
  
  <h1>API de Gerador de Senhas</h1>

  <p>/login para geração do token</p>
  <p>/generate-password para geração da sua senha, lembre-se de usar o "Authorization: Bearer {token}"</p>
  '''


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
