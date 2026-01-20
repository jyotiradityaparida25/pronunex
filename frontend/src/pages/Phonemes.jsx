/**
 * Phonemes Page
 * Browse 44 English phonemes with articulation tips
 */

import { useState } from 'react';
import { Search, Volume2, Info } from 'lucide-react';
import { useApi } from '../hooks/useApi';
import { ENDPOINTS } from '../api/endpoints';
import { Card } from '../components/Card';
import { Spinner } from '../components/Loader';
import { ErrorState } from '../components/ErrorState';
import { Modal } from '../components/Modal';
import './Phonemes.css';

const PHONEME_CATEGORIES = [
    { id: 'all', label: 'All' },
    { id: 'vowel', label: 'Vowels' },
    { id: 'consonant', label: 'Consonants' },
];

export function Phonemes() {
    const { data: phonemes, isLoading, error, refetch } = useApi(ENDPOINTS.PHONEMES.LIST);

    const [searchQuery, setSearchQuery] = useState('');
    const [activeCategory, setActiveCategory] = useState('all');
    const [selectedPhoneme, setSelectedPhoneme] = useState(null);

    // Handle both array and paginated response { results: [...] }
    const phonemesArray = phonemes
        ? (Array.isArray(phonemes) ? phonemes : (phonemes.results || phonemes.data || []))
        : [];

    const filteredPhonemes = phonemesArray.filter((phoneme) => {
        const matchesSearch =
            (phoneme.symbol || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
            (phoneme.ipa || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
            (phoneme.example_word || '').toLowerCase().includes(searchQuery.toLowerCase());

        const matchesCategory =
            activeCategory === 'all' ||
            (phoneme.category || phoneme.type || '').toLowerCase() === activeCategory;

        return matchesSearch && matchesCategory;
    });

    if (isLoading) {
        return (
            <div className="phonemes-loading">
                <Spinner size="lg" />
                <p>Loading phonemes...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="phonemes-error">
                <ErrorState
                    icon="server"
                    title="Failed to load phonemes"
                    message="We could not load the phoneme library. Please try again."
                    onRetry={refetch}
                />
            </div>
        );
    }

    return (
        <div className="phonemes">
            <header className="phonemes__header">
                <div className="phonemes__title-section">
                    <h1 className="phonemes__title">Phoneme Library</h1>
                    <p className="phonemes__subtitle">
                        Explore the 44 sounds of English and learn how to pronounce them
                    </p>
                </div>

                <div className="phonemes__filters">
                    {/* Search */}
                    <div className="phonemes__search">
                        <Search className="phonemes__search-icon" size={18} />
                        <input
                            type="text"
                            placeholder="Search phonemes..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="phonemes__search-input"
                        />
                    </div>

                    {/* Category tabs */}
                    <div className="phonemes__tabs">
                        {PHONEME_CATEGORIES.map((category) => (
                            <button
                                key={category.id}
                                type="button"
                                className={`phonemes__tab ${activeCategory === category.id ? 'phonemes__tab--active' : ''
                                    }`}
                                onClick={() => setActiveCategory(category.id)}
                            >
                                {category.label}
                            </button>
                        ))}
                    </div>
                </div>
            </header>

            <main className="phonemes__grid">
                {filteredPhonemes.map((phoneme) => (
                    <Card
                        key={phoneme.id}
                        hover
                        className="phoneme-card"
                        onClick={() => setSelectedPhoneme(phoneme)}
                    >
                        <div className="phoneme-card__symbol">{phoneme.ipa}</div>
                        <div className="phoneme-card__info">
                            <span className="phoneme-card__arpabet">{phoneme.symbol}</span>
                            {phoneme.example_word && (
                                <span className="phoneme-card__example">
                                    {phoneme.example_word}
                                </span>
                            )}
                        </div>
                        <button
                            type="button"
                            className="phoneme-card__action"
                            onClick={(e) => {
                                e.stopPropagation();
                                setSelectedPhoneme(phoneme);
                            }}
                            aria-label={`Learn more about ${phoneme.symbol}`}
                        >
                            <Info size={16} />
                        </button>
                    </Card>
                ))}
            </main>

            {filteredPhonemes.length === 0 && (
                <div className="phonemes__no-results">
                    <p>No phonemes found matching your search.</p>
                </div>
            )}

            {/* Phoneme Detail Modal */}
            <Modal
                isOpen={!!selectedPhoneme}
                onClose={() => setSelectedPhoneme(null)}
                title={`Phoneme: ${selectedPhoneme?.symbol || ''}`}
                size="md"
            >
                {selectedPhoneme && (
                    <div className="phoneme-detail">
                        <div className="phoneme-detail__header">
                            <div className="phoneme-detail__symbol">{selectedPhoneme.ipa}</div>
                            <div className="phoneme-detail__meta">
                                <span className="phoneme-detail__arpabet">{selectedPhoneme.symbol}</span>
                                <span className="phoneme-detail__category">
                                    {selectedPhoneme.category || selectedPhoneme.type}
                                </span>
                            </div>
                        </div>

                        {selectedPhoneme.example_word && (
                            <div className="phoneme-detail__section">
                                <h3>Example Word</h3>
                                <p className="phoneme-detail__example">
                                    <strong>{selectedPhoneme.example_word}</strong>
                                </p>
                            </div>
                        )}

                        {(selectedPhoneme.articulation_tips || selectedPhoneme.articulation_tip) && (
                            <div className="phoneme-detail__section">
                                <h3>How to Pronounce</h3>
                                <p>{selectedPhoneme.articulation_tips || selectedPhoneme.articulation_tip}</p>
                            </div>
                        )}

                        {selectedPhoneme.common_mistakes && (
                            <div className="phoneme-detail__section">
                                <h3>Common Mistakes</h3>
                                <p>{selectedPhoneme.common_mistakes}</p>
                            </div>
                        )}
                    </div>
                )}
            </Modal>
        </div>
    );
}

export default Phonemes;
