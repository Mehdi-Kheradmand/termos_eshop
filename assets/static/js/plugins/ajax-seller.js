

function do_jobs(isSuperuser = false){
    let index;

    let crf = $('input[name=csrfmiddlewaretoken]').val();
    let the_button = document.getElementById("btn_submit");
    the_button.value = "در‌حال پردازش";

    disable_enable_all_inputs(false);
    ShowTitleAlert(false);
    ShowStockPriceAlert(false);

    let inputs = document.getElementsByTagName('input');

    let DataId = [];
    let DataTitle = [];
    let DataStock = [];
    let DataPrice = [];
    let DataSellPrice = [];

    let DataIndex = 0;

    let step = 4; // For SuperUser
    if (isSuperuser){
        step += 1;
    }

    for (index = 0; index < (inputs.length-step); index +=step) {

        console.log(" ---------- ");

        DataId[DataIndex] = inputs[index].id.trim().replace(/,/g, ''); // ID
        DataId[DataIndex] = DataId[DataIndex].replace(/ /g, '');
        console.log("ID is : " + DataId[DataIndex]);
        if (! isNumeric(DataId[DataIndex])){
            return reload_page();
        }

        DataTitle[DataIndex] = inputs[index+1].value.trim(); //Title
        console.log("title is : " + DataTitle[DataIndex]);
        if (DataTitle[DataIndex] == null || DataTitle[DataIndex] === ''){
            return ShowTitleAlert(true);
        }

        DataStock[DataIndex] = inputs[index+2].value.trim().replace(/,/g, ''); // Stock
        DataStock[DataIndex] = DataStock[DataIndex].replace(/ /g, '');
        console.log("Stock is : " + DataStock[DataIndex]);
        if (! isNumeric(DataStock[DataIndex])){
            return ShowStockPriceAlert(true);
        }

        DataPrice[DataIndex] = inputs[index+3].value.trim().replace(/,/g, ''); // EntryPrice
        DataPrice[DataIndex] = DataPrice[DataIndex].replace(/ /g, '');
        console.log("Price is : " + DataPrice[DataIndex]);
        if (! isNumeric(DataPrice[DataIndex])){
            return ShowStockPriceAlert(true);
        }

        if (isSuperuser){
            DataSellPrice[DataIndex] = inputs[index+4].value.trim().replace(/,/g, ''); // SellPrice
            DataSellPrice[DataIndex] = DataSellPrice[DataIndex].replace(/ /g, '');
            console.log("SellPrice is : " + DataSellPrice[DataIndex]);
            if (! isNumeric(DataSellPrice[DataIndex])){
                return ShowStockPriceAlert(true);
            }
        }

        DataIndex +=1;
    }

    $.ajax({
        url: '/profile/seller/',
        type: 'post',
        data: {
            DataId,
            DataTitle,
            DataStock,
            DataPrice,
            DataSellPrice,
            csrfmiddlewaretoken: crf,
        },

        success: function(response) {

            let error = check_and_show_errors(response);

            if (! error){ // If there is no Error
                success_alert();
                make_page_normal(false);
            }
        },
        error: function () {
            alert('خطا! لطفا دوباره اقدام کنید ');
            window.location.reload();
        }
    });
}



function make_page_normal(scroll_top = false, enable_submit = false, remove_alerts = false){
    disable_enable_all_inputs(true);
    let the_button = document.getElementById("btn_submit");
    the_button.value = "ثبت اطلاعات";

    if(remove_alerts){
        ShowTitleAlert(false);
        ShowStockPriceAlert(false);
    }

    if (enable_submit){
        enable_submit_button();
    }else {
        enable_submit_button(false);
    }
    if (scroll_top){
        window.scrollTo(0, 0);
    }
}

function check_and_show_errors(response){
    let error = false;

    if(response['error_list']['stock_price']){
        alert("stock_price Error");
        ShowStockPriceAlert(true);
        error = true;
    }
    if(response['error_list']['title']){
        alert("Title Error");
        ShowTitleAlert(true);
        error = true;
    }
    return error;
}

// ============================================== Alerts

function success_alert(show = true){
    let elem = document.getElementById("success_alert");
    if (show){
        elem.removeAttribute('hidden');
    }else{
        elem.setAttribute('hidden', "hidden");
    }
}

function ShowStockPriceAlert(force) {
    let _alert = document.getElementById('alert_stock_price');
    if (force){
        _alert.removeAttribute("hidden")
        make_page_normal(true);
    } else {
        _alert.setAttribute("hidden", "hidden")
    }
}

function ShowTitleAlert(force){
    let _alert = document.getElementById("alert_title");
    if (force) {
        _alert.removeAttribute("hidden");
        make_page_normal(true);
    } else {
        _alert.setAttribute("hidden", "hidden")
    }
}

function disable_enable_all_inputs(en_true_dis_false){
    let inputs, index;

    inputs = document.getElementsByTagName('input');
    for (index = 0; index < inputs.length; ++index) {
        if (en_true_dis_false === false){
            inputs[index].setAttribute("disabled", "disabled");
        }else{
            inputs[index].removeAttribute("disabled");
        }
    }
}

function reload_page(){
    window.location.reload();
}

function enable_submit_button(enable = true){
    let the_button = document.getElementById('btn_submit');
    if (enable){
        the_button.removeAttribute("disabled");
    }else {
        the_button.setAttribute("disabled", '');
    }
}

function isNumeric(str) {
    if (str == null || str === ''){
        console.log("Null input");
        return false;
    }

    console.log("Before per to eng : " + str);
    str = toEnglishNumber(str);
    console.log("After per to eng : " + str);

    for (let i=0; i < str.length; i++) {
        if (!(/^\d$/.test(str[i]))) {
            return false
        }
    }
    return true
}

function toEnglishNumber(strNum) {
    let pn = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
    let en = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

    let cache = strNum;
    for (let i = 0; i < 10; i++) {
        let regex_fa = new RegExp(pn[i], 'g');
        cache = cache.replace(regex_fa, en[i]);
    }
    //$('#'+name).val(cache);
    return cache;
}

// Key Press

function value_changed(val){
    console.log(val);
    if (val == null || val === ''){
        make_page_normal(false, false, false);
    }else {
        make_page_normal(false, true, true);
    }
}
