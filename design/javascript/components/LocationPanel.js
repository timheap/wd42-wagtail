function mutex() {
	let isHeld = false;

	return function wrap(fn) {
		return function wrapped() {
			if (isHeld) return;
			try {
				isHeld = true;
				fn.apply(this, arguments);
			} finally {
				isHeld = false;
			}
		};
	};
}

export default class LocationPanel {
	constructor(mapEl, latEl, lngEl, options) {
		this.mapEl = mapEl;
		this.latEl = latEl;
		this.lngEl = lngEl;
		this.updateMutex = mutex();

		this.options = options;

		const initialPosition = this.extractSelectedPosition();

		this.makeMap(initialPosition);
		this.bind();
	}

	extractSelectedPosition() {
		if (!this.latEl.value || !this.lngEl.value) return null;

		const position = new google.maps.LatLng(
			parseFloat(this.latEl.value),
			parseFloat(this.lngEl.value));

		if (isNaN(position.lat()) || isNaN(position.lng())) return null;

		return position;
	}

	makeMap(initialPosition) {
		const opts = {};
		if (initialPosition) {
			opts['center'] = initialPosition;
			opts['zoom'] = this.options.selectedZoom;
		} else {
			opts['center'] = new google.maps.LatLng(...this.options.initialCenter);
			opts['zoom'] = this.options.initialZoom;
		}

		Object.assign(opts, this.options.mapOptions);
		this.map = new google.maps.Map(this.mapEl, opts);
		google.maps.event.addListener(
			this.map, 'click', this.updateMutex((event) => {
				this.updateMarker(event.latLng);
				this.updateFields(event.latLng);
			}),
		);

		if (initialPosition) {
			this.updateMarker(initialPosition);
		}
	}

	bind() {
		const update = this.updateMutex(() => {
			const position = this.extractSelectedPosition();
			if (position) {
				this.updateMarker(position);
				this.map.panTo(position);
			}
		});

		for (let el of [this.latEl, this.lngEl]) {
			el.addEventListener('change', update);
			el.addEventListener('keyup', update);
		}
	}

	updateMarker(position) {
		if (this.marker) {
			this.marker.setPosition(position);
		} else {
			this.marker = new google.maps.Marker({
				draggable: true,
				map: this.map,
				position: position,
			});
			const update = this.updateMutex((event) => {
				this.updateFields(event.latLng);
			});
			google.maps.event.addListener(this.marker, 'dragend', update);
			google.maps.event.addListener(this.marker, 'drag', update);
		}
	}

	updateFields(position) {
		this.latEl.value = position.lat().toFixed(this.options.decimalPlaces);
		this.lngEl.value = position.lng().toFixed(this.options.decimalPlaces);
	}
}
