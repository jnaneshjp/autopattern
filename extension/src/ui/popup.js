document.getElementById("open-dashboard").onclick = () => {
    chrome.tabs.create({
        url: "src/ui/dashboard.html"
    });
};
