document.addEventListener('DOMContentLoaded', function() {
    const bars = document.querySelectorAll('.bar-chart');
    bars.forEach(bar => {
        const ratio = parseFloat(bar.dataset.ratio);
        const width = Math.abs(ratio) * 10; // 10을 곱해 더 큰 막대를 만듭니다
        bar.style.width = `${width}px`;
    });
});