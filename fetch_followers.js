function fetch_followers(uid, page) {
    if(localStorage.getItem("followers") == null) {
        localStorage.setItem("followers", JSON.stringify([]));
    }

    fetch("https://api2.sololearn.com/v2/userinfo/v3/profile/"+uid+"/followers?count=100&page="+page, {
    "headers": {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.8",
        "authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJ7XCJJbnN0YW5jZUlkXCI6NDM4MDIwMTgsXCJVc2VySWRcIjozMjAwMTQ5MyxcIk5pY2tuYW1lXCI6XCJCcmVudHNwaW5lXCIsXCJEZXZpY2VJZFwiOjg5MjE1ODU3LFwiQ2xpZW50SWRcIjoxMTQzLFwiTG9jYWxlSWRcIjoxLFwiQXBwVmVyc2lvblwiOlwiMC4wLjAuMFwiLFwiSXNQcm9cIjpmYWxzZSxcIkdlbmVyYXRpb25cIjpcIjA1YmM4OGNmLTVhNDItNGVlOC1iOTA0LTI1OWRmOGZhOWY1Y1wifSIsImp0aSI6ImM0MzVjOTJmLTY0YzItNDNkMi04NTRmLTM1YzAwOTRmYmQxYSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IlVzZXIiLCJuYmYiOjE3MTU0NjU5MDEsImV4cCI6MTcxNTQ2OTUwMSwiaXNzIjoiU29sb0xlYXJuLlNlY3VyaXR5LkJlYXJlciIsImF1ZCI6IlNvbG9MZWFybi5TZWN1cml0eS5CZWFyZXIifQ.fiqXpFk0XcucAZ-ZtWVeg9nOvCumuvcWf4q_fg4RB_04QBnze9bcfVbd5PW7zL-wTT_cuS_jrYdj88GJ0b8sfA",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "sl-locale": "de",
        "sl-time-zone": "+2"
    },
    "referrer": "https://www.sololearn.com/",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": null,
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
    }).then(response => response.json()).then(data => {
        if(data["data"].length == 0 || data["data"] == undefined || data.length == 0) {
            return;
        }
        followers = JSON.parse(localStorage.getItem("followers"));
        data["data"].forEach(user => {
            followers.push(user["userId"]);
        });
        localStorage.setItem("followers", JSON.stringify(followers));
        console.log("Page "+page+" done");
        fetch_followers(uid, page+1);
    }).catch(error => console.error(error));
}

function print_followers() {
    followers = JSON.parse(localStorage.getItem("followers"));
    // Split by space
    followers = followers.join(" ");
    console.log(followers);
}

function reset_followers() {
    localStorage.setItem("followers", JSON.stringify([]));
}

