import { useMemo } from 'react';

import './styles.css'

const onClick = ({ setState, state: { count } }) => {
	setState({ count: count + 1 });
};

const Clicker = ({ id, classNames, style, getHandler, state: { topText, bottomText, count } }) => {
	const handlerOnClick = getHandler(onClick);

	const useBottomText = useMemo(() => bottomText.replaceAll('%1', count), [bottomText, count]);

	return (
		<div
			key={id}
			className={classNames}
			style={style}
			onClick={handlerOnClick}
		>
			<span>{topText}</span>
			<span>{useBottomText}</span>
		</div>
	);
};

export default Clicker;
