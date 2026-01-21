/**
 * Progress Page
 * Analytics charts and phoneme breakdown (lazy loaded)
 */

import { useMemo } from 'react';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, Cell
} from 'recharts';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { ENDPOINTS } from '../api/endpoints';
import { Card } from '../components/Card';
import { Spinner } from '../components/Loader';
import { ErrorState } from '../components/ErrorState';
import { NoProgress } from '../components/EmptyState';
import './Progress.css';

const CHART_COLORS = {
    primary: 'var(--color-primary-500)',
    success: 'var(--color-success-500)',
    warning: 'var(--color-warning-500)',
    error: 'var(--color-error-500)',
};

export function Progress() {
    const { data: history, isLoading: historyLoading, error: historyError, refetch: refetchHistory } =
        useApi(ENDPOINTS.ANALYTICS.HISTORY);
    const { data: phonemes, isLoading: phonemesLoading, error: phonemesError, refetch: refetchPhonemes } =
        useApi(ENDPOINTS.ANALYTICS.PHONEME_STATS);

    const isLoading = historyLoading || phonemesLoading;
    const error = historyError || phonemesError;

    const chartData = useMemo(() => {
        if (!history) return [];
        // Handle both array and paginated response { results: [...] }
        const historyArray = Array.isArray(history) ? history : (history.results || history.data || []);
        if (!Array.isArray(historyArray)) return [];
        return historyArray.map((item) => ({
            date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
            score: Math.round((item.average_score || 0) * 100),
            attempts: item.attempts || 0,
        }));
    }, [history]);

    const phonemeData = useMemo(() => {
        if (!phonemes) return [];
        // Handle both array and paginated response { results: [...] }
        const phonemesArray = Array.isArray(phonemes) ? phonemes : (phonemes.results || phonemes.data || []);
        if (!Array.isArray(phonemesArray)) return [];
        return phonemesArray
            .sort((a, b) => (a.average_score || a.current_score || 0) - (b.average_score || b.current_score || 0))
            .slice(0, 10)
            .map((p) => ({
                name: p.phoneme || p.phoneme_symbol || p.phoneme_arpabet || p.symbol,
                score: Math.round((p.average_score || p.current_score || 0) * 100),
                fill: (p.average_score || p.current_score || 0) >= 0.7 ? CHART_COLORS.success :
                    (p.average_score || p.current_score || 0) >= 0.5 ? CHART_COLORS.warning : CHART_COLORS.error,
            }));
    }, [phonemes]);

    const trend = useMemo(() => {
        if (!chartData || chartData.length < 2) return null;
        const recent = chartData.slice(-7);
        if (recent.length < 2) return null;

        const first = recent[0].score;
        const last = recent[recent.length - 1].score;
        const diff = last - first;

        return {
            direction: diff > 0 ? 'up' : diff < 0 ? 'down' : 'neutral',
            value: Math.abs(diff),
        };
    }, [chartData]);

    if (isLoading) {
        return (
            <div className="progress-loading">
                <Spinner size="lg" />
                <p>Loading your progress...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="progress-error">
                <ErrorState
                    icon="server"
                    title="Failed to load progress"
                    message="We could not load your progress data. Please try again."
                    onRetry={() => {
                        refetchHistory();
                        refetchPhonemes();
                    }}
                />
            </div>
        );
    }

    if (!chartData || chartData.length === 0) {
        return (
            <div className="progress-empty">
                <NoProgress onStart={() => { }} />
            </div>
        );
    }

    return (
        <div className="progress">
            <header className="progress__header">
                <h1 className="progress__title">Your Progress</h1>
                {trend && (
                    <div className={`progress__trend progress__trend--${trend.direction}`}>
                        {trend.direction === 'up' && <TrendingUp size={20} />}
                        {trend.direction === 'down' && <TrendingDown size={20} />}
                        {trend.direction === 'neutral' && <Minus size={20} />}
                        <span>
                            {trend.direction === 'up' && `+${trend.value}% this week`}
                            {trend.direction === 'down' && `-${trend.value}% this week`}
                            {trend.direction === 'neutral' && 'No change this week'}
                        </span>
                    </div>
                )}
            </header>

            <div className="progress__charts">
                {/* Score History Chart */}
                <Card variant="elevated" padding="lg" className="progress__chart-card">
                    <h2 className="progress__chart-title">Score History</h2>
                    <div className="progress__chart">
                        <ResponsiveContainer width="100%" height={300}>
                            <AreaChart data={chartData}>
                                <defs>
                                    <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#14b8a6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-primary)" />
                                <XAxis
                                    dataKey="date"
                                    stroke="var(--text-tertiary)"
                                    fontSize={12}
                                    tickLine={false}
                                />
                                <YAxis
                                    stroke="var(--text-tertiary)"
                                    fontSize={12}
                                    tickLine={false}
                                    domain={[0, 100]}
                                    tickFormatter={(value) => `${value}%`}
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'var(--surface-primary)',
                                        border: '1px solid var(--border-primary)',
                                        borderRadius: 'var(--radius-lg)',
                                    }}
                                    formatter={(value) => [`${value}%`, 'Score']}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="score"
                                    stroke="#14b8a6"
                                    strokeWidth={2}
                                    fill="url(#scoreGradient)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </Card>

                {/* Phoneme Breakdown */}
                <Card variant="elevated" padding="lg" className="progress__chart-card">
                    <h2 className="progress__chart-title">Phoneme Performance</h2>
                    <p className="progress__chart-subtitle">Your lowest scoring phonemes</p>
                    <div className="progress__chart">
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={phonemeData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-primary)" horizontal={false} />
                                <XAxis
                                    type="number"
                                    stroke="var(--text-tertiary)"
                                    fontSize={12}
                                    domain={[0, 100]}
                                    tickFormatter={(value) => `${value}%`}
                                />
                                <YAxis
                                    type="category"
                                    dataKey="name"
                                    stroke="var(--text-tertiary)"
                                    fontSize={12}
                                    width={50}
                                    tickLine={false}
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'var(--surface-primary)',
                                        border: '1px solid var(--border-primary)',
                                        borderRadius: 'var(--radius-lg)',
                                    }}
                                    formatter={(value) => [`${value}%`, 'Score']}
                                />
                                <Bar dataKey="score" radius={[0, 4, 4, 0]}>
                                    {phonemeData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.fill} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </Card>
            </div>
        </div>
    );
}

export default Progress;
