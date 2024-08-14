// 간단한 선형 회귀 모델 생성
async function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 1, inputShape: [1] }));
    model.compile({ loss: 'meanSquaredError', optimizer: 'sgd' });
    return model;
}

// 모델 학습 함수
async function trainModel(model, inputs, labels) {
    const history = await model.fit(inputs, labels, {
        epochs: 100,
        callbacks: { onEpochEnd: (epoch, log) => console.log(`Epoch ${epoch}: loss = ${log.loss}`) }
    });
    return model;
}

// 주가 예측 함수
async function predictPrice(model, inputData) {
    const tensorData = tf.tensor2d(inputData, [inputData.length, 1]);
    const prediction = model.predict(tensorData);
    return prediction.dataSync();
}

// 메인 실행 함수
async function run() {
    // 주가 데이터 준비
    const dates = stockData.map(d => new Date(d.date));
    const prices = stockData.map(d => d.price);

    // 데이터 정규화
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const normalizedPrices = prices.map(p => (p - minPrice) / (maxPrice - minPrice));

    // 학습 데이터 준비
    const inputs = tf.tensor2d(normalizedPrices.slice(0, -1), [normalizedPrices.length - 1, 1]);
    const labels = tf.tensor2d(normalizedPrices.slice(1), [normalizedPrices.length - 1, 1]);

    // 모델 생성 및 학습
    const model = await createModel();
    await trainModel(model, inputs, labels);

    // 다음 거래일 주가 예측
    const lastPrice = normalizedPrices[normalizedPrices.length - 1];
    const prediction = await predictPrice(model, [[lastPrice]]);
    const predictedPrice = prediction[0] * (maxPrice - minPrice) + minPrice;

    // Chart.js를 사용하여 그래프 그리기
    const ctx = document.getElementById('stockChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: '실제 주가',
                    data: prices,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: '예측 주가',
                    data: [...prices, predictedPrice],
                    borderColor: 'rgb(255, 99, 132)',
                    borderDash: [5, 5],
                    pointRadius: 0,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // 예측 결과 표시
    document.getElementById('predictionInfo').innerHTML = `
        <p>다음 거래일 예상 주가: ${predictedPrice.toFixed(2)}원</p>
        <p class="text-sm text-gray-400">
            (이 예측은 간단한 모델을 기반으로 하며, 실제 주가와 다를 수 있습니다.)
        </p>
    `;
}

// 페이지 로드 시 실행
run();