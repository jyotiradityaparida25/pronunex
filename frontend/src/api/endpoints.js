/**
 * Pronunex API Endpoints
 * Centralized route constants
 */

const API_VERSION = 'v1';
const BASE_PATH = `/api/${API_VERSION}`;

export const ENDPOINTS = {
    // Authentication
    AUTH: {
        LOGIN: `${BASE_PATH}/auth/login/`,
        SIGNUP: `${BASE_PATH}/auth/signup/`,
        LOGOUT: `${BASE_PATH}/auth/logout/`,
        REFRESH: `${BASE_PATH}/auth/token/refresh/`,
        PROFILE: `${BASE_PATH}/auth/profile/`,
        PASSWORD_RESET: `${BASE_PATH}/auth/password/reset/`,
        PASSWORD_RESET_CONFIRM: `${BASE_PATH}/auth/password/reset/confirm/`,
        PASSWORD_CHANGE: `${BASE_PATH}/auth/password/change/`,
    },

    // Library
    PHONEMES: {
        LIST: `${BASE_PATH}/phonemes/`,
        DETAIL: (id) => `${BASE_PATH}/phonemes/${id}/`,
    },
    SENTENCES: {
        LIST: `${BASE_PATH}/sentences/`,
        DETAIL: (id) => `${BASE_PATH}/sentences/${id}/`,
        AUDIO: (id) => `${BASE_PATH}/sentences/${id}/audio/`,
        RECOMMEND: `${BASE_PATH}/sentences/recommend/`,
        PREGENERATE: `${BASE_PATH}/sentences/pregenerate/`,
    },

    // Practice
    SESSIONS: {
        LIST: `${BASE_PATH}/sessions/`,
        CREATE: `${BASE_PATH}/sessions/`,
        DETAIL: (id) => `${BASE_PATH}/sessions/${id}/`,
        END: (id) => `${BASE_PATH}/sessions/${id}/end/`,
    },
    ATTEMPTS: {
        LIST: `${BASE_PATH}/attempts/`,
        DETAIL: (id) => `${BASE_PATH}/attempts/${id}/`,
    },
    ASSESS: `${BASE_PATH}/assess/`,

    // Analytics
    ANALYTICS: {
        PROGRESS: `${BASE_PATH}/analytics/progress/`,
        PHONEMES: `${BASE_PATH}/analytics/phonemes/`,
        HISTORY: `${BASE_PATH}/analytics/history/`,
    },
};

export default ENDPOINTS;
