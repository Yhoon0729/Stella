document.addEventListener('DOMContentLoaded', function() {
    fetch(`/api/stock/${stockCode}/chart-data/`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('stockChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: '주가',
                        data: data.prices,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: '최근 30일 주가 변동'
                        }
                    }
                }
            });
        });
});