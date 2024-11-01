//Opus
import { loadApp, registerComponentTypes, registerExternalAction  } from '@intenda/opus-ui';//Opus

//Script Actions
import convertMarkdownToComponents from './scriptActions/convertMarkdownToComponents';
import getDocSectionInView from './scriptActions/getDocSectionInView';
import depthFirstSearch from './scriptActions/depthFirstSearch';
import queryUrl2 from './scriptActions/queryUrl2';
import routeFromUrl from './scriptActions/routeFromUrl';
import route from './scriptActions/route';

//Helpers
import handleBrowserBackForward from './helpers/handleBrowserBackForward';

//Custom Components
import Label from './components/label';
import propsLabel from './components/label/props';
import Clicker from './components/clicker';
import propsClicker from './components/clicker/props';

//Styles
import './main.css';

//Setup
window.addEventListener('popstate', handleBrowserBackForward);

//Custom Component Registration
registerComponentTypes([{
	type: 'label',
	component: Label,
	propSpec: propsLabel
}, {
	type: 'clicker',
	component: Clicker,
	propSpec: propsClicker
}]);

const externalActions = {
	convertMarkdownToComponents,
	getDocSectionInView,
	depthFirstSearch,
	queryUrl2,
	routeFromUrl,
	route
};

//Pure Opus UI Application
(async() => {
	const res = await fetch('/app.json')
	const mdaPackage = await res.json();

	Object.entries(externalActions).forEach(([k, v]) => {
		registerExternalAction({
			type: k,
			handler: v
		});
	});

	loadApp({
		mdaPackage,
		loadUrlParameters: true,
		config: {
			env: 'production'
		}
	});
})();
