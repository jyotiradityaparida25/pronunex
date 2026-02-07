import React, { useState, useEffect, useRef } from 'react';
import { Eye, EyeOff } from 'lucide-react';

const AnimatedLogin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  
  // State for eye movement
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const leftEyeRef = useRef(null);
  const rightEyeRef = useRef(null);

  // Track mouse movement globally
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Calculate eye rotation
  const calculateEyeRotation = (eyeRef) => {
    if (!eyeRef.current) return 0;
    const { left, top, width, height } = eyeRef.current.getBoundingClientRect();
    const eyeCenterX = left + width / 2;
    const eyeCenterY = top + height / 2;
    
    // Calculate angle between eye center and mouse
    const radian = Math.atan2(mousePosition.x - eyeCenterX, mousePosition.y - eyeCenterY);
    const rotation = (radian * (180 / Math.PI) * -1) + 0;
    return rotation;
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-4xl bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col md:flex-row min-h-[600px]">
        
        {/* --- LEFT SIDE: ANIMATED MASCOT --- */}
        <div className="w-full md:w-1/2 bg-[#ecfdf5] relative flex items-center justify-center p-8 overflow-hidden">
          
          {/* Background Decorative Circles */}
          <div className="absolute top-10 left-10 w-20 h-20 bg-[#10b981] rounded-full opacity-20 blur-xl animate-pulse"></div>
          <div className="absolute bottom-10 right-10 w-32 h-32 bg-[#34d399] rounded-full opacity-20 blur-xl animate-pulse delay-700"></div>

          {/* THE CHARACTER */}
          <div className="relative z-10 w-64 h-64">
            {/* Body */}
            <div className="absolute inset-0 bg-gradient-to-br from-[#10b981] to-[#059669] rounded-[3rem] shadow-xl flex flex-col items-center pt-12 transition-all duration-300 hover:scale-105">
              
              {/* Eyes Container */}
              <div className="flex gap-4 mb-4">
                {/* Left Eye */}
                <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center relative overflow-hidden shadow-inner">
                  <div 
                    ref={leftEyeRef}
                    className="w-6 h-6 bg-[#0f172a] rounded-full absolute"
                    style={{ 
                      transform: `rotate(${calculateEyeRotation(leftEyeRef)}deg) translateY(12px)` 
                    }}
                  >
                     <div className="w-2 h-2 bg-white rounded-full absolute top-1 left-1 opacity-80"></div>
                  </div>
                </div>

                {/* Right Eye */}
                <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center relative overflow-hidden shadow-inner">
                  <div 
                    ref={rightEyeRef}
                    className="w-6 h-6 bg-[#0f172a] rounded-full absolute"
                    style={{ 
                      transform: `rotate(${calculateEyeRotation(rightEyeRef)}deg) translateY(12px)` 
                    }}
                  >
                    <div className="w-2 h-2 bg-white rounded-full absolute top-1 left-1 opacity-80"></div>
                  </div>
                </div>
              </div>

              {/* Mouth (Changes based on input focus!) */}
              <div className={`w-12 h-6 bg-[#022c22] rounded-b-full transition-all duration-300 ${password.length > 0 ? 'scale-y-150 rounded-full w-8 h-8' : ''}`}></div>

              {/* Blush */}
              <div className="absolute top-24 left-4 w-6 h-4 bg-pink-300 rounded-full opacity-40 blur-sm"></div>
              <div className="absolute top-24 right-4 w-6 h-4 bg-pink-300 rounded-full opacity-40 blur-sm"></div>
            </div>
            
            {/* Paws */}
            <div className="absolute -bottom-4 -left-2 w-16 h-12 bg-[#059669] rounded-2xl shadow-lg transform -rotate-12"></div>
            <div className="absolute -bottom-4 -right-2 w-16 h-12 bg-[#059669] rounded-2xl shadow-lg transform rotate-12"></div>
          </div>

          <div className="absolute bottom-8 text-[#059669] font-semibold tracking-wide opacity-80">
            PRONUNEX
          </div>
        </div>

        {/* --- RIGHT SIDE: LOGIN FORM --- */}
        <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center bg-white">
          <div className="mb-8 text-center md:text-left">
            <h2 className="text-3xl font-bold text-[#10b981] mb-2">Welcome Back!</h2>
            <p className="text-slate-400">Please enter your details.</p>
          </div>

          <form className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Email</label>
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-[#10b981] focus:ring-4 focus:ring-[#10b981]/10 outline-none transition-all"
                placeholder="anna@gmail.com"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Password</label>
              <div className="relative">
                <input 
                  type={showPassword ? "text" : "password"} 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-[#10b981] focus:ring-4 focus:ring-[#10b981]/10 outline-none transition-all pr-10"
                  placeholder="••••••••"
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  {showPassword ? <EyeOff size={20}/> : <Eye size={20}/>}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded border-slate-300 text-[#10b981] focus:ring-[#10b981]" />
                <span className="text-slate-600">Remember for 30 days</span>
              </label>
              <a href="#" className="text-[#10b981] font-semibold hover:underline">Forgot password?</a>
            </div>

            <button className="w-full py-3 bg-[#10b981] hover:bg-[#059669] text-white font-bold rounded-xl shadow-lg shadow-[#10b981]/30 active:scale-[0.98] transition-all">
              Log In
            </button>

            <button className="w-full py-3 bg-white border-2 border-slate-100 hover:bg-slate-50 text-slate-700 font-bold rounded-xl flex items-center justify-center gap-2 transition-all">
               Log in with Google
            </button>
          </form>

          <p className="mt-8 text-center text-slate-500 text-sm">
            Don't have an account? <a href="#" className="text-[#10b981] font-bold hover:underline">Sign Up</a>
          </p>
        </div>

      </div>
    </div>
  );
};

export default AnimatedLogin;