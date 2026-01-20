/**
 * AudioRecorder Component
 * Recording with permission handling, error states, and waveform visualization
 */

import { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Pause, RotateCcw, Send, AlertCircle } from 'lucide-react';
import { useAudio, AUDIO_STATES, isAudioSupported, isSecureContext } from '../hooks/useAudio';
import { Spinner } from './Loader';
import './AudioRecorder.css';

export function AudioRecorder({
    onRecordingComplete,
    maxDuration = 30,
    disabled = false
}) {
    const {
        state,
        error,
        duration,
        audioBlob,
        audioUrl,
        isSupported,
        isSecure,
        isRecording,
        isProcessing,
        isDenied,
        hasRecording,
        startRecording,
        stopRecording,
        cancelRecording,
        retry,
    } = useAudio({ maxDuration, onRecordingComplete });

    const [isPlaying, setIsPlaying] = useState(false);
    const audioRef = useRef(null);
    const canvasRef = useRef(null);
    const analyserRef = useRef(null);
    const animationRef = useRef(null);

    // Format duration as MM:SS
    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    // Handle audio playback
    const togglePlayback = () => {
        if (!audioRef.current) return;

        if (isPlaying) {
            audioRef.current.pause();
        } else {
            audioRef.current.play();
        }
        setIsPlaying(!isPlaying);
    };

    // Audio ended handler
    useEffect(() => {
        const audio = audioRef.current;
        if (!audio) return;

        const handleEnded = () => setIsPlaying(false);
        audio.addEventListener('ended', handleEnded);

        return () => audio.removeEventListener('ended', handleEnded);
    }, [audioUrl]);

    // Unsupported browser
    if (!isSupported) {
        return (
            <div className="audio-recorder audio-recorder--unsupported">
                <div className="audio-recorder__error">
                    <AlertCircle size={48} />
                    <h3>Browser Not Supported</h3>
                    <p>Your browser does not support audio recording. Please use Chrome, Firefox, or Edge.</p>
                </div>
            </div>
        );
    }

    // HTTPS required warning (only in production)
    if (!isSecure && window.location.hostname !== 'localhost') {
        return (
            <div className="audio-recorder audio-recorder--unsupported">
                <div className="audio-recorder__error">
                    <AlertCircle size={48} />
                    <h3>Secure Connection Required</h3>
                    <p>Microphone access requires a secure connection (HTTPS).</p>
                </div>
            </div>
        );
    }

    // Permission denied state
    if (isDenied) {
        return (
            <div className="audio-recorder audio-recorder--denied">
                <div className="audio-recorder__error">
                    <AlertCircle size={48} />
                    <h3>Microphone Access Denied</h3>
                    <p>Please allow microphone access in your browser settings and try again.</p>
                    <button type="button" className="btn btn--primary" onClick={retry}>
                        <RotateCcw size={18} />
                        <span>Try Again</span>
                    </button>
                </div>
            </div>
        );
    }

    // Error state
    if (state === AUDIO_STATES.ERROR) {
        return (
            <div className="audio-recorder audio-recorder--error">
                <div className="audio-recorder__error">
                    <AlertCircle size={48} />
                    <h3>Recording Error</h3>
                    <p>{error || 'An error occurred while recording. Please try again.'}</p>
                    <button type="button" className="btn btn--primary" onClick={retry}>
                        <RotateCcw size={18} />
                        <span>Try Again</span>
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className={`audio-recorder ${disabled ? 'audio-recorder--disabled' : ''}`}>
            {/* Waveform / Status Display */}
            <div className="audio-recorder__display">
                {isRecording && (
                    <div className="audio-recorder__recording">
                        <div className="audio-recorder__waveform">
                            {[...Array(20)].map((_, i) => (
                                <div
                                    key={i}
                                    className="audio-recorder__bar"
                                    style={{
                                        animationDelay: `${i * 0.05}s`,
                                        height: `${20 + Math.random() * 60}%`,
                                    }}
                                />
                            ))}
                        </div>
                        <div className="audio-recorder__recording-indicator">
                            <span className="audio-recorder__pulse" />
                            <span>Recording</span>
                        </div>
                    </div>
                )}

                {isProcessing && (
                    <div className="audio-recorder__processing">
                        <Spinner size="md" />
                        <span>Processing...</span>
                    </div>
                )}

                {hasRecording && !isRecording && !isProcessing && (
                    <div className="audio-recorder__playback">
                        <audio ref={audioRef} src={audioUrl} />
                        <button
                            type="button"
                            className="audio-recorder__play-btn"
                            onClick={togglePlayback}
                            aria-label={isPlaying ? 'Pause' : 'Play'}
                        >
                            {isPlaying ? <Pause size={24} /> : <Play size={24} />}
                        </button>
                        <div className="audio-recorder__audio-info">
                            <span>Recording complete</span>
                            <span className="audio-recorder__duration">{formatTime(duration)}</span>
                        </div>
                    </div>
                )}

                {!isRecording && !isProcessing && !hasRecording && (
                    <div className="audio-recorder__idle">
                        <Mic size={48} className="audio-recorder__mic-icon" />
                        <p>Click the button below to start recording</p>
                    </div>
                )}
            </div>

            {/* Timer */}
            <div className="audio-recorder__timer">
                <span className="audio-recorder__time">{formatTime(duration)}</span>
                <span className="audio-recorder__max-time">/ {formatTime(maxDuration)}</span>
            </div>

            {/* Progress bar */}
            <div className="audio-recorder__progress">
                <div
                    className="audio-recorder__progress-bar"
                    style={{ width: `${(duration / maxDuration) * 100}%` }}
                />
            </div>

            {/* Controls */}
            <div className="audio-recorder__controls">
                {!isRecording && !hasRecording && (
                    <button
                        type="button"
                        className="audio-recorder__btn audio-recorder__btn--record"
                        onClick={startRecording}
                        disabled={disabled || isProcessing}
                        aria-label="Start recording"
                    >
                        <Mic size={24} />
                        <span>Start Recording</span>
                    </button>
                )}

                {isRecording && (
                    <button
                        type="button"
                        className="audio-recorder__btn audio-recorder__btn--stop"
                        onClick={stopRecording}
                        aria-label="Stop recording"
                    >
                        <Square size={24} />
                        <span>Stop</span>
                    </button>
                )}

                {hasRecording && !isRecording && !isProcessing && (
                    <>
                        <button
                            type="button"
                            className="audio-recorder__btn audio-recorder__btn--retry"
                            onClick={cancelRecording}
                            aria-label="Record again"
                        >
                            <RotateCcw size={20} />
                            <span>Retry</span>
                        </button>
                        <button
                            type="button"
                            className="audio-recorder__btn audio-recorder__btn--submit"
                            onClick={() => onRecordingComplete && onRecordingComplete(audioBlob)}
                            aria-label="Submit recording"
                        >
                            <Send size={20} />
                            <span>Submit</span>
                        </button>
                    </>
                )}
            </div>

            {/* Hint text */}
            <p className="audio-recorder__hint">
                {isRecording
                    ? 'Recording will automatically stop at maximum duration'
                    : hasRecording
                        ? 'Review your recording and submit or try again'
                        : 'Press Space to toggle recording'}
            </p>
        </div>
    );
}

export default AudioRecorder;
