# Pronunex API Reference

Base URL: `http://localhost:8000/api/v1/`

All authenticated endpoints require JWT token:
```
Authorization: Bearer <access_token>
```

---

## Authentication

### POST /auth/signup/
Register a new user.

**Request:**
```json
{
    "email": "user@example.com",
    "username": "user123",
    "full_name": "John Doe",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "native_language": "Hindi",
    "proficiency_level": "beginner"
}
```

**Response (201):**
```json
{
    "message": "Registration successful.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "user123",
        "full_name": "John Doe",
        "proficiency_level": "beginner"
    },
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

---

### POST /auth/login/
Authenticate user.

**Request:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
    "message": "Login successful.",
    "user": {...},
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

---

### POST /auth/logout/
**Auth Required**

Blacklist refresh token.

**Request:**
```json
{
    "refresh": "eyJ..."
}
```

---

### POST /auth/token/refresh/
Refresh access token.

**Request:**
```json
{
    "refresh": "eyJ..."
}
```

**Response (200):**
```json
{
    "access": "eyJ..."
}
```

---

### GET /auth/profile/
### PUT /auth/profile/
**Auth Required**

Get or update user profile.

---

### POST /auth/password/reset/
Request password reset email.

**Request:**
```json
{
    "email": "user@example.com"
}
```

---

### POST /auth/password/reset/confirm/
Confirm password reset.

**Request:**
```json
{
    "token": "reset_token_here",
    "new_password": "NewPass123!",
    "new_password_confirm": "NewPass123!"
}
```

---

## Phonemes

### GET /phonemes/
**Auth Required**

List all 44 English phonemes.

**Response (200):**
```json
[
    {
        "id": 1,
        "symbol": "/s/",
        "arpabet": "S",
        "ipa": "s",
        "type": "fricative",
        "example_word": "see",
        "description": "Voiceless alveolar fricative",
        "articulation_tip": "Tongue behind teeth, narrow air channel"
    }
]
```

---

### GET /phonemes/{id}/
**Auth Required**

Get phoneme details.

---

## Sentences

### GET /sentences/
**Auth Required**

List practice sentences.

**Query Parameters:**
- `difficulty_level`: beginner, intermediate, advanced
- `source`: curated, llm_generated
- `search`: text search

**Response (200):**
```json
{
    "count": 100,
    "results": [
        {
            "id": 1,
            "text": "She sells seashells by the seashore.",
            "difficulty_level": "intermediate",
            "audio_source": "/media/references/sentence_01.wav",
            "target_phonemes": ["SH", "S"],
            "source": "curated",
            "is_validated": true
        }
    ]
}
```

---

### GET /sentences/{id}/
**Auth Required**

Get sentence with precomputed phoneme data.

**Response (200):**
```json
{
    "id": 1,
    "text": "She sells seashells by the seashore.",
    "difficulty_level": "intermediate",
    "audio_source": "/media/references/sentence_01.wav",
    "phoneme_sequence": ["SH", "IY", "S", "EH", "L", "Z", ...],
    "alignment_map": [
        {"phoneme": "SH", "start": 0.0, "end": 0.15},
        {"phoneme": "IY", "start": 0.15, "end": 0.25}
    ],
    "target_phonemes": ["SH", "S"]
}
```

---

### GET /sentences/recommend/
**Auth Required**

Get personalized recommendations based on weak phonemes.

**Query Parameters:**
- `limit`: number of sentences (default: 5)
- `difficulty`: filter by difficulty

**Response (200):**
```json
{
    "recommendations": [...],
    "based_on_weak_phonemes": ["TH", "R", "L"]
}
```

---

## Assessment

### POST /assess/
**Auth Required**

Core pronunciation assessment endpoint.

**Request (multipart/form-data):**
```
sentence_id: 1
audio: <audio_file.wav>
```

**Response (200):**
```json
{
    "overall_score": 0.85,
    "fluency_score": 0.78,
    "phoneme_scores": [
        {"phoneme": "S", "score": 0.92, "word": "she", "is_weak": false},
        {"phoneme": "TH", "score": 0.65, "word": "the", "is_weak": true}
    ],
    "weak_phonemes": ["TH", "R"],
    "llm_feedback": {
        "summary": "Good overall pronunciation with minor issues on TH sounds.",
        "phoneme_tips": [
            {"phoneme": "TH", "tip": "Place tongue between teeth and blow gently."}
        ],
        "encouragement": "Keep practicing! You are improving.",
        "practice_focus": ["TH", "R"]
    },
    "processing_time_ms": 1245,
    "attempt_id": 42
}
```

---

## Sessions

### GET /sessions/
### POST /sessions/
**Auth Required**

List or create practice sessions.

---

### GET /sessions/{id}/
**Auth Required**

Get session with attempts.

---

### POST /sessions/{id}/end/
**Auth Required**

End session and calculate metrics.

---

## Attempts

### GET /attempts/
**Auth Required**

List user's attempts.

---

### GET /attempts/{id}/
**Auth Required**

Get attempt details with phoneme errors.

---

## Analytics

### GET /analytics/progress/
**Auth Required**

Get progress dashboard data.

**Query Parameters:**
- `days`: history range (default: 30)

**Response (200):**
```json
{
    "total_sessions": 25,
    "total_attempts": 150,
    "total_practice_minutes": 320.5,
    "overall_average_score": 0.78,
    "current_weak_phonemes": ["TH", "R"],
    "current_strong_phonemes": ["S", "M", "N"],
    "score_trend": "improving",
    "streak": {
        "current_streak": 5,
        "longest_streak": 12,
        "last_practice_date": "2026-01-09"
    },
    "recent_progress": [...],
    "phoneme_progress": [...]
}
```

---

### GET /analytics/phonemes/
**Auth Required**

Get per-phoneme analytics.

---

### GET /analytics/history/
**Auth Required**

Get daily progress history.

---

## Error Responses

**400 Bad Request:**
```json
{
    "error": "Invalid input.",
    "details": {...}
}
```

**401 Unauthorized:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**404 Not Found:**
```json
{
    "error": "Resource not found."
}
```

**500 Internal Server Error:**
```json
{
    "error": "Assessment failed.",
    "details": "..."
}
```
