//React
import { createRoot } from 'react-dom/client';

//Opus
import Opus, { registerComponentTypes, Component } from '@intenda/opus-ui';

//Custom Components
import Clicker from './components/clicker';
import propsClicker from './components/clicker/props';

//Styles
import './main.css';

//Custom Component Registration
registerComponentTypes([{
	type: 'clicker',
	component: Clicker,
	propSpec: propsClicker
}]);

//Hybrid Opus UI Application
const Title = () => {
	return (
		<div style={{
			display: 'flex',
			flexDirection: 'column',
			alignItems: 'center',
			gap: '24px'
		}}>
			<span style={{
				fontSize: '32px'
			}}>
				Opus UI Example Application
			</span>
			<Component mda={{
				type: 'clicker',
				prps: {
					topText: 'Click me',
					bottomText: 'You have clicked %1 time(s)',
					color: 'darkBlue'
				}
			}} />
		</div>
	);
};

const root = createRoot(document.getElementById('root'));

root.render(
	<Opus startupComponent={<Title />} />
);