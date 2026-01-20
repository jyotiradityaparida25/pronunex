/**
 * ErrorBoundary Component
 * Catches React errors and displays fallback UI
 */

import { Component } from 'react';
import { ErrorState } from './ErrorState';

export class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // Log error to console in development
        console.error('ErrorBoundary caught an error:', error, errorInfo);

        // Could send to error reporting service here
        if (this.props.onError) {
            this.props.onError(error, errorInfo);
        }
    }

    handleRetry = () => {
        this.setState({ hasError: false, error: null });
    };

    render() {
        if (this.state.hasError) {
            // Custom fallback UI
            if (this.props.fallback) {
                return this.props.fallback;
            }

            return (
                <div className="error-boundary">
                    <ErrorState
                        icon="generic"
                        title="Something went wrong"
                        message="An unexpected error occurred. Please try refreshing the page."
                        onRetry={this.handleRetry}
                    />
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
