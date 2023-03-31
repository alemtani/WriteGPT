import { render, screen } from '@testing-library/react';
import { useEffect } from 'react';
import FlashProvider from './FlashProvider';
import { useFlash } from './FlashProvider';
import FlashMessage from '../components/FlashMessage';
import { act } from 'react-dom/test-utils';

beforeEach(() => {
    jest.useFakeTimers();
});

afterEach(() => {
    jest.useRealTimers()
});

test('flashes a message', async () => {
    const Test = () => {
        const flash = useFlash();
        useEffect(() => {
            flash('foo', 'danger');
        }, []);
        return null;
    };

    render(
        <FlashProvider>
            <FlashMessage />
            <Test />
        </FlashProvider>
    );

    const alert = screen.getByRole('alert');

    expect(alert).toHaveTextContent('foo');
    expect(alert).toHaveClass('alert-danger');
    expect(alert).toHaveAttribute('data-visible', 'true');

    act(() => jest.runAllTimers());
    expect(alert).toHaveAttribute('data-visible', 'false');
});