browser.runtime.onMessage.addListener(notify);

console.log(document.body.serializeWithStyles());

function notify(message) {
    let filter = browser.webRequest.filterResponseData(details.requestId);
    let decoder = new TextDecoder("utf-8");
    let str = "";
    filter.ondata = (event) => {
        str += decoder.decode(event.data);
    };
    filter.onstop = (event) => {
        let obj = JSON.parse(str);
        console.log("Got message!");
        console.log(obj);
        console.log(document.body.serializeWithStyles());
    }
}