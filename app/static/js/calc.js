$(document).ready(function() {

    $('.updateButton').on('click', function() {

        req = $.ajax({
            url : '/calc',
            type : 'POST',
            data : { ExxBlendPCT : ExxBlendPCT, GasEthPCT : GasEthPCT, GasOct : GasOct }
        });

        req.done(function(data) {});


    });

});