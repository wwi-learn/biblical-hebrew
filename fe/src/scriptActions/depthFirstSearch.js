const depthFirstSearch = ({ root, findId }) => {
	if (root.id === findId)
		return root;

	if (!root.children)
		return;

	for (let child of root.children) {
		const result = depthFirstSearch({ root: child, findId });
		if (result)
			return result;
	}

	return;
}

export default depthFirstSearch;