import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  console.log('Received file:', formData);
  const file = formData.get('ArchitectureDiagram');
  console.log('Received file:', file);

  // Function to handle the fetch call to FastAPI and return the result
  const callFastApi = async (formData: FormData) => {
    try {
      const response = await fetch("http://0.0.0.0:8002/generateawstemplate", {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        console.error(`FastAPI call failed with status: ${response.status}`);
        return { status: response.status, message: 'Failed' };
      }

      const data = await response.json();
      return { status: response.status, template: data.results[0].response, uuid:formData.get('UUID') };
    } catch (error) {
      console.error('Error in FastAPI call:', error);
      return { status: 500, message: 'Error in FastAPI call' };
    }
  };

  // Array of tasks to send to FastAPI, each for a different formData (could be multiple files or different data)
  const tasks = [callFastApi(formData)];

  // You can add more formData to the tasks array if you want to make multiple calls

  // Wait for all tasks (FastAPI calls) to finish
  const responses = await Promise.all(tasks);

  console.log("REEEEEE", responses)

  // You can now return the collected responses from the FastAPI calls
  return NextResponse.json({
    message: 'File forwarded to FastAPI',
    responses: responses,
  });
}
