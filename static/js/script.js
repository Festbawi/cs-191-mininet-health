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
    var adjOpenBtn = document.getElementById('adj-modal-open');
    var adjCloseBtn = document.getElementById('adj-modal-close');
    adjOpenBtn.addEventListener("click", function() {
        document.getElementById("adj-modal").style.display = "";
    });
    adjCloseBtn.addEventListener("click", function() {
        document.getElementById("adj-modal").style.display = "none";
    });

    var verifyBtn = document.getElementById('verify-btn');
    var resultDiv = document.getElementById('result-div');
    var resultPre = document.getElementById('result-pre');
    verifyBtn.addEventListener("click", function() {
        resultDiv.style.display = "";
        resultPre.innerHTML = '';
        window.scrollTo(0, document.body.scrollHeight);
        ajaxStream('/verify', resultPre);
    });
}

window.onload = onLoad