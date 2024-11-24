

export async function login(username: string, password: string) {
    const response = await fetch('localhost:5111/authenticate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: username, password }),
    });

    if (!response.ok) {
        return { ok: true }
    }

    return response;
}