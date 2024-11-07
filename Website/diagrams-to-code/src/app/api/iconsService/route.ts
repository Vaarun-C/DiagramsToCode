import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    const formData = await request.formData();
    // console.log(requestBody)
    try {
        console.log("BEFORE SENDING TO FASTAPI")
        // Forward the incoming POST request to the FastAPI backend (localhost:8000)
        const response = await fetch('http://0.0.0.0:8000/getawsicons', {
            method: 'POST',
            body: formData, // Forward the body (image) directly
        });

        const result = await response.json();
        console.log("RESULTS!!!!")
        console.log(result)
        return NextResponse.json(result);
    } catch (error) {
        return NextResponse.json({ error: 'Error uploading image' }, { status: 500 });
    }
}
