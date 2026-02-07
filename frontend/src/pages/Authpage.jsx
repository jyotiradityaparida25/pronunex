import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useUI } from '../context/UIContext';
import { Spinner } from '../components/Loader';
import './AuthPage.css';

const AuthPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { login, signup } = useAuth();
    const { toast } = useUI();

    // False = Login is Front, True = Signup is Front
    const [isSignUp, setIsSignUp] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setIsSignUp(location.pathname === '/signup');
    }, [location.pathname]);

    const handleToggle = (status) => {
        setIsSignUp(status);
        window.history.pushState(null, '', status ? '/signup' : '/login');
    };

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await login(e.target.email.value, e.target.password.value);
            toast.success("Welcome back!");
            navigate('/');
        } catch (error) { toast.error("Login failed."); } finally { setLoading(false); }
    };

    const handleSignupSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        const data = {
            username: e.target.username.value,
            full_name: e.target.full_name.value,
            email: e.target.email.value,
            password: e.target.password.value
        };
        try {
            await signup(data);
            toast.success("Account created!");
            navigate('/');
        } catch (error) { toast.error("Registration failed."); } finally { setLoading(false); }
    };

    return (
        <div className="auth-wrapper-fullscreen">
            <div className="auth-stack-container">
                
                {/* --- CARD 1: LOGIN FORM --- */}
                {/* If !isSignUp (Login Mode), this card is 'active'. If Signup Mode, it's 'inactive' */}
                <div 
                    className={`auth-card ${!isSignUp ? 'active' : 'inactive'}`}
                    onClick={() => { if (isSignUp) handleToggle(false); }}
                >
                    <div className="auth-header">
                        <h1>Welcome Back</h1>
                        <p>Sign in to continue to Pronunex</p>
                    </div>

                    <form style={{width: '100%'}} onSubmit={handleLoginSubmit}>
                        <input className="auth-input" type="email" name="email" placeholder="Email Address" required />
                        <input className="auth-input" type="password" name="password" placeholder="Password" required />
                        
                        <a href="/forgot-password" style={{fontSize: '12px', display:'block', textAlign:'right', marginTop:'10px', color: '#10b981', textDecoration: 'none'}}>
                            Forgot Password?
                        </a>

                        <button className="auth-btn" disabled={loading}>
                            {loading ? <Spinner size="sm"/> : "Sign In"}
                        </button>
                    </form>

                    <p className="switch-text">
                        New here? <span className="switch-btn" onClick={(e) => { e.stopPropagation(); handleToggle(true); }}>Create Account</span>
                    </p>
                </div>

                {/* --- CARD 2: SIGNUP FORM --- */}
                {/* If isSignUp (Signup Mode), this card is 'active'. If Login Mode, it's 'inactive' */}
                <div 
                    className={`auth-card ${isSignUp ? 'active' : 'inactive'}`}
                    onClick={() => { if (!isSignUp) handleToggle(true); }}
                >
                    <div className="auth-header">
                        <h1>Create Account</h1>
                        <p>Join us and start your journey</p>
                    </div>

                    <form style={{width: '100%'}} onSubmit={handleSignupSubmit}>
                        <input className="auth-input" type="text" name="username" placeholder="Username" required />
                        <input className="auth-input" type="text" name="full_name" placeholder="Full Name" required />
                        <input className="auth-input" type="email" name="email" placeholder="Email Address" required />
                        <input className="auth-input" type="password" name="password" placeholder="Password" required />
                        
                        <button className="auth-btn" disabled={loading}>
                            {loading ? <Spinner size="sm"/> : "Sign Up"}
                        </button>
                    </form>

                    <p className="switch-text">
                        Already joined? <span className="switch-btn" onClick={(e) => { e.stopPropagation(); handleToggle(false); }}>Sign In</span>
                    </p>
                </div>

            </div>
        </div>
    );
};

export default AuthPage;