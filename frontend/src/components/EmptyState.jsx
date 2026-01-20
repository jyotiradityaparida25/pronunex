/**
 * EmptyState Component
 * No data placeholder with optional action
 */

import { Inbox, Search, FileText, Mic, BarChart2 } from 'lucide-react';
import './EmptyState.css';

const ICONS = {
    inbox: Inbox,
    search: Search,
    file: FileText,
    mic: Mic,
    chart: BarChart2,
};

export function EmptyState({
    title = 'No data found',
    message = 'There is nothing to display here yet.',
    icon = 'inbox',
    action,
    className = '',
}) {
    const IconComponent = ICONS[icon] || ICONS.inbox;

    return (
        <div className={`empty-state ${className}`}>
            <div className="empty-state__icon">
                <IconComponent size={48} strokeWidth={1.5} />
            </div>
            <h3 className="empty-state__title">{title}</h3>
            <p className="empty-state__message">{message}</p>
            {action && (
                <button
                    type="button"
                    className="empty-state__action btn btn--primary"
                    onClick={action.onClick}
                >
                    {action.icon && action.icon}
                    <span>{action.label}</span>
                </button>
            )}
        </div>
    );
}

/**
 * No sessions preset
 */
export function NoSessions({ onStart }) {
    return (
        <EmptyState
            icon="mic"
            title="No Practice Sessions"
            message="Start your first practice session to begin improving your pronunciation."
            action={{
                label: 'Start Practice',
                onClick: onStart,
            }}
        />
    );
}

/**
 * No results preset
 */
export function NoResults({ query }) {
    return (
        <EmptyState
            icon="search"
            title="No Results Found"
            message={`No results found for "${query}". Try a different search term.`}
        />
    );
}

/**
 * No progress preset
 */
export function NoProgress({ onStart }) {
    return (
        <EmptyState
            icon="chart"
            title="No Progress Yet"
            message="Complete practice sessions to see your progress here."
            action={{
                label: 'Start Practicing',
                onClick: onStart,
            }}
        />
    );
}

export default EmptyState;
