const networkFilters = {
    urls: [
        "*://utdallas.collegescheduler.com/api/*"
    ]
};

const generateUriRegex = /^.*:\/\/utdallas\.collegescheduler\.com\/api\/terms\/[^\/]+\/schedules\/generate$/;

const API_ENDPOINT = "http://100.65.237.99:8000/ratings/json-endpoint/";

browser.webRequest.onBeforeRequest.addListener((details) => {
    if (details.url.match(generateUriRegex)) {
        let filter = browser.webRequest.filterResponseData(details.requestId);
        let decoder = new TextDecoder("utf-8");
        let encoder = new TextEncoder();

        let str = "";
        filter.ondata = (event) => {
            str += decoder.decode(event.data);
        };
        filter.onstop = (event) => {
            let obj = JSON.parse(str);
            const toSend = obj["schedules"].map((value) => value["combination"]);
            console.log(JSON.stringify(toSend));

            let conn = new XMLHttpRequest();
            conn.open("POST", API_ENDPOINT, false);
            conn.setRequestHeader("Content-Type", "application/json");
            conn.onreadystatechange = function() {
                if (conn.readyState == 4 && conn.status == 200) {
                    console.log("response", conn.response);

                    filter.write(encoder.encode(str));
                    filter.disconnect();
                }
            }
            conn.send(JSON.stringify(toSend));
        }

        console.log("Hello background", details);
        // console.log("Cookies", await browser.cookies.getAll({ domain: "collegescheduler.com" }));
    }

    return {};
}, networkFilters, ["blocking"]);
