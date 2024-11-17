const networkFilters = {
    urls: [
        "*://utdallas.collegescheduler.com/api/*"
    ]
};

const generateUriRegex = /^.*:\/\/utdallas\.collegescheduler\.com\/api\/terms\/[^\/]+\/schedules\/generate$/;

browser.webRequest.onCompleted.addListener(async (details) => {
    if (details.url.match(generateUriRegex)) {
        console.log("Hello background", details);
        console.log("Cookies", await browser.cookies.getAll({ domain: "collegescheduler.com" }));
    } else {
        console.log("unrelated event");
    }
}, networkFilters);
