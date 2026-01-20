/**
 * Admin Profile Page
 * Extended admin dashboard with system stats and management links
 */

import { useState, useEffect } from 'react';
import {
    Shield, Users, Activity, Settings, ExternalLink,
    TrendingUp, Calendar, BarChart2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Card, StatCard } from '../components/Card';
import { Spinner } from '../components/Loader';
import Profile from './Profile';
import './AdminProfile.css';

export function AdminProfile() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);

    // Redirect non-admin users
    useEffect(() => {
        if (user && !user.is_staff) {
            navigate('/profile');
        }
    }, [user, navigate]);

    // Mock admin stats (in production, fetch from admin API)
    useEffect(() => {
        // Simulated admin stats
        setStats({
            total_users: 156,
            active_today: 42,
            total_sessions: 1247,
            avg_score: 0.73,
        });
    }, []);

    if (!user || !user.is_staff) {
        return (
            <div className="admin-loading">
                <Spinner size="lg" />
                <p>Checking admin access...</p>
            </div>
        );
    }

    return (
        <div className="admin-profile">
            {/* Admin Banner */}
            <div className="admin-banner">
                <div className="admin-banner__content">
                    <Shield size={28} />
                    <div className="admin-banner__text">
                        <h2>Administrator Dashboard</h2>
                        <p>Manage users and monitor system activity</p>
                    </div>
                </div>
                <a
                    href="/admin/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn--secondary admin-banner__link"
                >
                    <Settings size={18} />
                    <span>Django Admin</span>
                    <ExternalLink size={14} />
                </a>
            </div>

            {/* Admin Stats */}
            {stats && (
                <section className="admin-stats">
                    <h3 className="admin-section-title">System Overview</h3>
                    <div className="admin-stats__grid">
                        <StatCard
                            label="Total Users"
                            value={stats.total_users}
                            icon={Users}
                        />
                        <StatCard
                            label="Active Today"
                            value={stats.active_today}
                            icon={Activity}
                        />
                        <StatCard
                            label="Total Sessions"
                            value={stats.total_sessions}
                            icon={Calendar}
                        />
                        <StatCard
                            label="Avg Score"
                            value={`${Math.round(stats.avg_score * 100)}%`}
                            icon={TrendingUp}
                        />
                    </div>
                </section>
            )}

            {/* Quick Actions */}
            <section className="admin-actions">
                <h3 className="admin-section-title">Quick Actions</h3>
                <div className="admin-actions__grid">
                    <Card hover className="admin-action-card">
                        <a
                            href="/admin/accounts/user/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="admin-action-card__link"
                        >
                            <div className="admin-action-card__icon">
                                <Users size={24} />
                            </div>
                            <div className="admin-action-card__content">
                                <h4>Manage Users</h4>
                                <p>View, edit, or delete user accounts</p>
                            </div>
                            <ExternalLink size={16} className="admin-action-card__arrow" />
                        </a>
                    </Card>
                    <Card hover className="admin-action-card">
                        <a
                            href="/admin/library/referencesentence/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="admin-action-card__link"
                        >
                            <div className="admin-action-card__icon">
                                <BarChart2 size={24} />
                            </div>
                            <div className="admin-action-card__content">
                                <h4>Manage Sentences</h4>
                                <p>Add or edit practice sentences</p>
                            </div>
                            <ExternalLink size={16} className="admin-action-card__arrow" />
                        </a>
                    </Card>
                    <Card hover className="admin-action-card">
                        <a
                            href="/admin/library/phoneme/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="admin-action-card__link"
                        >
                            <div className="admin-action-card__icon">
                                <Activity size={24} />
                            </div>
                            <div className="admin-action-card__content">
                                <h4>Manage Phonemes</h4>
                                <p>Update phoneme library data</p>
                            </div>
                            <ExternalLink size={16} className="admin-action-card__arrow" />
                        </a>
                    </Card>
                </div>
            </section>

            {/* User Profile Section */}
            <section className="admin-profile-section">
                <h3 className="admin-section-title">Your Profile</h3>
                <Profile />
            </section>
        </div>
    );
}

export default AdminProfile;
