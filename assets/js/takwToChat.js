// Cookie helper functions
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Initialize Tawk.to
var Tawk_API = Tawk_API || {}, Tawk_LoadStart = new Date();
(function () {
    var s1 = document.createElement("script"), s0 = document.getElementsByTagName("script")[0];
    s1.async = true;
    s1.src = 'https://embed.tawk.to/677e9d9eaf5bfec1dbe880ec/1ih39fcqb';
    s1.charset = 'UTF-8';
    s1.setAttribute('crossorigin', '*');
    s0.parentNode.insertBefore(s1, s0);
})();

// Save and restore Tawk.to session using cookies
Tawk_API.onLoad = function () {
    // Save session ID in a cookie when Tawk.to loads
    Tawk_API.getSessionId(function (sessionID) {
        setCookie('tawk_session', sessionID, 7); // Save for 7 days
    });
};

Tawk_API.onChatStarted = function () {
    // Restore session from cookie if available
    var storedSession = getCookie('tawk_session');
    if (storedSession) {
        Tawk_API.setAttributes({
            session: storedSession
        }, function (error) {
            if (error) {
                console.error("Error restoring Tawk.to session:", error);
            }
        });
    }
};
