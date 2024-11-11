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
	const { getWgtState, setWgtState } = scriptProps;
	const { saveToStateKey, saveToStateSubKey, target } = action;

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

const getRandomWord = (verbs, filter3ms) => {
	console.log("filter3ms: ", filter3ms);
	const patterns = ["pa'al", "pi'el", "nif'al", "hif'il", "hitpa'el"];
	const pattern = patterns[Math.floor(Math.random() * patterns.length)];
	const pattern_verbs = verbs['pattern_index_list'][pattern];
	const ix = pattern_verbs[Math.floor(Math.random() * pattern_verbs.length)];
	const active_forms = verbs['verbs'][ix]['active_forms'];

	const persons_list = [
		'singular_1st_person',
		'singular_2nd_person_male',
		'singular_2nd_person_female',
		'singular_3rd_person_male',
		'singular_3rd_person_female',
		'plural_1st_person',
		'plural_2nd_person_male',
		'plural_2nd_person_female',
		'plural_3rd_person_male',
		'plural_3rd_person_female'
	];
	const active_forms_list = [
		'past_tense',
		'future_tense'
	]
	const ix_person = persons_list[Math.floor(Math.random() * persons_list.length)];
	const ix_active_form = active_forms_list[Math.floor(Math.random() * active_forms_list.length)];

	if (filter3ms) return {
		'word': active_forms['past_tense']['singular_3rd_person_male']['menakud'],
		'wordPattern': pattern
	};
	return {
		'word': active_forms[ix_active_form][ix_person]['menakud'],
		'wordPattern': pattern
	};
};

/* eslint-disable-next-line max-lines-per-function */
const getPealimData = async (action, script, scriptProps) => {
	try {
		const { extractRandomWord } = action;
		const { verbs, filter3ms } = action;
		const { extractAny, extractResults } = action;

		let response = null;
		if (extractRandomWord)
			response = getRandomWord(verbs, filter3ms);
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
