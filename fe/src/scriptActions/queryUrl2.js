/*
	Also add this to your package.json dependencies:
		"rxjs": "^7.8.1"
*/

//External Helpers
import { ajax } from 'rxjs/ajax';
import { getDeepProperty, setVariables } from '@intenda/opus-ui';

//Helpers
const performRequest = async (
	{
		url,
		method = 'GET',
		headers = { 'Content-Type': 'application/json' },
		body,
		crossDomain,
		withCredentials = false
	}
) => {
	const request = {
		url,
		method,
		headers,
		body
	};

	if (crossDomain !== undefined)
		request.crossDomain = crossDomain;

	if (withCredentials !== undefined)
		request.withCredentials = withCredentials;

	return new Promise((res, reject) => {
		const startTime = (new Date()).getTime();

		ajax(request).subscribe(response => {
			const finishTime = (new Date()).getTime();

			const duration = finishTime - startTime;

			response.duration = duration;

			res(response);
		}, e => reject(e));
	});
};

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

const saveResultInState = (action, script, scriptProps, requestResponse) => {
	const { getWgtState, setWgtState } = scriptProps;
	const { saveToStateKey, saveToStateSubKey, target } = action;

	const data = requestResponse.response.result[0].serviceresult.response;

	if (data && data[0] && data[0].error)
		return null;

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

const buildBody = ({ body, bodyIsFormData }) => {
	if (!bodyIsFormData)
		return body;

	const result = new FormData();

	Object.entries(body).forEach(([k, v]) => {
		if (v[0] && v[0] instanceof Blob) {
			for (let vv of v)
				result.append(k, vv);

			return;
		}

		result.append(k, v);
	});

	return result;
};

/* eslint-disable-next-line max-lines-per-function */
const queryUrl2 = async (action, script, scriptProps) => {
	try {
		const { url, method, headers, crossDomain } = action;
		const { extractAny, extractResults, withCredentials} = action;

		const body = buildBody(action);

		const request = {
			url,
			method,
			headers,
			body
		};

		if (crossDomain !== undefined)
			request.crossDomain = crossDomain;

		if (withCredentials !== undefined)
			request.withCredentials = withCredentials;

		const response = await performRequest(request);

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

export default queryUrl2;
