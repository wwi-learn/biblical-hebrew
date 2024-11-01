const getDocSectionInView = async ({ scrollContainerId, headings }) => {
	const elParent = document.getElementById(scrollContainerId);
	const rectParent = elParent.getBoundingClientRect();

	if (elParent.scrollTop === 0)
		return headings[0].id;
	else if (elParent.scrollTop === elParent.scrollHeight - elParent.clientHeight)
		return headings[headings.length - 1].id;

	const infoOnHeadings = headings.map(h => {
		const elHeading = document.getElementById(h.id);

		const { top, height } = elHeading.getBoundingClientRect();

		return {
			id: h.id,
			top: top - height
		};
	});

	infoOnHeadings.reverse();

	const useEntry = infoOnHeadings.find(f => {
		return f.top <= rectParent.top;
	});

	return useEntry.id;
};

export default getDocSectionInView;
