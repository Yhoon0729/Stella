document.getElementById('dateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var startDate = document.getElementById('start_date').value;
    var endDate = document.getElementById('end_date').value;
    window.location.href = `?start_date=${startDate}&end_date=${endDate}`;
});