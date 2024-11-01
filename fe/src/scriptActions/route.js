import { push as pushHistory, getCurrentEntry } from '../helpers/historyStack';

const routeFromUrl = ({ config, routeTo: routeToWithParameters }) => {
	const [routeTo, parameters] = routeToWithParameters.split('?');
	const entry = config[routeTo] ?? config.default;

	let nextUrl = entry.path;
	if (parameters?.length > 0)
		nextUrl += `?${parameters}`;

	if (getCurrentEntry().url === nextUrl)
		return;

	const nextTitle = entry.title;

	const newStateIndex = pushHistory(entry);
	window.history.pushState({ index: newStateIndex }, null, nextUrl);

	if (nextTitle)
		document.title = nextTitle;

	return entry.url;
};

export default routeFromUrl;
