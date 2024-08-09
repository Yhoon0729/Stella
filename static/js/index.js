document.addEventListener('DOMContentLoaded', function() {
    console.log('Stella 인덱스 페이지가 로드되었습니다.');

    // 실시간 시계 기능
    function updateClock() {
        const now = new Date();
        const clockElement = document.getElementById('real-time-clock');
        if (clockElement) {
            clockElement.textContent = now.toLocaleTimeString('ko-KR');
        }
    }

    setInterval(updateClock, 1000);
    updateClock(); // 초기 로드 시 즉시 시간 표시

    // 여기에 인덱스 페이지 특정 JavaScript 코드를 추가하세요
});