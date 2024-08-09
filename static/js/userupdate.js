document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('edit-info-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // 간단한 클라이언트 측 유효성 검사
        const userName = document.getElementById('user_name').value;
        const userEmail = document.getElementById('user_email').value;

        if (!userName || !userEmail) {
            alert('모든 필드를 채워주세요.');
            return;
        }

        // 이메일 형식 검사
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(userEmail)) {
            alert('올바른 이메일 형식이 아닙니다.');
            return;
        }

        // 모든 검사를 통과하면 폼 제출
        form.submit();
    });
});