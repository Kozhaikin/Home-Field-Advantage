function getPrediction() {
    var xhttp = new XMLHttpRequest();
    var url = 'pred/';

    var display_pred = document.getElementById('pred_result');
    xhttp.onreadystatechange = function() {
        var status = xhttp.status;
        display_pred.style.display = 'block';
        if (status === 200) {
            display_pred.innerHTML = this.response;
        } else {
            display_pred.innerHTML = `No result has been found`;
        }
    }
    xhttp.open('GET', url, true);
    xhttp.send();
    window.addEventListener("click", function(event) {
        if (event.target.className !== "show" && event.target.className !== "pred_btn")
            display_pred.style.display='none';
    });
}