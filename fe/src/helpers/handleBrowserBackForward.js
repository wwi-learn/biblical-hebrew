import { stateManager, getScopedId } from '@intenda/opus-ui';

import { findEntry as findEntryInHistory } from './historyStack';

const handleBrowserBack = () => {
	const entry = findEntryInHistory(window.history.state.index);

	if (entry.title)
		document.title = entry.title;

	stateManager.setWgtState('systemViewport', {
		value: entry.url
	});

	const idRouter = getScopedId('||router||');

	stateManager.setWgtState(idRouter, {
		onRoute: true
	});
};

export default handleBrowserBack;
