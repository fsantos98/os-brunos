

export async function login(username: string, password: string) {
    const response = await fetch('http://ec2-18-246-27-158.us-west-2.compute.amazonaws.com:5111/authenticate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: username, password }),
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }

    return response;
}