document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const emailInput = document.getElementById('email');

    form.addEventListener('submit', function(event) {
        if (!isValidEmail(emailInput.value)) {
            event.preventDefault();
            alert('올바른 이메일 주소를 입력해주세요.');
        }
    });

    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});