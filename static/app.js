var dvRed = 60, dvGreen = 20; //defaults values for slider
var dvs = [dvRed, dvRed + dvGreen];

$(document).ready(function () { //setup slider
    $('#slider').slider({
        min: 0,
        max: 100,
        step: 1,
        values: dvs,
        range: true,
        slide: function (event, ui) {
            $.each(ui.values, function (i, v) {
                updateSlider(); //update vals on change
            });
        }
    });
    updateSlider(); //initial update of values
});

function updateSlider() {
    //get slider values
    var R = Math.round($('#slider').slider('values')[0] * 10) / 10,
        B = Math.round((100 - $('#slider').slider('values')[1]) * 10) / 10,
        G = Math.round(((100 - (R + B))) * 10) / 10;

    //set slider track to 3 colors
    $('.ui-slider').css('background', 'linear-gradient(90deg, #6D6D6D 0% ' + R + '%, #38B0EC ' + R + '% ' + (G + R) + '%, #F9C253 ' + (G + R) + '% 100%');

    //center labels between handles
    $('#val1').html(R + '%').css('left', R / 2 + '%');
    $('#val2').html(G + '%').css('left', R + (G / 2) + '%');
    $('#val3').html(B + '%').css('left', R + G + (B / 2) + '%');

    //set body background color
    var bg = 'rgb(' + R * 255 + ',' + G * 255 + ',' + B * 255 + ')';
    $(document.body).css('background', bg);

    // set return values
    dvRed = R;
    dvGreen = B;
    dvBlue = 100 - (R + B);
    return dvGreen, dvRed, dvBlue;
}

$(document).ready(function () {
    $('select').on('change', function () {
        var selectedValues = [];
        $('select').each(function () {
            var thisValue = this.value;
            if (thisValue !== '')
                selectedValues.push(thisValue);
        }).each(function () {
            $(this).find('option:not(:selected)').each(function () {
                if ($.inArray(this.value, selectedValues) === -1) {
                    $(this).removeAttr('hidden');
                } else {
                    if (this.value !== '')
                        $(this).attr('hidden', 'hidden');
                }
            });
        });
    });
});

function update_selected_values_1() {
    updateSlider()
    update_start_date_value()
    var selected_currency1 = $("#selected_currency_1 option:selected").text(); // select the desired currency
    if (selected_currency1 !== "Wybierz walute 1") {
        var percent_of_investment1 = dvRed;
        var start_date = update_start_date_value()
        location.href = 'details' + '/' + selected_currency1 + '/' + percent_of_investment1 + '/' + start_date // save data
    }
}

function update_selected_values_2() {
    updateSlider()
    update_start_date_value()
    var selected_currency2 = $("#selected_currency_2 option:selected").text(); // select the desired currency
    if (selected_currency2 !== "Wybierz walute 2") {
        var percent_of_investment2 = dvBlue;
        var start_date = update_start_date_value()
        location.href = 'details' + '/' + selected_currency2 + '/' + percent_of_investment2 + '/' + start_date // save data
    }
}

function update_selected_values_3() {
    updateSlider()
    update_start_date_value()
    var selected_currency3 = $("#selected_currency_3 option:selected").text(); // select the desired currency
    if (selected_currency3 !== "Wybierz walute 3") {
        var percent_of_investment3 = dvGreen;
        var start_date = update_start_date_value()
        location.href = 'details' + '/' + selected_currency3 + '/' + percent_of_investment3 + '/' + start_date // save data
    }
}

// Trigger calculate view
function calc() {
    location.href = 'calculate'
}


function push_investment() {
    updateSlider()
    update_start_date_value()
    var selected_currency_1 = $("#selected_currency_1 option:selected").text(); // select the desired currency
    var selected_currency_2 = $("#selected_currency_2 option:selected").text();
    var selected_currency_3 = $("#selected_currency_3 option:selected").text();
    if ((selected_currency_1 === "Wybierz walute 1") || (selected_currency_2 === "Wybierz walute 2") || (selected_currency_3 === "Wybierz walute 3")) {
        alert("Należy wybrać wszystkie 3 waluty") // validate select tags
    } else {
        setTimeout(update_selected_values_1, 1)
        setTimeout(update_selected_values_2, 2)
        setTimeout(update_selected_values_3, 3)
        setTimeout(calc, 500)
    }
}

function refresh_website() {
    window.location.reload(true)
}

function update_website() {
    push_investment()
    setTimeout(refresh_website, 3000)
}

// set start portfolio value
var start_value = 1000

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        start_value = response.start_value;
    }
});

// set portfolio value after 30 days
var account_balance = null

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        account_balance = response.portfolio_value;
    }
});

// set percent changes
var account_changes = null;

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        account_changes = response.portfolio_changes;
    }
});

// set diff between start and end portfolio value
var account_diff = null;

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        account_diff = response.portfolio_diff;
    }
});

// set portoflio percent for cur1
var portfolio_cur1 = null;

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        portfolio_cur1 = response.portfolio_cur1;
    }
});

// set portoflio percent for cur2
var portfolio_cur2 = null;

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        portfolio_cur2 = response.portfolio_cur2;
    }
});

// set portoflio percent for cur2
var portfolio_cur3 = null;

$.ajax({
    url: '/charts/data',
    async: false,
    success: function (response) {
        portfolio_cur3 = response.portfolio_cur3;
    }
});


