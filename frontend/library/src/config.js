export const backendUrl = 'http://127.0.0.1:8000/api/';

// const backendUrl = import.meta.env.VITE_BACKEND_URL;

export async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('auth_token');

    const response = await fetch(`${backendUrl}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(token && {
                'Authorization': `token ${token}`
            }),
            ...options.headers,
        },
    });

    let data = null;

    // Some requests may return an empty response
    const contentType = response.headers.get('content-type');
    if (contentType?.includes('application/json')) {
        data = await response.json();
    }

    if (!response.ok) {
        throw new Error(data?.error || `Request failed with status ${response.status}`);
    }

    return data;
}