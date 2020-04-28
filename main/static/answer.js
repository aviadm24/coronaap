// wait for the DOM to be loaded
$(document).ready(function() {
    // bind 'myForm' and provide a simple callback function
    $('#myForm').submit(function() {
        var ans = $('#ans').val();
        console.log(ans == 'ים השיבולים');
        var url = window.location.pathname;
        console.log(url.includes('tarbut1'));
        //alert("ans: "+ans == '40');
        if (ans == '40' & url.includes('gvura')){$('#success').show();$('#fail').hide();}else if (url.includes('gvura')){$('#fail').show()}
        if (ans == '70' & url.includes('hapoelBeitShean')){$('#success').show();$('#fail').hide();}else if (url.includes('hapoelBeitShean')){$('#fail').show()}
        if (ans == '100' & url.includes('semel')){$('#success').show();$('#fail').hide();}else if (url.includes('semel')){$('#fail').show()}
        if (ans == '300' & url.includes('nofey')){$('#success').show();$('#fail').hide();}else if (url.includes('nofey')){$('#fail').show()}
        if (ans == '30' & url.includes('tarbut2')){$('#success').show();$('#fail').hide();}else if (url.includes('tarbut2')){$('#fail').show()}
        if (ans == '10' & url.includes('shichrur2')){$('#success').show();$('#fail').hide();}else if (url.includes('shichrur2')){$('#fail').show()}
        if (ans == 'ים השיבולים' & url.includes('tarbut1')){$('#success2').show();$('#fail2').hide();}else if (url.includes('tarbut1')){$('#fail2').show()}
        if (ans == 'תל בית שאן' & url.includes('shichrur1')){$('#success2').show();$('#fail2').hide();}else if (url.includes('shichrur1')){$('#fail2').show()}
    });
});