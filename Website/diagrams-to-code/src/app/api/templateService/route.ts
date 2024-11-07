import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    // const requestBody = {file_name: "testing", all_types: await request.json()};
    // console.log(requestBody) 
    const requestBody = await request.json();
    const newRequestBody = {
        file_name: "testing",
        all_types: requestBody,
    };

    console.log("BANANAS", newRequestBody)

    try {
        // Forward the incoming POST request to the FastAPI backend (localhost:8000)
        const response = await fetch('http://0.0.0.0:8002/generateawstemplate', {
            method: 'POST',
            body: JSON.stringify(newRequestBody), // Forward the body (image) directly
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const result = await response.json();
        return NextResponse.json(result);
    } catch (error) {
        return NextResponse.json({ error: 'Error generating template' }, { status: 500 });
    }
}
