tokens_to_refresh = %%tokens_to_refresh%%;
var refreshed_tokens = {};

// Ready event
// What if doc already loaded?
if (document.readyState === "complete" || document.readyState === "interactive") {
    // Document is already loaded
    startRefreshingTokens();
} else {
    // Wait for document to load
    document.addEventListener("DOMContentLoaded", startRefreshingTokens);
}

function startRefreshingTokens() {
    localStorage.setItem("refreshed_tokens", JSON.stringify({}));
    for (var i = 0; i < tokens_to_refresh.length; i++) {
        var refresh_token = tokens_to_refresh[i];
        setTimeout(refresh_it, i*750, refresh_token);
    }
    console.log("Refreshing tokens...");
}

function refresh_it(refresh_token) {
    fetch("https://api2.sololearn.com/v2/authentication/token:refresh", {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        },
        "referrer": "https://www.sololearn.com/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": "\""+refresh_token+"\"",
        "method": "POST",
        "mode": "cors",
        "credentials": "omit"
    }).then(response => response.json()).then(data => {
        refreshed_tokens[refresh_token] = data;
        console.log("Refreshed token: "+refresh_token);
        console.log("Data: "+data);
        localStorage.setItem("refreshed_tokens", JSON.stringify(refreshed_tokens));
    }).catch(error => console.error(error));
}