var FFX36 = window.FFX36 || {};

FFX36.Common = (function() {
	function _init() {
		if (_is_upgradable()) {
			$('.upgradable').show();

			_break_button_text();

			$('#shade').fadeIn('fast', function() {
				$('#modal').slideDown('fast');
			});

			$('a.dismiss').click(function(e) {
				e.preventDefault();

				$('#modal').slideUp('fast');
				$('#shade').fadeOut('fast');

				$('#sf').focus();
			});
		}
	}

	function _break_button_text() {
		var text = $('a.download span:first').text();
		var pieces = text.split(' ');

		// if we have a space in the text, insert a <br> close to the middle
		if (pieces.length > 0) {
			var br_pos = Math.floor((pieces.length/2)) - 1;
			var new_html = '';
			for (var i = 0; i < pieces.length; i++) {
				new_html += pieces[i] + ((br_pos === i) ? '<br />' : ' ');
			}

			$('a.download span:first').html(new_html);
		}
	}

	function _is_upgradable() {
		// check Mac PPC & version 3.6
		if ( (/(PPC|Mac OS X 10.[0-4])/.test(navigator.userAgent)) || (/(Firefox\/3.6)/.test(navigator.userAgent) === false) ) {
			return false;
		}

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