const networkFilters = {
    urls: [
        "*://utdallas.collegescheduler.com/api/*"
    ]
};

const generateUriRegex = /^.*:\/\/utdallas\.collegescheduler\.com\/api\/terms\/[^\/]+\/schedules\/generate$/;

browser.webRequest.onBeforeRequest.addListener((details) => {
    if (details.url.match(generateUriRegex)) {
        let filter = browser.webRequest.filterResponseData(details.requestId);
        let decoder = new TextDecoder("utf-8");
        let encoder = new TextEncoder();

        let str = "";
        filter.ondata = (event) => {
            str += decoder.decode(event.data);
            filter.write(event.data);
        };
        filter.onstop = (event) => {
            let obj = JSON.parse(str);
            console.log(obj["schedules"]);
            filter.disconnect();
        }

        console.log("Hello background", details);
        // console.log("Cookies", await browser.cookies.getAll({ domain: "collegescheduler.com" }));
    }
}, networkFilters, ["blocking"]);
