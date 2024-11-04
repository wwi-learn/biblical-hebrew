/*
	Also add this to your package.json dependencies:
		"rxjs": "^7.8.1"
*/

//External Helpers
import { ajax } from 'rxjs/ajax';
import { getDeepProperty, setVariables } from '@intenda/opus-ui';

// Helpers
const saveResultInScriptVariables = (extractors, script, scriptProps, requestResponse) => {
	extractors.forEach(({ path, variable: name }) => {
		const value = getDeepProperty(requestResponse, path);

		if (value === undefined)
			return;

		setVariables({
			variables: {
				[name]: value
			}
		}, script, scriptProps);
	});
};

const saveResultInState = (action, script, scriptProps, data) => {
	console.log(data)
	const { getWgtState, setWgtState } = scriptProps;
	const { saveToStateKey, saveToStateSubKey, target } = action;
	console.log(saveToStateKey, saveToStateSubKey, target)

	if (data && data[0] && data[0].error)
		return null;

	if (!saveToStateKey) {
		Object.entries(data).forEach(([key, value]) => {
			setWgtState(target, { [key]: value });
		  });
	}
	if (!saveToStateSubKey)
		setWgtState(target, { [saveToStateKey]: data });
	else {
		const currentPropData = getWgtState(target)[saveToStateKey];
		const newKeyPropData = {
			...currentPropData,
			[saveToStateSubKey]: data
		};
		setWgtState(target, { [saveToStateKey]: newKeyPropData });
	}
};

const getRandomWord = (verbs) => {
	console.log('getRandomWord...');
	console.log(verbs);
	console.log('...');
	const data = verbs;
	// const data = [
	// 	{'word': 'build', 'wordPattern': 'PAAL'},
	// 	{'word': 'pray', 'wordPattern': 'PIEL'},
	// 	{'word': 'run', 'wordPattern': 'NIFAL'},
	// 	{'word': 'create', 'wordPattern': 'HIFIL'},
	// 	{'word': 'write', 'wordPattern': 'HITPAEL'}
	// ];
	const randomIndex = Math.floor(Math.random() * data.length);
	return data[randomIndex];
};

/* eslint-disable-next-line max-lines-per-function */
const getPealimData = async (action, script, scriptProps) => {
	try {
		const { extractRandomWord } = action;
		const { verbs } = action;
		const { extractAny, extractResults } = action;

		let response = null;
		if (extractRandomWord)
			response = getRandomWord(verbs);
		if (extractAny)
			saveResultInScriptVariables(extractAny, script, scriptProps, response);
		if (extractResults)
			saveResultInScriptVariables(extractResults, script, scriptProps, response);
		if (!extractAny && !extractResults)
			saveResultInState(action, script, scriptProps, response);
	} catch (e) {
		const { extractAny, extractErrors } = action;

		if (extractAny)
			saveResultInScriptVariables(extractAny, script, scriptProps, e);
		if (extractErrors)
			saveResultInScriptVariables(extractErrors, script, scriptProps, e);

		return null;
	}
};

export default getPealimData;
