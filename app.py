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

# Definição dos nomes das features
FRONTEND_FEATURES = [
    'buying_price',  # preço de compra (inteiro)
    'maint_cost',    # custo de manutenção (inteiro)
    'doors',         # número de portas (string)
    'persons',       # capacidade de passageiros (string)
    'lug_boot_liters',  # capacidade do porta-malas (inteiro)
    'safety'         # classificação de segurança (string)
]

MODEL_FEATURES = [
    'buying',   # preço de compra (categórico)
    'maint',    # custo de manutenção (categórico)
    'doors',    # número de portas (categórico)
    'persons',  # capacidade de passageiros (categórico)
    'lug_boot', # capacidade do porta-malas (categórico)
    'safety'    # classificação de segurança (categórico)
]

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
            'frontend_features': FRONTEND_FEATURES,
            'model_features': MODEL_FEATURES,
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
        # Validar features do frontend
        for feature in FRONTEND_FEATURES:
            if feature not in data:
                return None  # Feature obrigatória faltando
        
        # Criar um dicionário com os dados do frontend
        features_dict = {feature: data[feature] for feature in FRONTEND_FEATURES}
        
        # Criar dicionário para os dados do modelo
        model_data = {}
        
        # Aplicar mapeamentos para campos numéricos e provenientes do frontend
        map_numerical_to_categorical(features_dict, model_data)
        
        # Verificar se todos os features do modelo estão presentes
        for feature in MODEL_FEATURES:
            if feature not in model_data:
                return None
        
        # Converter para DataFrame
        df = pd.DataFrame([model_data])
        
        # Aplicar transformações
        if ordinal_encoder:
            df = pd.DataFrame(ordinal_encoder.transform(df), columns=ordinal_encoder.get_feature_names_out())
            pass
        
        return df.values
    
    except Exception as e:
        print(f"Erro ao preparar features: {e}")
        return None


def map_numerical_to_categorical(frontend_data, model_data):
    """
    Mapeia valores numéricos para categorias categóricas conforme especificado
    Recebe frontend_data (com valores do frontend) e model_data (para adicionar valores mapeados)
    """
    # 1. Mapeamento de Preço de Compra (Buying)
    if 'buying_price' in frontend_data:
        buying_price = float(frontend_data['buying_price'])
        if buying_price >= 300000:
            model_data['buying'] = 'vhigh'
        elif buying_price >= 150000:
            model_data['buying'] = 'high'
        elif buying_price >= 80000:
            model_data['buying'] = 'med'
        else:
            model_data['buying'] = 'low'
    
    # 2. Mapeamento de Custo de Manutenção Anual (Maint)
    if 'maint_cost' in frontend_data:
        maint_cost = float(frontend_data['maint_cost'])
        if maint_cost >= 25000:
            model_data['maint'] = 'vhigh'
        elif maint_cost >= 12000:
            model_data['maint'] = 'high'
        elif maint_cost >= 6000:
            model_data['maint'] = 'med'
        else:
            model_data['maint'] = 'low'

    model_data['doors'] = frontend_data.get('doors', '4')

    model_data['persons'] = frontend_data.get('persons', '4')
    
    # 3. Mapeamento de Porta-malas (Lug_boot)
    if 'lug_boot_liters' in frontend_data:
        lug_boot_liters = float(frontend_data['lug_boot_liters'])
        if lug_boot_liters >= 450:
            model_data['lug_boot'] = 'big'
        elif lug_boot_liters >= 300:
            model_data['lug_boot'] = 'med'
        else:
            model_data['lug_boot'] = 'small'

    model_data['safety'] = frontend_data.get('safety', 'med')

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
