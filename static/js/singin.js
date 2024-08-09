document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signin-form');
    
    form.addEventListener('submit', function(event) {
        const userId = document.getElementById('user_id').value;
        const password = document.getElementById('user_password').value;

        if (!userId || !password) {
            event.preventDefault();
            alert('아이디와 비밀번호를 모두 입력해주세요.');
        }
    });
});