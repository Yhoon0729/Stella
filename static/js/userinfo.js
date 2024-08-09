document.addEventListener('DOMContentLoaded', function() {
    console.log('사용자 정보 페이지가 로드되었습니다.');

    // 정보 수정 버튼 클릭 이벤트
    const editInfoBtn = document.querySelector('.bg-blue-500');
    if (editInfoBtn) {
        editInfoBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('정보 수정 기능은 아직 구현되지 않았습니다.');
        });
    }

    // 비밀번호 변경 버튼 클릭 이벤트
    const changePasswordBtn = document.querySelector('.bg-red-500');
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            alert('비밀번호 변경 기능은 아직 구현되지 않았습니다.');
        });
    }
});