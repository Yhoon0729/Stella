$(document).ready(function() {
    var searchTimeout;
    $('#stock-search').on('input', function() {
        clearTimeout(searchTimeout);
        var query = $(this).val();
        searchTimeout = setTimeout(function() {
            if (query.length > 0) {
                $.ajax({
                    url: '/stock/search_stocks/',
                    data: {
                        'query': query
                    },
                    success: function(data) {
                        var results = $('#search-results');
                        results.empty();
                        if (data.stocks && data.stocks.length > 0) {
                            var list = $('<ul class="list-none p-0">');
                            data.stocks.forEach(function(stock) {
                                list.append($('<li class="p-2 hover:bg-gray-700 cursor-pointer">')
                                    .text(stock.code + ' - ' + stock.name)
                                    .click(function() {
                                        $('#stock-search').val(stock.code);
                                        results.empty();
                                        $('#stockSearchForm').submit();
                                    }));
                            });
                            results.append(list);
                            results.show();
                        } else {
                            results.hide();
                        }
                    },
                    error: function() {
                        $('#search-results').text('검색 중 오류가 발생했습니다.').show();
                    }
                });
            } else {
                $('#search-results').empty().hide();
            }
        }, 300);
    });

    $(document).click(function(event) {
        if (!$(event.target).closest('#stockSearchForm').length) {
            $('#search-results').hide();
        }
    });
});