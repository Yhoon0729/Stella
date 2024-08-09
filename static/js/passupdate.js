document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('change-password-form');

    form.addEventListener('submit', function(event) {

        const currentPassword = document.getElementById('current_password').value;
        const newPassword = document.getElementById('new_password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        // 간단한 클라이언트 측 유효성 검사
        if (!currentPassword || !newPassword || !confirmPassword) {
            alert('모든 필드를 채워주세요.');
            return;
        }

        if (newPassword !== confirmPassword) {
            alert('새 비밀번호와 확인 비밀번호가 일치하지 않습니다.');
            return;
        }

        // 모든 검사를 통과하면 폼 제출
        form.submit();
    });
});