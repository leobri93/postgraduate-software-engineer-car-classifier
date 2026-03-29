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
- ✅ Testes unitários incluídos

## 🗂️ Estrutura do Projeto

```
postgraduate-software-engineer-car-classifier/
├── app.py                          # Aplicação Flask principal
├── requirements.txt                # Dependências Python
├── test_model.py                   # Testes unitários
├── modelo_car_evaluation.joblib   # Modelo treinado
├── label_encoder.joblib            # Encoder para rótulos
├── ordinal_encoder.joblib          # Encoder ordinal
├── templates/
│   └── index.html                  # Interface HTML
├── static/
│   ├── style.css                   # Estilos CSS
│   └── script.js                   # JavaScript cliente
├── .venv/                          # Ambiente virtual Python
├── .git/                           # Controle de versão Git
└── __pycache__/                    # Cache Python
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para controle de versão)

### 1. Clonar ou Baixar o Projeto

```bash
git clone <url-do-repositorio>
cd postgraduate-software-engineer-car-classifier
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar os Testes (Opcional)

```bash
python test_model.py
```

### 5. Executar a Aplicação

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000`

## 📖 Como Usar

1. **Abra o navegador** e acesse `http://localhost:5000`
2. **Preencha o formulário** com os parâmetros do veículo:
   - **Preço de Compra (R$)**: Valor numérico em reais
   - **Custo de Manutenção Anual (R$)**: Valor numérico em reais
   - **Número de Portas**: 2, 3, 4 ou 5+
   - **Capacidade de Passageiros**: 2, 4 ou mais de 5
   - **Capacidade do Porta-Malas (litros)**: Valor numérico em litros
   - **Classificação de Segurança**: Baixa, Média ou Alta

3. **Clique em "Fazer Predição"**
4. **Visualize o resultado** com a classificação em português (Inaceitável, Aceitável, Bom, Muito Bom)

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
  "buying_price": 250000,
  "maint_cost": 15000,
  "doors": "4",
  "persons": "4",
  "lug_boot_liters": 350,
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
    "buying_price": 250000,
    "maint_cost": 15000,
    "doors": "4",
    "persons": "4",
    "lug_boot_liters": 350,
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

## 🧪 Testes

O projeto inclui testes unitários para validar o funcionamento do modelo e das funções de preparação de dados.

### Executar Testes

```bash
python test_model.py
```

### Cobertura dos Testes

- ✅ Validação de entrada com valores float
- ✅ Tratamento de dados inválidos
- ✅ Predições do modelo
- ✅ Mapeamento de valores numéricos para categorias
- ✅ Testes específicos para cada parâmetro (buying_price, maint_cost, lug_boot_liters)

## 📦 Dependências

As dependências estão listadas em `requirements.txt`:

```
flask
flask-openapi3
flask-cors
joblib
numpy
pandas
scikit-learn
```

## 🐛 Troubleshooting

### Erro: "Modelos não foram carregados"
- Verifique se os arquivos `.joblib` estão no mesmo diretório de `app.py`
- Certifique-se de que os arquivos não estão corrompidos

### Erro: "CORS bloqueado"
- O Flask-CORS está configurado para aceitar requisições de todas as origens
- Para restringir, edite `app.py`: `CORS(app, resources={r"/api/*": {"origins": "seu-dominio.com"}})`

### Erro nos Testes
- Certifique-se de que o ambiente virtual está ativado
- Verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`
- Os testes requerem que os arquivos `.joblib` estejam presentes

### Modelo retorna predição incorreta
- Verifique se os valores de entrada correspondem ao esperado pelo modelo
- Valide os tipos de dados das features (números para preços, strings para categorias)
- Confirme que os encoders estão sendo aplicados corretamente
- Os valores numéricos são automaticamente mapeados para categorias

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

1. **Adicionar autenticação e autorização**
2. **Implementar caching de predições**
3. **Adicionar logging detalhado**
4. **Expandir cobertura de testes unitários**
5. **Criar testes de integração para a API**
6. **Containerizar com Docker**
7. **Deployar em servidor de produção (Heroku, AWS, Azure, etc.)**
8. **Adicionar documentação OpenAPI automática com flask-openapi3**
9. **Implementar validação mais robusta de entrada**
10. **Adicionar métricas de performance e monitoramento**

## 📄 Licença

Este projeto é fornecido como está.

---

**Dúvidas ou sugestões?** Entre em contato ou abra uma issue no repositório.

## 📝 Estado Atual do Projeto

Esta versão representa o estado final da aplicação desenvolvida como projeto acadêmico de Pós-Graduação em Engenharia de Software. Inclui:

- ✅ API Flask funcional com endpoints REST
- ✅ Interface web responsiva em português
- ✅ Modelo de machine learning integrado
- ✅ Mapeamento automático de valores numéricos para categorias
- ✅ Testes unitários abrangentes
- ✅ Ambiente virtual configurado
- ✅ Controle de versão com Git
- ✅ Documentação completa

## 👥 Autor

Desenvolvido como parte de projeto acadêmico de Pós-Graduação em Engenharia de Software.

---
