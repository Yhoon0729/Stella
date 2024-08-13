document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');

    form.addEventListener('submit', function(event) {

        // 폼 유효성 검사
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        const gender = document.getElementById('gender').value;
        const agreeTerms = document.getElementById('agree-terms').checked;

        if (password !== confirmPassword) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
        }

        if (!agreeTerms) {
            alert('이용약관에 동의해주세요.');
            return;
        }

        // 여기에 서버로 데이터를 전송하는 로직을 추가하세요
        console.log('회원가입 정보:', { username, email, gender });
        alert('회원가입이 완료되었습니다!');

        // 실제 구현에서는 서버로 데이터를 전송하고 응답을 처리해야 합니다.
    });
});