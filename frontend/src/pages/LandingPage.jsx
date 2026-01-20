/**
 * Pronunex Landing Page
 * High-converting, responsive landing page for the AI Speech Therapy Platform
 * Uses Tailwind CSS with existing teal/green color palette
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
    Mic,
    Brain,
    Target,
    Focus,
    Route,
    BarChart3,
    LayoutDashboard,
    Shield,
    Lock,
    Github,
    Linkedin,
    ArrowRight,
    Play,
    CheckCircle2,
    Zap,
    TrendingUp,
    AudioWaveform,
} from 'lucide-react';
import './LandingPage.css';

/**
 * Hero Section Component
 */
function HeroSection() {
    return (
        <section className="hero-section">
            <div className="hero-bg-pattern" aria-hidden="true">
                <div className="hero-gradient-orb hero-orb-1"></div>
                <div className="hero-gradient-orb hero-orb-2"></div>
                <div className="hero-grid-pattern"></div>
            </div>

            <div className="hero-container">
                <div className="hero-content">
                    <div className="hero-badge">
                        <Zap className="hero-badge-icon" aria-hidden="true" />
                        <span>AI-Powered Speech Therapy</span>
                    </div>

                    <h1 className="hero-headline">
                        Master Your Spoken English with{' '}
                        <span className="hero-headline-accent">AI-Driven Precision</span>
                    </h1>

                    <p className="hero-subheadline">
                        From phoneme-level analysis to adaptive exercises, get a personalized
                        speech therapy experience that evolves with you. Our AI identifies
                        exactly where you struggle and creates a custom learning path.
                    </p>

                    <div className="hero-cta-group">
                        <Link to="/signup" className="hero-cta-primary">
                            <span>Start Your First Assessment</span>
                            <ArrowRight className="hero-cta-icon" aria-hidden="true" />
                        </Link>
                        <Link to="/login" className="hero-cta-secondary">
                            <Play className="hero-cta-icon" aria-hidden="true" />
                            <span>Sign In</span>
                        </Link>
                    </div>

                    <div className="hero-stats">
                        <div className="hero-stat">
                            <span className="hero-stat-value">44+</span>
                            <span className="hero-stat-label">Phonemes Tracked</span>
                        </div>
                        <div className="hero-stat-divider"></div>
                        <div className="hero-stat">
                            <span className="hero-stat-value">Real-time</span>
                            <span className="hero-stat-label">Analysis</span>
                        </div>
                        <div className="hero-stat-divider"></div>
                        <div className="hero-stat">
                            <span className="hero-stat-value">Adaptive</span>
                            <span className="hero-stat-label">Learning Paths</span>
                        </div>
                    </div>
                </div>

                <div className="hero-visual">
                    <div className="hero-mockup">
                        <div className="mockup-header">
                            <div className="mockup-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <span className="mockup-title">Practice Session</span>
                        </div>
                        <div className="mockup-content">
                            <div className="mockup-sentence">
                                <AudioWaveform
                                    className="mockup-wave-icon"
                                    aria-hidden="true"
                                />
                                <p>"The musician played beautiful melodies"</p>
                            </div>
                            <div className="mockup-phonemes">
                                <span className="phoneme-tag phoneme-success">th</span>
                                <span className="phoneme-tag phoneme-success">m</span>
                                <span className="phoneme-tag phoneme-warning">z</span>
                                <span className="phoneme-tag phoneme-success">sh</span>
                                <span className="phoneme-tag phoneme-error">r</span>
                                <span className="phoneme-tag phoneme-success">l</span>
                            </div>
                            <div className="mockup-score">
                                <div className="score-ring">
                                    <svg viewBox="0 0 36 36" className="score-svg">
                                        <path
                                            className="score-bg"
                                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                        />
                                        <path
                                            className="score-fill"
                                            strokeDasharray="85, 100"
                                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                        />
                                    </svg>
                                    <span className="score-value">85%</span>
                                </div>
                                <span className="score-label">Pronunciation Score</span>
                            </div>
                            <button className="mockup-record-btn" aria-label="Record button demo">
                                <Mic aria-hidden="true" />
                            </button>
                        </div>
                    </div>
                    <div className="hero-floating-card card-1">
                        <CheckCircle2 className="floating-icon" aria-hidden="true" />
                        <span>Phoneme Detected</span>
                    </div>
                    <div className="hero-floating-card card-2">
                        <TrendingUp className="floating-icon" aria-hidden="true" />
                        <span>+12% This Week</span>
                    </div>
                </div>
            </div>
        </section>
    );
}

/**
 * How It Works Section Component
 */
function HowItWorksSection() {
    const steps = [
        {
            number: '01',
            icon: Mic,
            title: 'Record',
            description:
                'Read aloud curated sentences. Our system captures your audio with high-fidelity accuracy for precise analysis.',
        },
        {
            number: '02',
            icon: Brain,
            title: 'Analyze',
            description:
                'Our AI uses forced alignment and pronunciation scoring to find exactly where you struggle at the phoneme level.',
        },
        {
            number: '03',
            icon: Target,
            title: 'Adapt',
            description:
                'Receive a personalized roadmap of exercises focusing on your specific problematic phonemes and sounds.',
        },
    ];

    return (
        <section className="how-it-works-section" id="how-it-works">
            <div className="section-container">
                <div className="section-header">
                    <span className="section-label">Simple Process</span>
                    <h2 className="section-title">How It Works</h2>
                    <p className="section-description">
                        Our three-step methodology ensures continuous improvement in your
                        pronunciation skills
                    </p>
                </div>

                <div className="steps-grid">
                    {steps.map((step, index) => (
                        <div key={step.number} className="step-card">
                            <div className="step-number">{step.number}</div>
                            <div className="step-icon-wrapper">
                                <step.icon className="step-icon" aria-hidden="true" />
                            </div>
                            <h3 className="step-title">{step.title}</h3>
                            <p className="step-description">{step.description}</p>
                            {index < steps.length - 1 && (
                                <div className="step-connector" aria-hidden="true"></div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

/**
 * Feature Grid Section Component
 */
function FeatureGridSection() {
    const features = [
        {
            icon: Focus,
            title: 'Phoneme-Level Accuracy',
            description:
                "Don't just get a score; see exactly which sounds (like /th/ or /r/) need work. Our AI pinpoints your specific challenges.",
            gradient: 'feature-gradient-1',
        },
        {
            icon: Route,
            title: 'Adaptive Learning Paths',
            description:
                'The platform generates exercises based on your unique "Focus Areas." Each session adapts to your progress.',
            gradient: 'feature-gradient-2',
        },
        {
            icon: BarChart3,
            title: 'Fluency & Prosody Tracking',
            description:
                'Measure your rhythm, pace, and intonation against native-level models. Track improvements over time.',
            gradient: 'feature-gradient-3',
        },
        {
            icon: LayoutDashboard,
            title: 'Interactive Dashboards',
            description:
                'Visualize your journey from "Beginner" to "Pro" with data-driven charts showing every milestone.',
            gradient: 'feature-gradient-4',
        },
    ];

    return (
        <section className="features-section" id="features">
            <div className="section-container">
                <div className="section-header">
                    <span className="section-label">Key Features</span>
                    <h2 className="section-title">Everything You Need to Improve</h2>
                    <p className="section-description">
                        Comprehensive tools designed to accelerate your pronunciation mastery
                    </p>
                </div>

                <div className="features-grid">
                    {features.map((feature) => (
                        <article key={feature.title} className="feature-card">
                            <div className={`feature-icon-wrapper ${feature.gradient}`}>
                                <feature.icon className="feature-icon" aria-hidden="true" />
                            </div>
                            <h3 className="feature-title">{feature.title}</h3>
                            <p className="feature-description">{feature.description}</p>
                            <div className="feature-card-glow" aria-hidden="true"></div>
                        </article>
                    ))}
                </div>
            </div>
        </section>
    );
}

/**
 * Data in Action Section Component
 */
function DataInActionSection() {
    const weeklyData = [
        { day: 'Mon', score: 65 },
        { day: 'Tue', score: 68 },
        { day: 'Wed', score: 72 },
        { day: 'Thu', score: 70 },
        { day: 'Fri', score: 78 },
        { day: 'Sat', score: 82 },
        { day: 'Sun', score: 85 },
    ];

    const focusPhonemes = [
        { phoneme: '/r/', score: 45, label: 'Needs Practice' },
        { phoneme: '/th/', score: 72, label: 'Improving' },
        { phoneme: '/l/', score: 88, label: 'Strong' },
        { phoneme: '/z/', score: 55, label: 'Focus Area' },
    ];

    return (
        <section className="data-section" id="dashboard">
            <div className="section-container">
                <div className="section-header section-header-light">
                    <span className="section-label section-label-light">Analytics</span>
                    <h2 className="section-title section-title-light">Data in Action</h2>
                    <p className="section-description section-description-light">
                        Detailed metrics at your fingertips. Track every attempt and celebrate
                        every milestone.
                    </p>
                </div>

                <div className="dashboard-mockup">
                    <div className="dashboard-card">
                        <h3 className="dashboard-card-title">Weekly Progress</h3>
                        <div className="chart-container">
                            <div className="line-chart">
                                {weeklyData.map((data, index) => (
                                    <div key={data.day} className="chart-bar-group">
                                        <div
                                            className="chart-bar"
                                            style={{ height: `${data.score}%` }}
                                            aria-label={`${data.day}: ${data.score}%`}
                                        >
                                            <span className="chart-tooltip">{data.score}%</span>
                                        </div>
                                        <span className="chart-label">{data.day}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="dashboard-card">
                        <h3 className="dashboard-card-title">Focus Phonemes</h3>
                        <div className="phoneme-list">
                            {focusPhonemes.map((item) => (
                                <div key={item.phoneme} className="phoneme-item">
                                    <div className="phoneme-info">
                                        <span className="phoneme-symbol">{item.phoneme}</span>
                                        <span className="phoneme-label">{item.label}</span>
                                    </div>
                                    <div className="phoneme-progress-wrapper">
                                        <div className="phoneme-progress-bar">
                                            <div
                                                className="phoneme-progress-fill"
                                                style={{ width: `${item.score}%` }}
                                                aria-label={`${item.score}% proficiency`}
                                            ></div>
                                        </div>
                                        <span className="phoneme-score">{item.score}%</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

/**
 * Technical Trust Section Component
 */
function TechnicalTrustSection() {
    const trustItems = [
        {
            icon: Brain,
            title: 'Wav2Vec2 Technology',
            description:
                'Powered by state-of-the-art speech recognition models for accurate phoneme detection and forced alignment.',
        },
        {
            icon: Shield,
            title: 'Privacy First',
            description:
                'Your voice data is processed securely and used only for your improvement. We never share your recordings.',
        },
        {
            icon: Lock,
            title: 'Secure Platform',
            description:
                'Enterprise-grade security with encrypted data transmission and secure authentication protocols.',
        },
    ];

    return (
        <section className="trust-section" id="technology">
            <div className="section-container">
                <div className="section-header">
                    <span className="section-label">Technology</span>
                    <h2 className="section-title">Built on Solid Foundations</h2>
                    <p className="section-description">
                        Cutting-edge AI technology combined with robust security measures
                    </p>
                </div>

                <div className="trust-grid">
                    {trustItems.map((item) => (
                        <div key={item.title} className="trust-card">
                            <div className="trust-icon-wrapper">
                                <item.icon className="trust-icon" aria-hidden="true" />
                            </div>
                            <h3 className="trust-title">{item.title}</h3>
                            <p className="trust-description">{item.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}

/**
 * Call to Action Section
 */
function CTASection() {
    return (
        <section className="cta-section">
            <div className="cta-container">
                <div className="cta-content">
                    <h2 className="cta-title">Ready to Improve Your Pronunciation?</h2>
                    <p className="cta-description">
                        Join thousands of learners who are mastering English pronunciation with
                        AI-powered precision.
                    </p>
                    <Link to="/signup" className="cta-button">
                        <span>Get Started Free</span>
                        <ArrowRight className="cta-button-icon" aria-hidden="true" />
                    </Link>
                </div>
                <div className="cta-bg-pattern" aria-hidden="true"></div>
            </div>
        </section>
    );
}

/**
 * Footer Component
 */
function Footer() {
    const navLinks = [
        { name: 'Dashboard', href: '/' },
        { name: 'Practice', href: '/practice' },
        { name: 'Progress', href: '/progress' },
        { name: 'Phonemes', href: '/phonemes' },
    ];

    return (
        <footer className="landing-footer">
            <div className="footer-container">
                <div className="footer-brand">
                    <div className="footer-logo">
                        <img src="/icon.png" alt="Pronunex Logo" className="footer-logo-img" />
                        <span className="footer-logo-text">Pronunex</span>
                    </div>
                    <p className="footer-tagline">
                        AI-Powered Speech Therapy for English Pronunciation Mastery
                    </p>
                </div>

                <nav className="footer-nav" aria-label="Footer navigation">
                    <h4 className="footer-nav-title">Quick Links</h4>
                    <ul className="footer-nav-list">
                        {navLinks.map((link) => (
                            <li key={link.name}>
                                <Link to={link.href} className="footer-nav-link">
                                    {link.name}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </nav>

                <div className="footer-social">
                    <h4 className="footer-nav-title">Connect</h4>
                    <div className="footer-social-links">
                        <a
                            href="https://github.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="footer-social-link"
                            aria-label="Visit our GitHub"
                        >
                            <Github aria-hidden="true" />
                        </a>
                        <a
                            href="https://linkedin.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="footer-social-link"
                            aria-label="Connect on LinkedIn"
                        >
                            <Linkedin aria-hidden="true" />
                        </a>
                    </div>
                </div>
            </div>

            <div className="footer-bottom">
                <p className="footer-copyright">
                    &copy; {new Date().getFullYear()} Pronunex. All rights reserved.
                </p>
            </div>
        </footer>
    );
}

/**
 * Main Landing Page Component
 */
export default function LandingPage() {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        setIsVisible(true);
    }, []);

    return (
        <div className={`landing-page ${isVisible ? 'visible' : ''}`}>
            <HeroSection />
            <HowItWorksSection />
            <FeatureGridSection />
            <DataInActionSection />
            <TechnicalTrustSection />
            <CTASection />
            <Footer />
        </div>
    );
}
