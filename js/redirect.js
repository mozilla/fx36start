var matches = /Firefox\/(\d+)/.exec(navigator.userAgent);
	
// if using Fx
if (matches !== null && matches.length > 1) {
	var version = parseInt(matches[1], 10);

	// if using a version with about:home (4 or greater), redirect them there
	if(version >= 4) {
		document.location.href = 'about:home';
	}

// if not using Fx, redirect
} else {
	document.location.href = 'https://www.mozilla.org/firefox/desktop/';
}