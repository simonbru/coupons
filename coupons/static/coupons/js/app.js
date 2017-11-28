var docCookies;

$(function() {
    $('.comment-form').each(function(index, form) {
        displayCommentForm(form)
        $(form).on('change', '[name=does_coupon_work]', function() {
            displayCommentForm(form)
        })
    })

    $('.geoloc-refresh-btn').each(function(index, btn) {
        var $btn = $(btn)
        $btn.on('click', function(e) {
            e.preventDefault()

            $btn.prop('disabled', true)
            retrieveAndStoreGeoloc()
                .then(function() {
                    return refreshSelectWidget('.restaurant-picker select')
                })
                .then(function() { $btn.css('color', 'rgb(0, 158, 0)') })
                .catch(function(err) {
                    if (err.name !== "PositionError") {
                        console.log(err)
                        return
                    }
                    switch(err.code) {
                        case err.POSITION_UNAVAILABLE:
                            alert("Erreur. Avez-vous activé la localisation sur votre appareil ?")
                            break
                        case err.PERMISSION_DENIED:
                            alert("Erreur: vous devez autoriser la localisation pour ce site.")
                            break
                    }
                })
                .always(function() { $btn.prop('disabled', false) })
        })
    })

    // If permissions is already granted, transparently update geolocation.
    // Does not work on Safari 11 (iOS and desktop) or MS Edge.
    if ('permissions' in navigator) {
        navigator.permissions.query({name: 'geolocation'})
            .then(function(status) {
                if (status.state === "granted") {
                    retrieveAndStoreGeoloc()
                }
            })
    }
})

function refreshSelectWidget(selector) {
    return $.get(location.href).then(function(response) {
        // Retrieve container element from response
        var content = $('<div>').html(response).find(selector)
        // Replace content of old container
        $(selector).empty().append(content.children())
        // Hack to ensure the right option is selected
        $(selector).get(0).selectedIndex = 1
        //$(selector).find('[selected]').prop('selected', true)
    })
}

function displayCommentForm(form) {
    var $form = $(form)
    if ($form.find('[name=does_coupon_work]:checked').length > 0) {
        $form.find('.comment-form-details').collapse('show')
    }
}

function retrieveAndStoreGeoloc() {
    var deferred = $.Deferred()
    if (!('geolocation' in navigator)) {
        deferred.reject("Geolocation API not available")
    } else {
        navigator.geolocation.getCurrentPosition(function(position) {
            console.log(position.coords)
            var coords = {
                lat: position.coords.latitude,
                lon: position.coords.longitude
            }
            docCookies.setItem(
                "coords", JSON.stringify(coords), Infinity, "/",
                /*domain*/ null,
                /*secure*/ true
            )
            deferred.resolve(coords)
        }, function(positionErr) {
            positionErr.name = "PositionError"
            deferred.reject(positionErr)
        })
    }
    return deferred.promise()
}


// https://github.com/madmurphy/cookies.js
/*\
|*|
|*|  :: cookies.js ::
|*|
|*|  A complete cookies reader/writer framework with full unicode support.
|*|
|*|  Revision #3 - July 13th, 2017
|*|
|*|  https://developer.mozilla.org/en-US/docs/Web/API/document.cookie
|*|  https://developer.mozilla.org/User:fusionchess
|*|  https://github.com/madmurphy/cookies.js
|*|
|*|  This framework is released under the GNU Public License, version 3 or later.
|*|  http://www.gnu.org/licenses/gpl-3.0-standalone.html
|*|
|*|  Syntaxes:
|*|
|*|  * docCookies.setItem(name, value[, end[, path[, domain[, secure]]]])
|*|  * docCookies.getItem(name)
|*|  * docCookies.removeItem(name[, path[, domain]])
|*|  * docCookies.hasItem(name)
|*|  * docCookies.keys()
|*|
\*/

var docCookies = {
    getItem: function (sKey) {
        if (!sKey) { return null; }
        return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
    },
    setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
        if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) { return false; }
        var sExpires = "";
        if (vEnd) {
            switch (vEnd.constructor) {
                case Number:
                    sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
                    /*
                    Note: Despite officially defined in RFC 6265, the use of `max-age` is not compatible with any
                    version of Internet Explorer, Edge and some mobile browsers. Therefore passing a number to
                    the end parameter might not work as expected. A possible solution might be to convert the the
                    relative time to an absolute time. For instance, replacing the previous line with:
                    */
                    /*
                    sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; expires=" + (new Date(vEnd * 1e3 + Date.now())).toUTCString();
                    */
                    break;
                case String:
                    sExpires = "; expires=" + vEnd;
                    break;
                case Date:
                    sExpires = "; expires=" + vEnd.toUTCString();
                    break;
            }
        }
        document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
        return true;
    },
    removeItem: function (sKey, sPath, sDomain) {
        if (!this.hasItem(sKey)) { return false; }
        document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "");
        return true;
    },
    hasItem: function (sKey) {
        if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) { return false; }
        return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
    },
    keys: function () {
        var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
        for (var nLen = aKeys.length, nIdx = 0; nIdx < nLen; nIdx++) { aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]); }
        return aKeys;
    }
};