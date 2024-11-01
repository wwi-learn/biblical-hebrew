const props = {
	count: {
		type: 'integer',
		desc: 'The amount of times that the user has clicked on the component',
		internal: true,
		dft: 0
	},
	topText: {
		type: 'string',
		desc: 'The top text of the clicker component',
		dft: 'Clicker'
	},
	bottomText: {
		type: 'string',
		desc: 'The bottom text of the clicker component. The string %1 will be replaced by the click count',
		dft: '%1'
	},
	color: {
		type: 'string',
		desc: 'The color of the clicker component text',
		dft: 'black',
		//cssAttr set to true means that this property will be placed into the component's style object
		cssAttr: true,
		//cssAttrVal set to true means that we want to use the property value as is, without any transformations
		cssAttrVal: true
	}
};

export default props;
