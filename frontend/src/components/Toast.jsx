/**
 * Toast Component
 * Notification display with auto-dismiss
 */

import { useEffect } from 'react';
import { CheckCircle, AlertCircle, AlertTriangle, Info, X } from 'lucide-react';
import { useUI, TOAST_TYPES } from '../context/UIContext';
import './Toast.css';

const ICONS = {
    [TOAST_TYPES.SUCCESS]: CheckCircle,
    [TOAST_TYPES.ERROR]: AlertCircle,
    [TOAST_TYPES.WARNING]: AlertTriangle,
    [TOAST_TYPES.INFO]: Info,
};

function ToastItem({ toast, onDismiss }) {
    const IconComponent = ICONS[toast.type] || ICONS.info;

    return (
        <div
            className={`toast toast--${toast.type}`}
            role="alert"
            aria-live="polite"
        >
            <div className="toast__icon">
                <IconComponent size={20} />
            </div>
            <p className="toast__message">{toast.message}</p>
            <button
                type="button"
                className="toast__dismiss"
                onClick={() => onDismiss(toast.id)}
                aria-label="Dismiss notification"
            >
                <X size={16} />
            </button>
        </div>
    );
}

export function ToastContainer() {
    const { toasts, dismissToast } = useUI();

    if (toasts.length === 0) {
        return null;
    }

    return (
        <div className="toast-container" aria-live="polite">
            {toasts.map((toast) => (
                <ToastItem key={toast.id} toast={toast} onDismiss={dismissToast} />
            ))}
        </div>
    );
}

export default ToastContainer;
