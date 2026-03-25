import os
import joblib
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd

# Inicializar a aplicação Flask
app = Flask(__name__)
CORS(app)

# Diretório base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carregar os modelos e encoders
try:
    modelo = joblib.load(os.path.join(BASE_DIR, 'modelo_car_evaluation.joblib'))
    label_encoder = joblib.load(os.path.join(BASE_DIR, 'label_encoder.joblib'))
    ordinal_encoder = joblib.load(os.path.join(BASE_DIR, 'ordinal_encoder.joblib'))
    print("✓ Modelos carregados com sucesso")
except Exception as e:
    print(f"✗ Erro ao carregar os modelos: {e}")
    modelo = None
    label_encoder = None
    ordinal_encoder = None


@app.route('/')
def index():
    """Rota para servir a página inicial"""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Endpoint para fazer predições
    Espera um JSON com os parâmetros do modelo
    """
    try:
        # Obter dados da requisição
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400
        
        # Validar se modelo foi carregado
        if modelo is None:
            return jsonify({'error': 'Modelo não foi carregado corretamente'}), 500
        
        # Preparar os dados para predição
        # Aqui você precisa ajustar de acordo com os nomes das features do seu modelo
        features = prepare_features(data)
        
        if features is None:
            return jsonify({'error': 'Dados inválidos ou incompletos'}), 400
        
        # Fazer predição
        prediction = modelo.predict(features)
        prediction_proba = modelo.predict_proba(features) if hasattr(modelo, 'predict_proba') else None
        
        # Decodificar a predição se houver label_encoder
        if label_encoder:
            prediction_label = label_encoder.inverse_transform(prediction)[0]
        else:
            prediction_label = prediction[0]
        
        # Preparar resposta
        response = {
            'success': True,
            'prediction': str(prediction_label),
            'prediction_code': int(prediction[0]),
            'input_data': data
        }
        
        # Adicionar probabilidades se disponíveis
        if prediction_proba is not None:
            classes = label_encoder.classes_ if label_encoder else list(range(len(prediction_proba[0])))
            probabilities = {str(cls): float(prob) for cls, prob in zip(classes, prediction_proba[0])}
            response['probabilities'] = probabilities
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro na predição: {str(e)}'}), 500


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Endpoint para obter informações sobre o modelo"""
    try:
        info = {
            'model_name': 'Car Evaluation Model',
            'model_type': type(modelo).__name__ if modelo else 'Unknown',
            'status': 'loaded' if modelo else 'not_loaded',
            'features': get_feature_names(),
            'classes': list(label_encoder.classes_) if label_encoder else []
        }
        return jsonify(info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def prepare_features(data):
    """
    Prepare os features para o modelo
    IMPORTANTE: Ajuste esta função de acordo com os nomes reais das features do seu modelo
    """
    try:
        # Exemplo de features esperadas (AJUSTE CONFORME SEU MODELO)
        feature_names = get_feature_names()
        
        # Criar um dicionário com os dados
        features_dict = {}
        
        for feature in feature_names:
            if feature in data:
                features_dict[feature] = data[feature]
            else:
                return None  # Feature obrigatória faltando
        
        # Converter para DataFrame
        df = pd.DataFrame([features_dict])
        
        # Aplicar transformações se necessário
        if ordinal_encoder:
            # Aplicar ordinal encoding se necessário
            # df = pd.DataFrame(ordinal_encoder.transform(df), columns=ordinal_encoder.get_feature_names_out())
            pass
        
        return df.values
    
    except Exception as e:
        print(f"Erro ao preparar features: {e}")
        return None


def get_feature_names():
    """
    Retorna os nomes das features esperadas pelo modelo
    IMPORTANTE: Atualize isto com os nomes reais do seu modelo
    """
    # Tente obter do modelo se possível
    if hasattr(modelo, 'feature_names_in_'):
        return list(modelo.feature_names_in_)
    
    # Caso contrário, retorne uma lista padrão
    # AJUSTE CONFORME SEU MODELO
    return [
        'buying',
        'maint',
        'doors',
        'persons',
        'lug_boot',
        'safety'
    ]


@app.errorhandler(404)
def not_found(error):
    """Tratamento para rota não encontrada"""
    return jsonify({'error': 'Rota não encontrada'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Tratamento para erro interno"""
    return jsonify({'error': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    print("🚀 Iniciando API Flask para Car Classifier...")
    app.run(debug=True, host='0.0.0.0', port=5000)
