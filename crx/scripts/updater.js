let schedules = [];
function update(obj) {
    schedules = obj["schedules"];
    const schedulesPanel = document.getElementById("schedules_panel");
    if (schedulesPanel != null)
        updateWithHeuristic(schedulesPanel);
}
browser.runtime.onMessage.addListener(update);

function updateWithHeuristic(schedulePanel) {
    console.log("schedule length", schedules.length);

    if (schedulePanel.childNodes[2] !== undefined) {
        for (const node of schedulePanel.childNodes[2].childNodes) {
            if (node.className === rowClass) {
                const scheduleId = parseInt(node.childNodes[1].innerText);
                if (scheduleId <= schedules.length) {
                    if (node.childNodes[node.childNodes.length-1].className !== "skedgii-heuristic") {
                        const heuristicNum = schedules[scheduleId-1]["heuristic"];
                        const heuristic = (Math.round(heuristicNum * 10) / 10).toFixed(1);
                        let color = heuristic > 20 ? (heuristic > 25 ? "green" : "yellow") : "red";
                        const span = document.createElement("span");
                        span.className = "skedgii-heuristic";
                        span.style.color = color == "yellow" ? "black" : "white";
                        span.style.backgroundColor = color;
                        span.style.border = "2px solid " + color;
                        span.style.borderRadius = "10px";
                        span.style.paddingLeft = "5px";
                        span.style.paddingRight = "5px";
                        const strong = document.createElement("strong");
                        strong.appendChild(document.createTextNode(heuristic));
                        span.appendChild(strong);
                        node.appendChild(span);
                        // console.log(scheduleId, heuristic, node);
                    }
                }
            }
        }
    }
}

const rowClass = "css-1k43ht9-rowCss";

let registeredMonitorPanel = false;
new Promise(async (resolve, reject) => {
    while (document.getElementById("schedules_panel") == null) {
        await new Promise(r => setTimeout(r, 500));
    }
    resolve(document.getElementById("schedules_panel"));
}).then((schedulePanel) => {
    if (registeredMonitorPanel) return;
    registeredMonitorPanel = true;

    const cfg = {
        attributes: false,
        childList: true,
        characterData: true
    };

    let monitor = new MutationObserver(function(data) {
        updateWithHeuristic(schedulePanel);
    });
    monitor.observe(schedulePanel, cfg);
    console.log("panel monitor is registered");
});

let registeredMonitorList = false;
new Promise(async (resolve, reject) => {
    while (document.getElementById("schedules_panel") == null) {
        await new Promise(r => setTimeout(r, 500));
    }
    const schedulePanel = document.getElementById("schedules_panel");
    while (schedulePanel.childNodes[2] === undefined) {
        await new Promise(r => setTimeout(r, 500));
    }
    resolve(schedulePanel);
}).then((schedulePanel) => {
    if (registeredMonitorList) return;
    registeredMonitorList = true;

    const cfg = {
        attributes: false,
        childList: true,
        characterData: true
    };

    let monitor = new MutationObserver(function(data) {
        updateWithHeuristic(schedulePanel);
    });
    monitor.observe(schedulePanel.childNodes[2], cfg);
    console.log("list monitor is registered");
});
