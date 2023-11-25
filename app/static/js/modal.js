function fillForm(prompt, negative_prompt, seed, height, width, steps) {
        document.getElementById('prompt').value = prompt;
        document.getElementById('negative_prompt').value = negative_prompt;
        document.getElementById('seed').value = seed;
        document.getElementById('height').value = height;
        document.getElementById('width').value = width;
        document.getElementById('steps').value = steps;
        $('#preferencesModal').modal('hide');
    }

    // Funkcja do pobrania wartości cookie (dla tokena CSRF)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function deletePreference(preferenceId) {
        if(confirm('Czy na pewno chcesz usunąć te preferencje?')) {
            fetch(`/delete-preference/${preferenceId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => {
                if(response.status === 204) {
                    // Usuń element z DOM tylko wtedy, gdy odpowiedź jest pomyślna
                    const element = document.getElementById('preference-row-' + preferenceId);
                    if(element) {
                        element.remove();
                    }
                    showAlert('Preferencje zostały usunięte. Odśwież stronę.');
                } else {
                    showAlert('Wystąpił błąd podczas usuwania preferencji.', true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Wystąpił błąd podczas usuwania preferencji.', true);
            });
        }
    }


    function showAlert(message, isError = false) {
        const alertBox = document.getElementById('alert-box');
        alertBox.textContent = message;
        alertBox.className = isError ? 'alert alert-danger' : 'alert alert-success';
        alertBox.style.display = 'block';
    }