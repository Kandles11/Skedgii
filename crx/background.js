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
            const oldSchedules = obj["schedules"];
            console.log(JSON.stringify(oldSchedules));

            let conn = new XMLHttpRequest();
            conn.open("POST", API_ENDPOINT, false);
            conn.setRequestHeader("Content-Type", "application/json");
            conn.onreadystatechange = function() {
                if (conn.readyState == 4) {
                    if (conn.status == 200) {
                        let newSchedules = JSON.parse(conn.responseText);
                        newSchedules = newSchedules["results"];
                        newSchedules.sort((a, b) => JSON.stringify(a["combination"]).localeCompare(JSON.stringify(b["combination"])));
                        console.log("response", newSchedules);

                        obj["schedules"] = newSchedules;

                        filter.write(encoder.encode(JSON.stringify(obj)));
                        filter.close();
                    } else {
                        console.log("unable to contact server!");
                        filter.write(encoder.encode(JSON.stringify(obj)));
                        filter.close();
                    }
                }
            }
            conn.send(JSON.stringify(oldSchedules));
        }

        console.log("Hello background", details);
        // console.log("Cookies", await browser.cookies.getAll({ domain: "collegescheduler.com" }));
    }

    return {};
}, networkFilters, ["blocking"]);
