// wait for the DOM to be loaded
$(document).ready(function() {
    var getLocation = function(href) {
    var l = document.createElement("a");
    l.href = href;
    return l;
    };
    // bind 'myForm' and provide a simple callback function
    $('#myForm').submit(function() {
        var ans = $('#ans').val();
        console.log(ans == 'ים השיבולים');
        var url = window.location.pathname;
        //var p =
        var path = getLocation(url).pathname;
        console.log(path);
        //alert("ans: "+ans == '40');
        switch(path) {
          case path = '/gvura/':
            if (ans == '40'){
                $('#success').show();
                $('#fail').hide();
                }
                else{$('#fail').show()}
            break;
          case path = '/hapoelBeitShean/':
            if (ans == '70'){
                $('#success').show();
                $('#fail').hide();
                }
                else{$('#fail').show()}
            break;
          case path = '/semel/':
            if (ans == '100'){
                $('#success').show();
                $('#fail').hide();
                }
                else{$('#fail').show()}
            break;
          case path = '/nofey/':
            if (ans == '300'){
                $('#success').show();
                $('#fail').hide();
                }
                else{$('#fail').show()}
            break;
          case path = '/tarbut1/':
            if (ans == 'ים השיבולים'){
                console.log("got here")
                $('#success2').show();
                $('#fail2').hide();
                }
                else{$('#fail2').show()}
            break;
          case path = '/tarbut2/':
            if (ans == '30'){
                $('#success').show();
                $('#fail').hide();
                }
                else{$('#fail').show()}
            break;
          case path = '/shichrur1/':
            if (ans == 'תל בית שאן'){
                $('#success2').show();
                $('#fail2').hide();
                }
                else{$('#fail2').show()}
            break;
          case path = '/shichrur2/':
            if (ans == '10'){
                $('#success').show();
                $('#fail').hide();
                }
                else{$('#fail').show()}
            break;
          default:
            console.log(path)
            // code block
        }
//        if (ans == '40' & url.includes('gvura')){$('#success').show();$('#fail').hide();}else if (url.includes('gvura')){$('#fail').show()}
//        if (ans == '70' & url.includes('hapoelBeitShean')){$('#success').show();$('#fail').hide();}else if (url.includes('hapoelBeitShean')){$('#fail').show()}
//        if (ans == '100' & url.includes('semel')){$('#success').show();$('#fail').hide();}else if (url.includes('semel')){$('#fail').show()}
//        if (ans == '300' & url.includes('nofey')){$('#success').show();$('#fail').hide();}else if (url.includes('nofey')){$('#fail').show()}
//        if (ans == '30' & url.includes('tarbut2')){$('#success').show();$('#fail').hide();}else if (url.includes('tarbut2')){$('#fail').show()}
//        if (ans == '10' & url.includes('shichrur2')){$('#success').show();$('#fail').hide();}else if (url.includes('shichrur2')){$('#fail').show()}
//        if (ans == 'ים השיבולים' & url.includes('tarbut1')){$('#success2').show();$('#fail2').hide();}else if (url.includes('tarbut1')){$('#fail2').show()}
//        if (ans == 'תל בית שאן' & url.includes('shichrur1')){$('#success2').show();$('#fail2').hide();}else if (url.includes('shichrur1')){$('#fail2').show()}
    });
});