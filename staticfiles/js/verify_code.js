document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const codeInput = document.getElementById('code');

    form.addEventListener('submit', function(event) {
        if (codeInput.value.length !== 6) {
            event.preventDefault();
            alert('인증 코드는 6자리여야 합니다.');
        }
    });
});