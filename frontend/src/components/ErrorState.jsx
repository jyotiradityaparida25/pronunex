/**
 * ErrorState Component
 * Error display with retry functionality
 */

import { AlertCircle, WifiOff, ShieldOff, ServerOff, RefreshCw } from 'lucide-react';
import './ErrorState.css';

const ICONS = {
    network: WifiOff,
    server: ServerOff,
    permission: ShieldOff,
    generic: AlertCircle,
};

export function ErrorState({
    title = 'Something went wrong',
    message = 'An unexpected error occurred. Please try again.',
    icon = 'generic',
    onRetry,
    className = '',
}) {
    const IconComponent = ICONS[icon] || ICONS.generic;

    return (
        <div className={`error-state ${className}`} role="alert">
            <div className="error-state__icon">
                <IconComponent size={48} strokeWidth={1.5} />
            </div>
            <h3 className="error-state__title">{title}</h3>
            <p className="error-state__message">{message}</p>
            {onRetry && (
                <button
                    type="button"
                    className="error-state__retry btn btn--primary"
                    onClick={onRetry}
                >
                    <RefreshCw size={18} />
                    <span>Try Again</span>
                </button>
            )}
        </div>
    );
}

/**
 * Network error preset
 */
export function NetworkError({ onRetry }) {
    return (
        <ErrorState
            icon="network"
            title="Connection Failed"
            message="Unable to connect to the server. Please check your internet connection."
            onRetry={onRetry}
        />
    );
}

/**
 * Server error preset
 */
export function ServerError({ onRetry }) {
    return (
        <ErrorState
            icon="server"
            title="Server Error"
            message="Something went wrong on our end. Please try again later."
            onRetry={onRetry}
        />
    );
}

/**
 * Permission error preset
 */
export function PermissionError({ message }) {
    return (
        <ErrorState
            icon="permission"
            title="Access Denied"
            message={message || 'You do not have permission to access this resource.'}
        />
    );
}

export default ErrorState;
