const stack = [];
let index = 0;

export const init = entry => {
	stack.length = 0;
	index = 0;

	stack.push(entry);

	window.history.replaceState({ index: 0 }, null);
};

export const push = entry => {
	index++;

	if (stack.length >= index - 1)
		stack.splice(index, stack.length - index);

	stack.push(entry);

	return index;
}

export const findEntry = findIndex => {
	if (findIndex < index)
		index--;
	else
		index++;

	return stack[index];
};

export const getCurrentEntry = () => stack[index];
