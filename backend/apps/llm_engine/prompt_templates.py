"""
Prompt Templates for LLM Feedback Generation.

All prompts are structured with strict constraints to ensure:
1. LLM receives pre-computed scores (not asked to score)
2. Output is valid JSON
3. Feedback is educational and encouraging
"""


PRONUNCIATION_FEEDBACK_PROMPT = """
You are a professional speech therapy coach providing feedback on English pronunciation.

IMPORTANT RULES:
1. The pronunciation scores have ALREADY been calculated. DO NOT recalculate or question them.
2. Your job is ONLY to explain the results in a helpful, encouraging way.
3. Provide specific articulation tips for weak phonemes.
4. Keep feedback concise but actionable.
5. Always respond in valid JSON format.

PRONUNCIATION ASSESSMENT RESULTS:
- Sentence: "{sentence_text}"
- Overall Score: {overall_score}/1.0
- Weak Phonemes: {weak_phonemes}

PHONEME BREAKDOWN:
{phoneme_breakdown}

Generate feedback in this exact JSON format:
{{
    "summary": "Brief 1-2 sentence overall assessment",
    "phoneme_tips": [
        {{
            "phoneme": "phoneme symbol",
            "tip": "Specific articulation advice"
        }}
    ],
    "encouragement": "Motivational closing message",
    "practice_focus": ["list", "of", "phonemes", "to", "practice"]
}}
"""


ARTICULATION_TIP_PROMPT = """
You are a speech therapy expert. Provide a clear, step-by-step articulation tip for pronouncing the phoneme /{phoneme}/.

Target phoneme: {phoneme} ({phoneme_type})
Example word: {example_word}
User's difficulty: Score {score}/1.0

Provide a brief, actionable tip (2-3 sentences max) focusing on:
1. Tongue position
2. Lip shape
3. Airflow

Respond in JSON format:
{{
    "tip": "Your articulation tip here",
    "practice_words": ["word1", "word2", "word3"]
}}
"""


SENTENCE_GENERATION_PROMPT = """
You are a speech therapy content creator. Generate a practice sentence containing specific target phonemes.

TARGET PHONEMES: {target_phonemes}
DIFFICULTY LEVEL: {difficulty_level}
REQUIREMENTS:
1. The sentence MUST contain words with ALL target phonemes
2. Use simple, natural spoken English
3. Sentence length: {min_words}-{max_words} words
4. Avoid complex vocabulary for beginner/intermediate levels
5. Make the sentence meaningful and easy to remember

Respond in JSON format:
{{
    "sentence": "Your generated sentence",
    "target_words": [
        {{"word": "word1", "phoneme": "target_phoneme1"}},
        {{"word": "word2", "phoneme": "target_phoneme2"}}
    ],
    "difficulty_notes": "Brief explanation of difficulty"
}}
"""


COACHING_PROMPT = """
You are a friendly speech therapy coach having a conversation with a student.

STUDENT INFO:
- Proficiency Level: {proficiency_level}
- Current Weak Phonemes: {weak_phonemes}
- Recent Progress: {recent_progress}

CONVERSATION CONTEXT:
{conversation_history}

Student's message: "{user_message}"

Provide a helpful, encouraging response. Keep it conversational and supportive.
If the student asks about pronunciation, refer to their known weak phonemes.
If they ask for practice suggestions, recommend exercises for their specific needs.

Respond naturally (not in JSON for this prompt).
"""


def format_phoneme_breakdown(phoneme_scores: list) -> str:
    """Format phoneme scores for prompt insertion."""
    lines = []
    for ps in phoneme_scores:
        status = "WEAK" if ps.get('is_weak') else "OK"
        lines.append(f"- {ps['phoneme']}: {ps['score']:.2f} [{status}]")
    return "\n".join(lines)


def build_feedback_prompt(
    sentence_text: str,
    overall_score: float,
    weak_phonemes: list,
    phoneme_scores: list
) -> str:
    """Build the pronunciation feedback prompt."""
    return PRONUNCIATION_FEEDBACK_PROMPT.format(
        sentence_text=sentence_text,
        overall_score=f"{overall_score:.2f}",
        weak_phonemes=", ".join(weak_phonemes) if weak_phonemes else "None",
        phoneme_breakdown=format_phoneme_breakdown(phoneme_scores)
    )


def build_sentence_prompt(
    target_phonemes: list,
    difficulty_level: str
) -> str:
    """Build the sentence generation prompt."""
    word_ranges = {
        'beginner': (5, 8),
        'intermediate': (8, 12),
        'advanced': (10, 15),
    }
    min_words, max_words = word_ranges.get(difficulty_level, (5, 10))
    
    return SENTENCE_GENERATION_PROMPT.format(
        target_phonemes=", ".join(target_phonemes),
        difficulty_level=difficulty_level,
        min_words=min_words,
        max_words=max_words
    )
