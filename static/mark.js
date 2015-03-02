function addEvent(element, evnt, funct){
    if (element.attachEvent)
        return element.attachEvent('on'+evnt, funct);
    else
        return element.addEventListener(evnt, funct, false);
}

function unmark() {
    var source_div = document.getElementById('source_html');
    var text = source_div.innerHTML;
    source_div.innerHTML = text.replace(/<\/?mark[^>]*>/g,'');
}

function markTag() {
    // unmark any currently-marked tags, otherwise our matching will fail
    unmark();
    var source_div = document.getElementById('source_html');
    var text = source_div.innerHTML;
    var tag_to_mark = this.text;
    // match the tag only if followed by whitespace or a >
    // that way we don't match <b> and <body> with the same regex
    var regexstring = '&lt;' + tag_to_mark + '(?=\\s|&gt)';
    console.log(regexstring);
    var regexp = new RegExp(regexstring, 'g');
    var marked = text.replace(regexp, '&lt;<mark>' + tag_to_mark + '</mark>');
    source_div.innerHTML = marked;
}
    
function unmark() {
    var source_div = document.getElementById('source_html');
    var text = source_div.innerHTML;
    source_div.innerHTML = text.replace(/<\/?mark[^>]*>/g,'');
}

function addMarkListeners() {
    var as = document.getElementsByTagName('a');
    for (var i=0; i<as.length; i++) {
        console.log('adding event!');
        as[i].addEventListener("click", markTag, false);
    }
}

// from http://stackoverflow.com/questions/8644428/how-to-highlight-text-using-javascript

