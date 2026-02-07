import React, { useState, useEffect, useRef } from 'react';
import { Eye, EyeOff, ArrowLeft } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useUI } from '../context/UIContext';
import { useSettings } from '../context/SettingsContext'; // IMPORT SETTINGS
import { Spinner } from '../components/Loader';
import './LoginMascot.css'; 

const SignupMascot = () => {
  const navigate = useNavigate();
  
  // Safe context access
  const auth = useAuth();
  const signup = auth ? auth.signup : null;
  
  const ui = useUI();
  const toast = ui ? ui.toast : { success: console.log, error: console.error };

  // GET GLOBAL SETTINGS
  const { settings } = useSettings();
  const currentTheme = settings?.mascotTheme || 'theme-green';

  const [formData, setFormData] = useState({
    username: '', full_name: '', email: '', password: '', password_confirm: ''
  });
  const [loading, setLoading] = useState(false);

  // Eye Tracking Logic
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const leftEyeRef = useRef(null);
  const rightEyeRef = useRef(null);

  useEffect(() => {
    const handleMouseMove = (e) => { setMousePosition({ x: e.clientX, y: e.clientY }); };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const calculateEyeRotation = (eyeRef) => {
    if (!eyeRef.current) return 0;
    const { left, top, width, height } = eyeRef.current.getBoundingClientRect();
    const radian = Math.atan2(mousePosition.x - (left + width / 2), mousePosition.y - (top + height / 2));
    return (radian * (180 / Math.PI) * -1) + 0;
  };

  const handleChange = (e) => { setFormData({ ...formData, [e.target.name]: e.target.value }); };

  const handleSignup = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.password_confirm) { 
        toast.error("Passwords do not match"); 
        return; 
    }
    
    if (!signup) {
        toast.error("Signup function missing. Check AuthContext.");
        return;
    }

    setLoading(true);
    try {
      await signup(formData);
      toast.success("Account created successfully!");
      navigate('/');
    } catch (error) { 
        toast.error(error.message || "Registration failed."); 
    } finally { 
        setLoading(false); 
    }
  };

  const handleGoogleSignup = () => {
    toast.info("Redirecting to Google...");
  };

  return (
    <div className="mascot-login-wrapper">
      {/* Apply Global Theme Class Here */}
      <div className={`mascot-login-container ${currentTheme}`}>
        
        {/* --- LEFT SIDE: MASCOT --- */}
        <div className="mascot-panel">
          <div className="mascot-body">
            <div className="mascot-eyes">
              <div className="eye-socket">
                <div ref={leftEyeRef} className="eye-pupil" style={{ transform: `rotate(${calculateEyeRotation(leftEyeRef)}deg) translateY(10px)` }}>
                    <div className="eye-shine"></div>
                </div>
              </div>
              <div className="eye-socket">
                <div ref={rightEyeRef} className="eye-pupil" style={{ transform: `rotate(${calculateEyeRotation(rightEyeRef)}deg) translateY(10px)` }}>
                    <div className="eye-shine"></div>
                </div>
              </div>
            </div>
            {/* Mouth Animation */}
            <div className={`w-10 h-5 bg-black opacity-30 rounded-b-full transition-all duration-300 
                ${formData.password.length > 0 ? 'scale-y-150 rounded-full w-6 h-6' : 
                  formData.username.length > 0 ? 'scale-x-125 rounded-b-full h-4' : ''}`}>
            </div>
          </div>
          <div className="mascot-shadow"></div>
          <h1 className="mascot-title">Join Us!</h1>
          <p className="mascot-subtitle">Start your journey today</p>
        </div>

        {/* --- RIGHT SIDE: FORM --- */}
        <div className="form-panel">
           <div className="back-button-wrapper">
              <Link to="/" className="back-btn-styled"><ArrowLeft size={18} /> Back to Home</Link>
           </div>

          <div style={{maxWidth: '400px', margin: '0 auto', width: '100%'}}>
              <h2 className="text-3xl font-bold text-[#1e293b] mb-2">Create Account</h2>
              <p className="text-[#64748b] mb-4">Enter your details to create account</p>

              <form onSubmit={handleSignup} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1">
                        <label className="text-xs font-bold text-[#334155]">Username</label>
                        <input type="text" name="username" value={formData.username} onChange={handleChange} className="w-full px-4 py-3 rounded-xl border-2 border-[#e2e8f0] bg-[#f8fafc] text-[#0f172a] outline-none transition-all font-medium input-theme" required />
                    </div>
                    <div className="space-y-1">
                        <label className="text-xs font-bold text-[#334155]">Full Name</label>
                        <input type="text" name="full_name" value={formData.full_name} onChange={handleChange} className="w-full px-4 py-3 rounded-xl border-2 border-[#e2e8f0] bg-[#f8fafc] text-[#0f172a] outline-none transition-all font-medium input-theme" required />
                    </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-[#334155]">Email</label>
                  <input type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-4 py-3 rounded-xl border-2 border-[#e2e8f0] bg-[#f8fafc] text-[#0f172a] outline-none transition-all font-medium input-theme" required />
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1">
                        <label className="text-xs font-bold text-[#334155]">Password</label>
                        <input type="password" name="password" value={formData.password} onChange={handleChange} className="w-full px-4 py-3 rounded-xl border-2 border-[#e2e8f0] bg-[#f8fafc] text-[#0f172a] outline-none transition-all font-medium input-theme" required />
                    </div>
                     <div className="space-y-1">
                        <label className="text-xs font-bold text-[#334155]">Confirm</label>
                        <input type="password" name="password_confirm" value={formData.password_confirm} onChange={handleChange} className="w-full px-4 py-3 rounded-xl border-2 border-[#e2e8f0] bg-[#f8fafc] text-[#0f172a] outline-none transition-all font-medium input-theme" required />
                    </div>
                </div>

                <button type="submit" disabled={loading} className="w-full py-3 text-white text-lg font-bold rounded-xl shadow-lg transform active:scale-[0.98] transition-all duration-200 mt-2 flex justify-center items-center gap-2 btn-theme">
                  {loading ? <Spinner size="sm" color="white" /> : "Sign Up"}
                </button>
              </form>

              {/* DIVIDER & GOOGLE BUTTON */}
              <div className="divider">OR</div>

              <button type="button" onClick={handleGoogleSignup} className="google-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" style={{ minWidth: '20px' }}>
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                </svg>
                Sign up with Google
              </button>

              <p className="text-center text-[#64748b] font-medium mt-6">
                Already have an account? <Link to="/login" className="text-theme font-bold hover:underline">Log In</Link>
              </p>

               {/* Removed Theme Switcher (Now handled in Settings) */}
          </div>
        </div>

      </div>
    </div>
  );
};

export default SignupMascot;