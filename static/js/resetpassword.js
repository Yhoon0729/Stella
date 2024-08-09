document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const newPasswordInput = document.getElementById('new_password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    form.addEventListener('submit', function(event) {
        if (newPasswordInput.value !== confirmPasswordInput.value) {
            event.preventDefault();
            alert('비밀번호가 일치하지 않습니다.');
        } else if (!isStrongPassword(newPasswordInput.value)) {
            event.preventDefault();
            alert('비밀번호는 최소 8자 이상이며, 대문자, 소문자, 숫자, 특수문자를 포함해야 합니다.');
        }
    });

    newPasswordInput.addEventListener('input', function() {
        updatePasswordStrength(this.value);
    });

    function isStrongPassword(password) {
        const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return re.test(password);
    }

    function updatePasswordStrength(password) {
        const strengthMeter = document.querySelector('.password-strength-meter');
        if (!strengthMeter) return;

        if (password.length < 8) {
            strengthMeter.className = 'password-strength-meter weak';
        } else if (password.length < 10) {
            strengthMeter.className = 'password-strength-meter medium';
        } else {
            strengthMeter.className = 'password-strength-meter strong';
        }
    }
});