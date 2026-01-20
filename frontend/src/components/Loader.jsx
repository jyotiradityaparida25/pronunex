/**
 * Loader Component
 * Variants: spinner, skeleton, overlay
 */

import './Loader.css';

/**
 * Spinner loader
 */
export function Spinner({ size = 'md', className = '' }) {
    return (
        <div className={`loader-spinner loader-spinner--${size} ${className}`} role="status">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle
                    className="loader-spinner__track"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="3"
                />
                <circle
                    className="loader-spinner__indicator"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                />
            </svg>
            <span className="sr-only">Loading...</span>
        </div>
    );
}

/**
 * Classic CSS-based spinner (simpler, border-based)
 * Uses primary color with transparent top border for spinning effect
 */
export function ClassicSpinner({ size = 'md', className = '' }) {
    return (
        <div
            className={`classic-spinner classic-spinner--${size} ${className}`}
            role="status"
        >
            <span className="sr-only">Loading...</span>
        </div>
    );
}

/**
 * Skeleton loader for content placeholders
 */
export function Skeleton({ width, height, variant = 'text', className = '' }) {
    const style = {
        width: width || '100%',
        height: height || (variant === 'text' ? '1em' : undefined),
    };

    const variantClass = `skeleton--${variant}`;

    return (
        <div
            className={`skeleton ${variantClass} ${className}`}
            style={style}
            aria-hidden="true"
        />
    );
}

/**
 * Full-screen loading overlay
 */
export function LoadingOverlay({ message = 'Loading...' }) {
    return (
        <div className="loading-overlay" role="status" aria-live="polite">
            <div className="loading-overlay__content">
                <Spinner size="lg" />
                <p className="loading-overlay__message">{message}</p>
            </div>
        </div>
    );
}

/**
 * Inline loader
 */
export function InlineLoader({ message = 'Loading...' }) {
    return (
        <div className="inline-loader">
            <Spinner size="sm" />
            <span>{message}</span>
        </div>
    );
}

export default Spinner;
