// Based on https://www.binarytides.com/ajax-based-streaming-without-polling/
function ajaxStream(url, resultDiv) {
    if (!window.XMLHttpRequest) {
        console.error("Your browser does not support XMLHttpRequest.")
    }

    try {
        var xhr = new XMLHttpRequest();
        xhr.previousText = '';

        xhr.onerror = function(e) {
            console.log(xhr);
            console.log(xhr.responseText);
            console.error(e);
        }

        xhr.onreadystatechange = function() {
            try {
                if (xhr.readyState > 2) {
                    var newResponse = xhr.responseText.substring(xhr.previousText.length);
                    var newResponses = newResponse.split('||');
                    for (var i = 0; i < newResponses.length; i++) {
                        if (newResponses[i].length == 0) {
                            continue;
                        }
                        var result = JSON.parse(newResponses[i]);
                        console.log(result);
                        // resultDiv.innerHTML += '<div class="siimple-box-' + result.type + '">' + result.message + '</div>';
                        // if (/\r|\n/.exec(result.message)) {
                        //     resultDiv.innerHTML += '<br/>';
                        // }
                        resultDiv.innerHTML += result;
                    }
                    xhr.previousText = xhr.responseText;
                }
            } catch (e) {
                console.error(e);
            }
        }

        xhr.open("GET", url, true);
        xhr.send();    
    } catch (e) {
        console.error(e);
    }
}

function onLoad() {
    var verifyBtn = document.getElementById('verify-btn');
    var resultDiv = document.getElementById('result-div');
    verifyBtn.onclick = function() {
        console.log('Verify button pressed');
        resultDiv.innerHTML = resultDiv.getAttribute('original-content');
        ajaxStream('/verify', resultDiv);
    }
}

window.onload = onLoad