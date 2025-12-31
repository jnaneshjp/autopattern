//this file is to store recorded activity into log

// background.js (service worker)

// ---------- CANONICALIZATION LAYER ----------
function canonicalizeEvent(meta = {}) {
    if (!meta) return { canonical_id: "unknown" };

    const token =
        meta.id ||
        meta.name ||
        meta.role ||
        meta.placeholder ||
        (meta.text ? meta.text.slice(0, 20) : "unknown");

    const stable = String(token)
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "_")
        .replace(/^_|_$/g, "");

    return {
        canonical_id: `${meta.element_type || "element"}:${stable}`,
        selector: meta.css_selector?.replace(/:nth-child\(\d+\)/g, ""), // remove unstable nth-child
        xpath: meta.xpath?.replace(/\[\d+\]/g, ""),                     // remove numeric index
        type: meta.element_type || "generic",
    };
}


// --------- IndexedDB helper ----------
let dbInstance;
function getDB() {
    return new Promise((resolve, reject) => {
        if (dbInstance) return resolve(dbInstance);

        const request = indexedDB.open('TaskMiningDB', 5); // version 4 to force schema update

        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('events')) {
                const store = db.createObjectStore('events', { keyPath: 'id', autoIncrement: true });
                // useful indexes for queries
                store.createIndex('event_ts', 'timestamp', { unique: false });
                store.createIndex('event_type', 'event', { unique: false });
                store.createIndex('url', 'url', { unique: false });
            }
        };

        request.onsuccess = (e) => {
            dbInstance = e.target.result;
            resolve(dbInstance);
        };

        request.onerror = (e) => reject(e);
    });
}

// write + notify
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    (async () => {
        try {
            const db = await getDB();
            const tx = db.transaction('events', 'readwrite');
            const store = tx.objectStore('events');

            // ⭐ ALWAYS attach raw + canonical (even if meta is missing)
            const meta = msg.data || {};
            msg.raw = structuredClone(meta);
            msg.canonical = canonicalizeEvent(meta);

            // ⭐ Fallbacks for missing fields
            if (!msg.canonical.canonical_id) msg.canonical.canonical_id = "generic:unknown";
            if (!msg.canonical.type) msg.canonical.type = msg.event || "generic";

            store.add(msg);

            tx.oncomplete = () => {
                chrome.runtime.sendMessage({ action: 'refresh_dashboard' });
                sendResponse({ status: 'ok' });
            };

            tx.onerror = (err) => sendResponse({ status: 'error', error: err.toString() });
        } catch (err) {
            sendResponse({ status: 'error', error: err.toString() });
        }
    })();
    return true;
});


