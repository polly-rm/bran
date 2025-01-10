<!-------- Prevent Negative Numbers in Inputs -------->
function preventNegativeNums() {
    let numInput = document.querySelectorAll('input[type="number"]:not([id*="temperature"])');

    for (let i = 0, len = numInput.length; i < len; i++) {
        if (numInput[i].id)
            numInput[i].addEventListener('input', function () {
                let num = this.value;
                if (num < 0) {
                    this.value = Math.abs(num);
                }
            }, false);
    }
}


<!-------- Prevent Decimal Numbers in Count -------->
function preventDecimalsInCount() {
    let countInput = document.querySelectorAll('input[type="number"][id$="-count"]');

    for (let i = 0, len = countInput.length; i < len; i++) {
        if (countInput[i].id)
            countInput[i].addEventListener('input', function () {
                let num = this.value;
                if (num % 1 !== 0) {
                    this.value = Math.round(num);
                }
            })
    }
}


<!-------- Get Decimal Places Count of Num -------->
function getDecimalPlaces(value) {
    const parts = value.split('.');
    if (parts.length === 2) {
        return parts[1].length;
    } else {
        return 0;
    }
}


<!-------- Prevent More Decimal Places in Inputs -------->
function preventMoreDecimalPlaces() {
    let numInput = document.querySelectorAll('input[type="number"]');

    for (let i = 0, len = numInput.length; i < len; i++) {
        if (numInput[i].id)
            numInput[i].addEventListener('input', function () {
                let num = this.value;
                const decimalPlaces = getDecimalPlaces(num);

                if (decimalPlaces > 2) {
                    this.value = num.toString().match(/^-?\d+(?:\.\d{0,2})?/)[0];
                }
            }, false);
    }
}


<!-------- Display Param Units in Inputs -------->
function showUnit() {
    $(":input[type=number]").on('input', function () {
        if ($(this).val()) {
            $(this).parent().find('.param-unit').show();
        } else {
            $(this).parent().find('.param-unit').hide();
        }
    })
}