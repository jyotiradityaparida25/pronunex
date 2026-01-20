/**
 * Auth Context
 * User authentication state, login/logout methods, protected route handling
 */

import { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { ENDPOINTS } from '../api/endpoints';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    // Check for existing session on mount
    useEffect(() => {
        const checkAuth = async () => {
            const storedAccess = sessionStorage.getItem('access_token');
            const storedRefresh = sessionStorage.getItem('refresh_token');

            if (storedAccess && storedRefresh) {
                api.setTokens(storedAccess, storedRefresh);

                try {
                    const { data } = await api.get(ENDPOINTS.AUTH.PROFILE);
                    setUser(data);
                    setIsAuthenticated(true);
                } catch {
                    // Token invalid, clear storage
                    sessionStorage.removeItem('access_token');
                    sessionStorage.removeItem('refresh_token');
                    api.clearTokens();
                }
            }

            setIsLoading(false);
        };

        checkAuth();
    }, []);

    // Set up unauthorized callback
    useEffect(() => {
        api.setOnUnauthorized(() => {
            logout();
            navigate('/login');
        });
    }, [navigate]);

    /**
     * Login with email and password
     */
    const login = useCallback(async (email, password) => {
        const { data } = await api.post(ENDPOINTS.AUTH.LOGIN, { email, password });

        // Backend returns { tokens: { access, refresh }, user: {...} }
        const tokens = data.tokens || data;

        // Store tokens in session storage (cleared on browser close)
        sessionStorage.setItem('access_token', tokens.access);
        sessionStorage.setItem('refresh_token', tokens.refresh);

        api.setTokens(tokens.access, tokens.refresh);
        setUser(data.user);
        setIsAuthenticated(true);

        return data;
    }, []);

    /**
     * Register new user
     */
    const signup = useCallback(async (userData) => {
        const { data } = await api.post(ENDPOINTS.AUTH.SIGNUP, userData);

        // Backend returns { tokens: { access, refresh }, user: {...} }
        const tokens = data.tokens;

        // Auto-login after signup if tokens returned
        if (tokens && tokens.access && tokens.refresh) {
            sessionStorage.setItem('access_token', tokens.access);
            sessionStorage.setItem('refresh_token', tokens.refresh);
            api.setTokens(tokens.access, tokens.refresh);
            setUser(data.user);
            setIsAuthenticated(true);
        }

        return data;
    }, []);

    /**
     * Logout user
     */
    const logout = useCallback(async () => {
        try {
            await api.post(ENDPOINTS.AUTH.LOGOUT, {
                refresh: sessionStorage.getItem('refresh_token'),
            });
        } catch {
            // Ignore logout errors
        }

        sessionStorage.removeItem('access_token');
        sessionStorage.removeItem('refresh_token');
        api.clearTokens();
        setUser(null);
        setIsAuthenticated(false);
    }, []);

    /**
     * Update user profile
     */
    const updateProfile = useCallback(async (profileData) => {
        const { data } = await api.put(ENDPOINTS.AUTH.PROFILE, profileData);
        setUser(data);
        return data;
    }, []);

    const value = {
        user,
        isLoading,
        isAuthenticated,
        login,
        signup,
        logout,
        updateProfile,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Hook to access auth context
 */
export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }

    return context;
}

export default AuthContext;
