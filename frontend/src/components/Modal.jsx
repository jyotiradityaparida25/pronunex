/**
 * Modal Component
 * Accessible modal with Esc to close and focus trap
 */

import { useEffect, useRef, useCallback } from 'react';
import { X } from 'lucide-react';
import { useKeyboard } from '../hooks/useKeyboard';
import './Modal.css';

export function Modal({
    isOpen,
    onClose,
    title,
    children,
    size = 'md',
    showCloseButton = true,
    closeOnOverlayClick = true,
    closeOnEsc = true,
}) {
    const modalRef = useRef(null);
    const previousActiveElement = useRef(null);

    // Handle Esc key
    useKeyboard(
        closeOnEsc
            ? {
                Escape: () => onClose(),
            }
            : {},
        [closeOnEsc, onClose]
    );

    // Focus trap and restore
    useEffect(() => {
        if (isOpen) {
            // Store current focus
            previousActiveElement.current = document.activeElement;

            // Focus modal
            if (modalRef.current) {
                modalRef.current.focus();
            }

            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        } else {
            // Restore scroll
            document.body.style.overflow = '';

            // Restore focus
            if (previousActiveElement.current) {
                previousActiveElement.current.focus();
            }
        }

        return () => {
            document.body.style.overflow = '';
        };
    }, [isOpen]);

    const handleOverlayClick = useCallback(
        (event) => {
            if (closeOnOverlayClick && event.target === event.currentTarget) {
                onClose();
            }
        },
        [closeOnOverlayClick, onClose]
    );

    if (!isOpen) {
        return null;
    }

    return (
        <div
            className="modal-overlay"
            onClick={handleOverlayClick}
            role="dialog"
            aria-modal="true"
            aria-labelledby={title ? 'modal-title' : undefined}
        >
            <div
                ref={modalRef}
                className={`modal modal--${size}`}
                tabIndex={-1}
            >
                {(title || showCloseButton) && (
                    <div className="modal__header">
                        {title && (
                            <h2 id="modal-title" className="modal__title">
                                {title}
                            </h2>
                        )}
                        {showCloseButton && (
                            <button
                                type="button"
                                className="modal__close"
                                onClick={onClose}
                                aria-label="Close modal"
                            >
                                <X size={20} />
                            </button>
                        )}
                    </div>
                )}
                <div className="modal__content">{children}</div>
            </div>
        </div>
    );
}

/**
 * Modal with footer actions
 */
export function ModalWithFooter({
    isOpen,
    onClose,
    title,
    children,
    actions,
    ...props
}) {
    return (
        <Modal isOpen={isOpen} onClose={onClose} title={title} {...props}>
            <div className="modal__body">{children}</div>
            {actions && <div className="modal__footer">{actions}</div>}
        </Modal>
    );
}

export default Modal;
