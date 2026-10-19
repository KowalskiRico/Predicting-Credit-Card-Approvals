(function() {

	'use strict';

	var $form = document.getElementById('predictor-form'),
		$submit = $form.querySelector('input[type="submit"]'),
		$message = document.getElementById('result');

	var fields = ['car_owner', 'property_owner', 'income', 'education'];

	function show(type, text) {
		$message.className = 'message ' + type + ' visible';
		$message.textContent = text;
	}

	function hide() {
		$message.className = 'message';
	}

	$form.addEventListener('submit', function(e) {
		e.preventDefault();
		hide();
		$submit.disabled = true;

		var formData = {};
		fields.forEach(function(id) {
			formData[id] = document.getElementById(id).value;
		});

		fetch('/predict', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(formData)
		})
		.then(function(response) { return response.json(); })
		.then(function(data) {
			if (data.status === 'success') {
				show(data.prediction === 'Approved' ? 'success' : 'failure',
					'Prediction: ' + data.prediction);
			} else {
				show('failure', 'Error: ' + data.message);
			}
		})
		.catch(function() {
			show('failure', 'Could not reach the server. Please try again.');
		})
		.then(function() {
			$submit.disabled = false;
		});
	});

})();
