/**
 * UI Context
 * Global UI state: loading, toasts, modals, errors
 */

import { createContext, useContext, useState, useCallback } from 'react';

const UIContext = createContext(null);

// Toast types
export const TOAST_TYPES = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info',
};

let toastIdCounter = 0;

export function UIProvider({ children }) {
    // Global loading state
    const [isLoading, setIsLoading] = useState(false);
    const [loadingMessage, setLoadingMessage] = useState('');

    // Toast notifications
    const [toasts, setToasts] = useState([]);

    // Modal state
    const [activeModal, setActiveModal] = useState(null);
    const [modalData, setModalData] = useState(null);

    // Global error state
    const [globalError, setGlobalError] = useState(null);

    /**
     * Show loading overlay
     */
    const showLoading = useCallback((message = 'Loading...') => {
        setLoadingMessage(message);
        setIsLoading(true);
    }, []);

    /**
     * Hide loading overlay
     */
    const hideLoading = useCallback(() => {
        setIsLoading(false);
        setLoadingMessage('');
    }, []);

    /**
     * Show toast notification
     */
    const showToast = useCallback((message, type = TOAST_TYPES.INFO, duration = 5000) => {
        const id = ++toastIdCounter;

        const toast = {
            id,
            message,
            type,
            duration,
        };

        setToasts((prev) => [...prev, toast]);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                dismissToast(id);
            }, duration);
        }

        return id;
    }, []);

    /**
     * Dismiss specific toast
     */
    const dismissToast = useCallback((id) => {
        setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, []);

    /**
     * Dismiss all toasts
     */
    const dismissAllToasts = useCallback(() => {
        setToasts([]);
    }, []);

    /**
     * Convenience toast methods
     */
    const toast = {
        success: (message, duration) => showToast(message, TOAST_TYPES.SUCCESS, duration),
        error: (message, duration) => showToast(message, TOAST_TYPES.ERROR, duration),
        warning: (message, duration) => showToast(message, TOAST_TYPES.WARNING, duration),
        info: (message, duration) => showToast(message, TOAST_TYPES.INFO, duration),
    };

    /**
     * Open modal
     */
    const openModal = useCallback((modalId, data = null) => {
        setActiveModal(modalId);
        setModalData(data);
    }, []);

    /**
     * Close modal
     */
    const closeModal = useCallback(() => {
        setActiveModal(null);
        setModalData(null);
    }, []);

    /**
     * Set global error
     */
    const showError = useCallback((error) => {
        setGlobalError(error);
    }, []);

    /**
     * Clear global error
     */
    const clearError = useCallback(() => {
        setGlobalError(null);
    }, []);

    const value = {
        // Loading
        isLoading,
        loadingMessage,
        showLoading,
        hideLoading,

        // Toasts
        toasts,
        showToast,
        dismissToast,
        dismissAllToasts,
        toast,

        // Modal
        activeModal,
        modalData,
        openModal,
        closeModal,

        // Global error
        globalError,
        showError,
        clearError,
    };

    return <UIContext.Provider value={value}>{children}</UIContext.Provider>;
}

/**
 * Hook to access UI context
 */
export function useUI() {
    const context = useContext(UIContext);

    if (!context) {
        throw new Error('useUI must be used within a UIProvider');
    }

    return context;
}

export default UIContext;
