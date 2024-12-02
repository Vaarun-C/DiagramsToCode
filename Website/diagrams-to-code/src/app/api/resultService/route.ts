import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const formData = await request.formData();

  // Function to handle the fetch call to FastAPI and return the result
  const callFastApi = async (formData: FormData) => {
    try {
      const response = await fetch("http://0.0.0.0:8002/result", {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        console.error(`FastAPI call failed with status: ${response.status}`);
        return { status: response.status, message: 'Failed' };
      }

      const data = await response.json();
      return { status: response.status, uuid:data.get('result') };
    } catch (error) {
      console.error('Error in FastAPI call:', error);
      return { status: 500, message: 'Error in FastAPI call' };
    }
  };

  const response = await callFastApi(formData);

  // You can now return the collected responses from the FastAPI calls
  return NextResponse.json({
    message: 'File forwarded to FastAPI',
    responses: response,
  });
}
