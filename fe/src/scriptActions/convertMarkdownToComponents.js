const convertMarkdownToComponents = ({ value }) => {
	const split = value
		.replaceAll('\r', '')
		.split('\n');

	const components = [];
	let currentType = '';
	let buffer = '';
	const headings = [];

	const pushToRes = () => {
		if (!buffer.length)
			return;

		buffer = buffer.substr(0, buffer.length - 1);
		if (currentType === 'info')
			buffer = buffer.replaceAll('||', '││');

		components.push({
			type: currentType,
			value: (
				currentType === 'codeJson' ||
				currentType === 'componentLibrarySection'
			) ? JSON.parse(buffer) : buffer
		});

		buffer = '';
	};

	split.forEach(s => {
		const isNewType = s.indexOf('```') === 0;
		if (!isNewType) {
			buffer += s + '\n';

			if (s.indexOf('# ') === 0)
				headings.push(s.substr(2));
		} else {
			pushToRes();

			currentType = s.substr(3);
		}
	});

	pushToRes();

	return {
		components,
		headings: headings.map(h => {
			return {
				heading: h,
				id: h.toLowerCase().replaceAll(' ', '-')
			};
		})
	};
};

export default convertMarkdownToComponents;