document.addEventListener('DOMContentLoaded', function() {
    const bars = document.querySelectorAll('.bar');
    bars.forEach(bar => {
        const ratio = parseFloat(bar.getAttribute('data-ratio'));
        const width = Math.abs(ratio) * 5; // 5를 곱해 그래프를 더 크게 표시
        bar.style.width = `${Math.min(width, 100)}%`; // 최대 100%를 넘지 않도록
    });
});