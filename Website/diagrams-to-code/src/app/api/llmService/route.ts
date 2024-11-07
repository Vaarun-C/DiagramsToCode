import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {

    const requestBody = await request.json();

    console.log("FROM LLM", requestBody)
    try {
        // Forward the incoming POST request to the FastAPI backend (localhost:8000)
        const response = await fetch('http://0.0.0.0:8001/getllmsuggestion', {
            method: 'POST',
            body: JSON.stringify({"items": requestBody}), // Forward the body (image) directly
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const result = await response.json();
        return NextResponse.json(result);
    } catch (error) {
        return NextResponse.json({ error: 'Error getting LLM suggestions' }, { status: 500 });
    }
}
