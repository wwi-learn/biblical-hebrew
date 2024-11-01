import { init as initHistoryStack } from '../helpers/historyStack';

const routeFromUrl = ({ config }) => {
	const [, ...pathArray] = window.location.pathname.split('/');
	const path = pathArray.join('/');

	const useEntry = Object.values(config).find(v => v.path === `/${path}`) ?? config.default;

	if (useEntry.title)
		document.title = useEntry.title;

	initHistoryStack(useEntry);

	return useEntry.url;
};

export default routeFromUrl;
