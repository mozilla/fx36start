var FFX36 = window.FFX36 || {};

FFX36.Common = (function() {
	function _init() {
		var $sf = $('#sf');
		var $modal, $shade;

		$sf.focus();

		if (_is_upgradable()) {
			$modal = $('#modal');
			$shade = $('#shade');

			$('.upgradable').show();

			$shade.fadeIn('fast', function() {
				$modal.slideDown('fast');
			});

			$('a.dismiss').click(function(e) {
				e.preventDefault();

				_ga_track(['_trackEvent', 'start.mozilla.org Interactions', 'link click', 'No thanks. I\'ll risk it.']);

				$modal.slideUp('fast');
				$shade.fadeOut('fast');

				$sf.focus();
			});
		}

		// track search form submit
		$('#search-form').on('submit', function(e) {
			e.preventDefault();

			var $form = $(this);
			$form.unbind('submit');

			_ga_track(['_trackEvent', 'start.mozilla.org Interactions', 'Submit', 'Google Search'], function() {
				$form.submit();
			});
		});

		// track clicks on modal download CTA
		$('#download-cta').on('click', function(e) {
			e.preventDefault();

			var href = this.href;

			_ga_track(['_trackEvent', 'start.mozilla.org Interactions', 'download button click', 'Firefox for Desktop'], function() {
				window.location = href;
			});
		});
	}

	function _is_upgradable() {
		var matches = /Firefox\/(\d+)/.exec(navigator.userAgent);

		// if using Fx
		if (matches !== null && matches.length > 1) {
			var version = parseInt(matches[1], 10);

			// make sure platform is upgradeable (not on PPC or OS X 10.0 - 10.4)
			if ( (/(PPC|Mac OS X 10.[0-4])/.test(navigator.userAgent) === false) && (version < 29) ) {
				// display appropriate message
				if (version === 3) {
					$('#fx3').show();
				} else if (version === 4) {
					$('#fx4').show();
				} else {
					$('#fxother').show();
				}

				return true;
			}
		// if not using Fx, redirect
		} else {
			document.location.href = 'https://www.mozilla.org/firefox/desktop/';
		}

		// not upgradeable if above conditions fail to match
		return false;
	}

	// swiped from https://github.com/mozilla/bedrock/blob/master/media/js/base/global.js#L135
	function _ga_track(eventArray, callback) {
	    // submit eventArray to GA and call callback only after tracking has
	    // been sent, or if sending fails.
	    //
	    // callback is optional.
	    //
	    // Example usage:
	    //
	    // $(function() {
	    //      var handler = function(e) {
	    //           var _this = this;
	    //           e.preventDefault();
	    //           $(_this).off('submit', handler);
	    //           gaTrack(
	    //              ['_trackEvent', 'Newsletter Registration', 'submit', newsletter],
	    //              function() {$(_this).submit();}
	    //           );
	    //      };
	    //      $(thing).on('submit', handler);
	    // });

	    var hasCallback = typeof(callback) === 'function';

	    if (typeof(window._gaq) === 'object') {
	        // send event to GA
	        window._gaq.push(eventArray);
	        // Only set up timer and hitCallback if a callback exists.
	        if (hasCallback) {
	            // Need a timeout in order for __utm.gif request to complete in
	            // order to register the GA event, before excecuting the callback.
	            setTimeout(callback, 600);
	        }
	    } else {
	        // GA disabled or blocked or something, make sure we still
	        // call the caller's callback:
	        if (hasCallback) {
	            callback();
	        }
	    }
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
