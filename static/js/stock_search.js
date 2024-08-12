$(document).ready(function() {
    var searchTimeout;
    $('#stock-search').on('input', function() {
        clearTimeout(searchTimeout);
        var query = $(this).val();
        searchTimeout = setTimeout(function() {
            if (query.length > 0) {
                $.ajax({
                    url: '/stock/search_stocks/',  // URL 수정
                    data: {
                        'query': query
                    },
                    success: function(data) {
                        var results = $('#search-results');
                        results.empty();
                        if (data.stocks && data.stocks.length > 0) {
                            var list = $('<ul style="list-style-type: none; padding: 0;">');
                            data.stocks.forEach(function(stock) {
                                list.append($('<li style="padding: 5px; cursor: pointer;">').text(stock.code + ' - ' + stock.name)
                                    .click(function() {
                                        $('#stock-search').val(stock.code);
                                        results.empty();
                                    }));
                            });
                            results.append(list);
                        } else {
                            results.text('일치하는 주식이 없습니다.');
                        }
                    },
                    error: function() {
                        $('#search-results').text('검색 중 오류가 발생했습니다.');
                    }
                });
            } else {
                $('#search-results').empty();
            }
        }, 300);
    });
});