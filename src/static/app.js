let currentPrediction = null;

document.getElementById('irisForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const features = {
        sepal_length: parseFloat(document.getElementById('sepal_length').value),
        sepal_width: parseFloat(document.getElementById('sepal_width').value),
        petal_length: parseFloat(document.getElementById('petal_length').value),
        petal_width: parseFloat(document.getElementById('petal_width').value)
    };

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(features)
        });

        const result = await response.json();
        
        if (result.error) {
            showResult(`Erreur: ${result.error}`, false);
        } else {
            currentPrediction = { features, ...result };
            showResult(`
                <strong>Prédiction:</strong> ${result.prediction}<br>
                <strong>Confiance:</strong> ${(result.confidence * 100).toFixed(1)}%
            `, true);
            document.getElementById('feedback').style.display = 'block';
        }
    } catch (error) {
        showResult('Erreur de connexion', false);
    }
});

function showResult(message, isSuccess) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = message;
    resultDiv.className = `result ${isSuccess ? 'success' : ''}`;
    resultDiv.style.display = 'block';
}

async function sendFeedback(approved) {
    if (!currentPrediction) return;
    
    try {
        await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...currentPrediction.features,
                prediction: currentPrediction.prediction,
                approved: approved
            })
        });
        
        document.getElementById('feedback').style.display = 'none';
        showResult(`Merci pour votre feedback! ${approved ? '👍' : '👎'}`, true);
    } catch (error) {
        showResult('Erreur lors de l\'envoi du feedback', false);
    }
}