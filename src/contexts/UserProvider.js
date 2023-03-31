import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useApi } from './ApiProvider';
import { useFlash } from '../contexts/FlashProvider';

const UserContext = createContext();

export default function UserProvider({ children }) {
    const [user, setUser] = useState();
    const api = useApi();
    const flash = useFlash();

    useEffect(() => {
        (async () => {
            if (api.isAuthenticated()) {
                const currentUser = localStorage.getItem('currentUser');
                const response = await api.get('/prompters/' + currentUser);
                setUser(response.ok ? response.body : null);
            } else {
                setUser(null);
            }
        })();
    }, [api]);

    const login = useCallback(async (username, password) => {
        const result = await api.login(username, password);
        if (result === 'ok') {
            const currentUser = localStorage.getItem('currentUser');
            const response = await api.get('/prompters/' + currentUser);
            setUser(response.ok ? response.body : null);
        }
        return result;
    }, [api]);

    const logout = useCallback(async () => {
        await api.logout();
        flash('You have successfully logged out!', 'success');
        setUser(null);
    }, [api, flash]);

    return (
        <UserContext.Provider value={{ user, setUser, login, logout }}>
            {children}
        </UserContext.Provider>
    );
}

export function useUser() {
    return useContext(UserContext);
}