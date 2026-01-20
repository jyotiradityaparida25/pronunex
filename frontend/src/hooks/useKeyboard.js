/**
 * useKeyboard Hook
 * Global keyboard event handling for accessibility
 */

import { useEffect, useCallback } from 'react';

/**
 * Hook to register global keyboard handlers
 * @param {Object} handlers - Key handlers { key: callback }
 * @param {Array} deps - Dependencies array
 */
export function useKeyboard(handlers, deps = []) {
    const handleKeyDown = useCallback(
        (event) => {
            const key = event.key;
            const handler = handlers[key];

            if (handler) {
                // Check if we're in an input field (allow default behavior)
                const target = event.target;
                const isInput =
                    target.tagName === 'INPUT' ||
                    target.tagName === 'TEXTAREA' ||
                    target.isContentEditable;

                // Only handle Escape globally, other keys depend on context
                if (key === 'Escape' || !isInput) {
                    handler(event);
                }
            }
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [handlers, ...deps]
    );

    useEffect(() => {
        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [handleKeyDown]);
}

/**
 * Common keyboard handler presets
 */
export const KEY_HANDLERS = {
    /**
     * Create Escape handler that closes something
     * @param {Function} onClose - Close callback
     */
    escape: (onClose) => ({
        Escape: (event) => {
            event.preventDefault();
            onClose();
        },
    }),

    /**
     * Create Enter handler for form submission
     * @param {Function} onSubmit - Submit callback
     */
    enter: (onSubmit) => ({
        Enter: (event) => {
            // Only if not in textarea
            if (event.target.tagName !== 'TEXTAREA') {
                event.preventDefault();
                onSubmit();
            }
        },
    }),

    /**
     * Create Space handler for toggle buttons
     * @param {Function} onToggle - Toggle callback
     */
    space: (onToggle) => ({
        ' ': (event) => {
            // Only for buttons
            if (event.target.tagName === 'BUTTON') {
                event.preventDefault();
                onToggle();
            }
        },
    }),
};

export default useKeyboard;
