var FFX36 = window.FFX36 || {};

FFX36.Common = (function() {
	function _init() {
		if (_is_upgradable()) {
			$('#shade').fadeIn('fast', function() {
				$('#modal').slideDown('fast');
			});

			$('a.dismiss').click(function(e) {
				e.preventDefault();

				$('#modal').slideUp('fast');
				$('#shade').fadeOut('fast');
			});
		}
	}

	function _is_upgradable() {
		// check Mac PPC
		if (/(PPC|Mac OS X 10.[0-4])/.test(navigator.userAgent)) {
			return false;
		}

		// check unsupported locales

		// upgradable if no conditions match
		return true;
	}

	return {
		init: function() {
			_init();
		}
	};
})();

$(document).ready(function() {
	FFX36.Common.init();
});