import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import { useState, useEffect } from 'react';
import FlashProvider from './FlashProvider';
import ApiProvider from './ApiProvider';
import UserProvider from './UserProvider';
import { useUser } from './UserProvider';

const realFetch = global.fetch;

beforeEach(() => {
    global.fetch = jest.fn();
});

afterEach(() => {
    global.fetch = realFetch;
    localStorage.clear();
});

test('logs user in', async () => {
    const urls = [];
  
    global.fetch
    .mockImplementationOnce(url => {
        urls.push(url);
        return {
            status: 200,
            ok: true,
            json: () => Promise.resolve({token: '123', currentUser: 1}),
        };
    })
    .mockImplementationOnce(url => {
        urls.push(url);
        return {
            status: 200,
            ok: true,
            json: () => Promise.resolve({username: 'username'}),
        };
    });
  
    const Test = () => {
        const { login, user } = useUser();
        useEffect(() => {
            (async () => await login('username', 'password'))();
        }, []);
        return user ? <p>{user.username}</p> : null;
    };
  
    render(
        <FlashProvider>
            <ApiProvider>
                <UserProvider>
                    <Test />
                </UserProvider>
            </ApiProvider>
        </FlashProvider>
    );

    const element = await screen.findByText('username');
    expect(element).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(2);
    expect(urls).toHaveLength(2);
    expect(urls[0]).toMatch(/^\/api\/tokens$/);
    expect(urls[1]).toMatch(/^\/api\/prompters\/1$/);
});

test('logs user in with bad credentials', async () => {
    const urls = [];
  
    global.fetch
      .mockImplementationOnce(url => {
        urls.push(url);
        return {
          status: 401,
          ok: false,
          json: () => Promise.resolve({}),
        };
      });
  
    const Test = () => {
        const [result, setResult] = useState();
        const { login, user } = useUser();
        useEffect(() => {
            (async () => {
                setResult(await login('username', 'password'));
            })();
        }, []);
        return <>{result}</>;
    };
  
    render(
        <FlashProvider>
            <ApiProvider>
                <UserProvider>
                    <Test />
                </UserProvider>
            </ApiProvider>
        </FlashProvider>
    );
  
    const element = await screen.findByText('fail');
    expect(element).toBeInTheDocument();
    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(urls).toHaveLength(1);
    expect(urls[0]).toMatch(/^\/api\/tokens$/);
});

test('logs user out', async () => {
    localStorage.setItem('token', '123');
    localStorage.setItem('currentUser', 1)
  
    global.fetch
    .mockImplementationOnce(url => {
        return {
            status: 200,
            ok: true,
            json: () => Promise.resolve({username: 'susan'}),
        };
    })
    .mockImplementationOnce((url) => {
        return {
            status: 204,
            ok: true,
            json: () => Promise.resolve({}),
        };
    });
  
    const Test = () => {
        const { user, logout } = useUser();
        if (user) {
            return (
                <>
                    <p>{user.username}</p>
                    <button onClick={logout}>logout</button>
                </>
            );
        }
        else if (user === null) {
            return <p>logged out</p>;
        }
        else {
            return null;
        }
    };
  
    render(
        <FlashProvider>
            <ApiProvider>
                <UserProvider>
                    <Test />
                </UserProvider>
            </ApiProvider>
        </FlashProvider>
    );
  
    const element = await screen.findByText('susan');
    const button = await screen.findByRole('button');
    expect(element).toBeInTheDocument();
    expect(button).toBeInTheDocument();
  
    userEvent.click(button);
    const element2 = await screen.findByText('logged out');
    expect(element2).toBeInTheDocument();
    expect(localStorage.getItem('token')).toBeNull();
    expect(localStorage.getItem('currentUser')).toBeNull();
});