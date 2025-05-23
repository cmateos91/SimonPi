from flask import Flask, request, jsonify
import requests
import os
import simplejson as json
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configurar headers para la API de Pi Network
api_key = os.getenv('PI_API_KEY', None)
if not api_key:
    logger.warning('PI_API_KEY is missing, limited mode enabled.')


server_header = {
    'Authorization': f'Key {api_key}'
}

app = Flask(__name__)

@app.route('/api/me', methods=['POST'])
def get_user_info():
    try:
        # Obtener el token de acceso del frontend
        access_token = request.json.get('accessToken')
        if not access_token:
            logger.error('No access token provided')
            return jsonify({'error': 'No access token provided'}), 400

        # Configurar headers para la petición al usuario
        user_header = {
            'Authorization': f'Bearer {access_token}'
        }

        # Hacer la petición a la API de Pi Network
        user_url = "https://api.minepi.com/v2/me"
        response = requests.get(user_url, headers=user_header)

        if response.status_code != 200:
            logger.error(f'Failed to get user info: {response.text}')
            return jsonify({'error': 'Failed to get user info'}), 400

        user_data = response.json()
        logger.info(f'Successfully retrieved user info: {user_data}')
        return jsonify(user_data)

    except Exception as e:
        logger.error(f'Error getting user info: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/wallet', methods=['POST'])
def get_wallet_info():
    try:
        # Obtener el token de acceso del frontend
        access_token = request.json.get('accessToken')
        if not access_token:
            logger.error('No access token provided')
            return jsonify({'error': 'No access token provided'}), 400

        # Configurar headers para la petición al usuario
        user_header = {
            'Authorization': f'Bearer {access_token}'
        }

        # Hacer la petición a la API de Pi Network
        wallet_url = "https://api.minepi.com/v1/me"
        response = requests.get(wallet_url, headers=user_header)

        if response.status_code != 200:
            logger.error(f'Failed to get wallet info: {response.text}')
            return jsonify({'error': 'Failed to get wallet info'}), 400

        wallet_data = response.json()
        logger.info(f'Successfully retrieved wallet info: {wallet_data}')
        return jsonify(wallet_data)

    except Exception as e:
        logger.error(f'Error getting wallet info: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 8080)))
