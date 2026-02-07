import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';
// import { useAuth } from '../context/AuthContext'; // Import this if your auth context has a reset function
import { useUI } from '../context/UIContext';
import { Spinner } from '../components/Loader';
import './LoginMascot.css';

const ForgotPasswordMascot = () => {
  // const { resetPassword } = useAuth(); // Enable if available
  const { toast } = useUI();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentTheme, setCurrentTheme] = useState('theme-purple'); // Default to purple for this page?

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

  const handleReset = async (e) => {
    e.preventDefault();
    setLoading(true);
    // Simulate API call or use actual auth function
    setTimeout(() => {
        toast.success("Reset link sent! Check your email.");
        setLoading(false);
    }, 1500);
  };

  return (
    <div className="mascot-login-wrapper">
      <div className={`mascot-login-container ${currentTheme}`}>
        
        {/* --- LEFT SIDE: MASCOT --- */}
        <div className="mascot-panel">
          <div className="mascot-body">
            <div className="mascot-eyes">
              {/* Pupils are slightly smaller to look "confused/worried" */}
              <div className="eye-socket">
                <div ref={leftEyeRef} className="eye-pupil" style={{ width: '15px', height: '15px', transform: `rotate(${calculateEyeRotation(leftEyeRef)}deg) translateY(8px)` }}><div className="eye-shine" style={{width:'5px', height:'5px'}}></div></div>
              </div>
              <div className="eye-socket">
                <div ref={rightEyeRef} className="eye-pupil" style={{ width: '15px', height: '15px', transform: `rotate(${calculateEyeRotation(rightEyeRef)}deg) translateY(8px)` }}><div className="eye-shine" style={{width:'5px', height:'5px'}}></div></div>
              </div>
            </div>
            {/* Mouth is a small "o" for surprise */}
            <div className="w-6 h-6 bg-black opacity-30 rounded-full"></div>
          </div>
          <div className="mascot-shadow"></div>

          <h1 className="mascot-title">Forgot It?</h1>
          <p className="mascot-subtitle">Don't worry, it happens.</p>
        </div>

        {/* --- RIGHT SIDE: FORM --- */}
        <div className="form-panel">
           <div className="back-button-wrapper">
              <Link to="/login" className="back-btn-styled"><ArrowLeft size={18} /> Back to Login</Link>
           </div>

          <div style={{maxWidth: '400px', margin: '0 auto', width: '100%'}}>
              <h2 className="text-3xl font-bold text-[#1e293b] mb-2">Reset Password</h2>
              <p className="text-[#64748b] mb-8">Enter your email and we'll send you a link.</p>

              <form onSubmit={handleReset} className="space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-bold text-[#334155]">Email Address</label>
                  <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full px-5 py-4 rounded-xl border-2 border-[#e2e8f0] bg-[#f8fafc] text-[#0f172a] outline-none transition-all font-medium input-theme" placeholder="name@example.com" required />
                </div>

                <button type="submit" disabled={loading} className="w-full py-4 text-white text-lg font-bold rounded-xl shadow-lg transform active:scale-[0.98] transition-all duration-200 mt-6 flex justify-center items-center gap-2 btn-theme">
                  {loading ? <Spinner size="sm" color="white" /> : "Send Reset Link"}
                </button>
              </form>

              <div className="theme-switcher">
                  <div className={`theme-btn bg-emerald-500 ${currentTheme === 'theme-green' ? 'active' : ''}`} onClick={() => setCurrentTheme('theme-green')}></div>
                  <div className={`theme-btn bg-blue-500 ${currentTheme === 'theme-blue' ? 'active' : ''}`} onClick={() => setCurrentTheme('theme-blue')}></div>
                  <div className={`theme-btn bg-purple-500 ${currentTheme === 'theme-purple' ? 'active' : ''}`} onClick={() => setCurrentTheme('theme-purple')}></div>
               </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ForgotPasswordMascot;