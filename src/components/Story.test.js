import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Story from './Story';

test('it renders all the components of the story', () => {
    const timestampUTC = '2020-01-01T00:00:00.000Z';
    const story = {
        title: 'hello',
        prompter: {id: 1, username: 'susan', _links: {avatar: 'https://example.com/avatar/susan'}},
        timestamp: timestampUTC,
        body: 'this is a test story'
    };

    render(
        <BrowserRouter>
            <Story story={story} />
        </BrowserRouter>
    );

    const message = screen.getByText('hello');
    const prompterLink = screen.getByText('susan');
    const avatar = screen.getByAltText('susan');
    const timestamp = screen.getByText(/.* ago$/);
    const body = screen.getByText('this is a test story');

    expect(message).toBeInTheDocument();
    expect(prompterLink).toBeInTheDocument();
    expect(prompterLink).toHaveAttribute('href', '/prompter/1');
    expect(avatar).toBeInTheDocument();
    expect(avatar).toHaveAttribute('src', 'https://example.com/avatar/susan&s=48');
    expect(timestamp).toBeInTheDocument();
    expect(timestamp).toHaveAttribute(
        'title', new Date(Date.parse(timestampUTC)).toString());
    expect(body).toBeInTheDocument();
    expect(body).toHaveAttribute('class', 'story-summary');
});