import './styles.css'

const Label = ({ id, classNames, style, state: { caption } }) => {
	return (
		<div
			key={id}
			className={classNames}
			style={style}
		>
			{caption}
		</div>
	);
};

export default Label;
