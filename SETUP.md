# 🚗 Car Evaluation Classifier - API Flask

Uma API Flask que serve um modelo de avaliação de carros pré-treinado através de uma interface web intuitiva.

## 📋 Características

- ✅ API REST com Flask
- ✅ Interface web responsiva e moderna
- ✅ Suporte a CORS
- ✅ Predições em tempo real
- ✅ Exibição de probabilidades por classe
- ✅ Validação de entrada
- ✅ Tratamento de erros

## 🗂️ Estrutura do Projeto

```
postgraduate-software-engineer-car-classifier/
├── app.py                          # Aplicação Flask principal
├── requirements.txt                # Dependências Python
├── modelo_car_evaluation.joblib   # Modelo treinado
├── label_encoder.joblib            # Encoder para rótulos
├── ordinal_encoder.joblib          # Encoder ordinal
├── templates/
│   └── index.html                  # Interface HTML
└── static/
    ├── style.css                   # Estilos CSS
    └── script.js                   # JavaScript cliente
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000`

## 📖 Como Usar

1. **Abra o navegador** e acesse `http://localhost:5000`
2. **Preencha o formulário** com os parâmetros do veículo:
   - Preço de Compra
   - Preço de Manutenção
   - Número de Portas
   - Capacidade de Passageiros
   - Tamanho do Porta-Malas
   - Classificação de Segurança

3. **Clique em "Fazer Predição"**
4. **Visualize o resultado** com a classificação e confiança por classe

## 🔌 Endpoints da API

### GET `/`
Serve a página inicial da aplicação.

**Resposta:** HTML da interface web

---

### POST `/api/predict`
Realiza uma predição com base nos parâmetros fornecidos.

**Request Body:**
```json
{
  "buying": "high",
  "maint": "med",
  "doors": "4",
  "persons": "4",
  "lug_boot": "big",
  "safety": "high"
}
```

**Response (Sucesso 200):**
```json
{
  "success": true,
  "prediction": "vgood",
  "prediction_code": 3,
  "input_data": {
    "buying": "high",
    "maint": "med",
    "doors": "4",
    "persons": "4",
    "lug_boot": "big",
    "safety": "high"
  },
  "probabilities": {
    "unacc": 0.05,
    "acc": 0.15,
    "good": 0.30,
    "vgood": 0.50
  }
}
```

**Response (Erro 400/500):**
```json
{
  "error": "Mensagem de erro descritiva"
}
```

---

### GET `/api/model-info`
Retorna informações sobre o modelo carregado.

**Response:**
```json
{
  "model_name": "Car Evaluation Model",
  "model_type": "RandomForestClassifier",
  "status": "loaded",
  "features": ["buying", "maint", "doors", "persons", "lug_boot", "safety"],
  "classes": ["unacc", "acc", "good", "vgood"]
}
```

## ⚙️ Configuração

### Ajustar Features do Modelo

Se seu modelo tiver features diferentes, edite a função `get_feature_names()` em `app.py`:

```python
def get_feature_names():
    return [
        'feature1',
        'feature2',
        'feature3',
        # ... adicione todas as features do seu modelo
    ]
```

### Ativar/Desativar Debug

Em `app.py`, linha final:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

- `debug=True`: Modo desenvolvimento (auto-reload)
- `debug=False`: Modo produção

### Mudar Porta

```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Porta 8000
```

## 📊 Parametrização do Modelo

O modelo espera os seguintes parâmetros (ajuste conforme necessário):

| Parâmetro | Valores | Descrição |
|-----------|---------|-----------|
| `buying` | vhigh, high, med, low | Preço de compra do veículo |
| `maint` | vhigh, high, med, low | Preço de manutenção |
| `doors` | 2, 3, 4, 5 | Número de portas |
| `persons` | 2, 4, more | Capacidade de passageiros |
| `lug_boot` | small, med, big | Tamanho do porta-malas |
| `safety` | low, med, high | Classificação de segurança |

## 🐛 Troubleshooting

### Erro: "Modelos não foram carregados"
- Verifique se os arquivos `.joblib` estão no mesmo diretório de `app.py`
- Certifique-se de que os arquivos não estão corrompidos

### Erro: "CORS bloqueado"
- O Flask-CORS está configurado para aceitar requisições de todas as origens
- Para restringir, edite `app.py`: `CORS(app, resources={r"/api/*": {"origins": "seu-dominio.com"}})`

### Modelo retorna predição incorreta
- Verifique se os valores de entrada correspondem ao esperado pelo modelo
- Valide os tipos de dados das features
- Confirme que os encoders estão sendo aplicados corretamente

## 📝 Notas Importantes

1. **Validação de Entrada**: A função `prepare_features()` pode ser expandida para incluir validações mais rigorosas
2. **Transformações**: Se seu modelo requer transformações específicas, adicione-as em `prepare_features()`
3. **Segurança**: Para produção, configure adequadamente:
   - CORS com origens específicas
   - Validação robusta de entrada
   - Rate limiting
   - HTTPS

## 🔄 Próximos Passos

Para melhorar a API:

1. Adicionar autenticação e autorização
2. Implementar caching de predições
3. Adicionar logging detalhado
4. Criar testes unitários
5. Containerizar com Docker
6. Deployar em servidor de produção (Heroku, AWS, Azure, etc.)

## 📄 Licença

Este projeto é fornecido como está.

## 👥 Autor

Desenvolvido como parte de projeto acadêmico de Pós-Graduação em Engenharia de Software.

---

**Dúvidas ou sugestões?** Entre em contato ou abra uma issue no repositório.
