// Elementos do DOM
const predictionForm = document.getElementById('predictionForm');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const predictionResult = document.getElementById('predictionResult');
const errorMessage = document.getElementById('errorMessage');
const probabilitiesContainer = document.getElementById('probabilitiesContainer');
const probabilitiesList = document.getElementById('probabilitiesList');

// Event Listeners
predictionForm.addEventListener('submit', handleSubmit);

// Função para preparar dados do formulário
function getFormData() {
    const formData = new FormData(predictionForm);
    const data = {};
    
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    return data;
}

// Função para validar formulário
function validateForm() {
    const inputs = predictionForm.querySelectorAll('select');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value) {
            isValid = false;
            input.style.borderColor = '#c33';
        } else {
            input.style.borderColor = '#e0e0e0';
        }
    });
    
    return isValid;
}

// Função para enviar dados ao servidor
async function handleSubmit(e) {
    e.preventDefault();
    
    // Validar formulário
    if (!validateForm()) {
        showError('Por favor, preencha todos os campos');
        return;
    }
    
    // Mostrar spinner de carregamento
    showLoading(true);
    hideError();
    hideResult();
    
    try {
        // Preparar dados
        const data = getFormData();
        
        // Enviar requisição
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        // Processar resposta
        const result = await response.json();
        
        showLoading(false);
        
        if (response.ok && result.success) {
            displayResult(result);
        } else {
            showError(result.error || 'Erro ao processar a predição');
        }
    } catch (error) {
        showLoading(false);
        showError(`Erro de conexão: ${error.message}`);
        console.error('Erro:', error);
    }
}

// Função para exibir resultado
function displayResult(result) {
    // Exibir predição principal
    predictionResult.textContent = result.prediction;
    
    // Exibir probabilidades se disponíveis
    if (result.probabilities && Object.keys(result.probabilities).length > 0) {
        displayProbabilities(result.probabilities);
        probabilitiesContainer.style.display = 'block';
    } else {
        probabilitiesContainer.style.display = 'none';
    }
    
    // Mostrar seção de resultado
    showResult();
}

// Função para exibir probabilidades
function displayProbabilities(probabilities) {
    probabilitiesList.innerHTML = '';
    
    // Ordenar probabilidades em ordem decrescente
    const sorted = Object.entries(probabilities)
        .sort((a, b) => b[1] - a[1]);
    
    sorted.forEach(([className, probability]) => {
        const percentage = (probability * 100).toFixed(1);
        
        const item = document.createElement('div');
        item.className = 'probability-item';
        
        item.innerHTML = `
            <span class="probability-class">${className}</span>
            <div class="probability-bar">
                <div class="probability-fill" style="width: ${percentage}%"></div>
            </div>
            <span class="probability-value">${percentage}%</span>
        `;
        
        probabilitiesList.appendChild(item);
    });
}

// Funções auxiliares para mostrar/ocultar elementos
function showLoading(show) {
    loadingSpinner.style.display = show ? 'block' : 'none';
}

function showResult() {
    resultSection.style.display = 'block';
    errorSection.style.display = 'none';
    loadingSpinner.style.display = 'none';
    
    // Scroll para o resultado
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

function hideResult() {
    resultSection.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultSection.style.display = 'none';
    loadingSpinner.style.display = 'none';
    
    // Scroll para o erro
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    errorSection.style.display = 'none';
}

// Função para resetar formulário
function resetForm() {
    predictionForm.reset();
    hideResult();
    hideError();
    
    // Scroll para o topo
    document.querySelector('main').scrollIntoView({ behavior: 'smooth' });
}

// Remover estilos de erro ao mudar de campo
document.querySelectorAll('select').forEach(select => {
    select.addEventListener('change', function() {
        if (this.value) {
            this.style.borderColor = '#e0e0e0';
        }
    });
});

// Carregar informações do modelo ao iniciar
document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/api/model-info');
        const info = await response.json();
        console.log('Informações do modelo:', info);
    } catch (error) {
        console.error('Erro ao carregar informações do modelo:', error);
    }
});
