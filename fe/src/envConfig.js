const appMode = import.meta.env.VITE_APP_MODE;

window.envConfig = {
	themeEntry_mdaLocation: {
		theme: 'system',
		key: 'mdaLocation',
		value: window.location.origin
	},
	themeEntry_appMode: {
		theme: 'system',
		key: 'appMode',
		value: appMode
	}
};
