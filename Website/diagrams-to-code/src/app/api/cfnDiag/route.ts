import fs from 'fs';
import path from 'path';
import { exec } from "child_process";
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    const formData = await request.formData();
    const yamlCode = formData.get('GeneratedTemplate') as string;
    const filePath = path.join(process.cwd(), 'cfndiag', 'output.yaml');
    const outputPath = path.join(process.cwd(), 'cfndiag', 'graph');

    try {
        fs.mkdirSync(path.dirname(filePath), { recursive: true });
  
        // Write the data to the file
        fs.writeFileSync(filePath, yamlCode, 'utf8');

        // Construct the command
        const command = `npx cfn-dia h -c -t ${filePath} -o ${outputPath}`;

        // Execute the command
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing command: ${stderr}`);
                return { status: 500, message: 'Command execution failed' };
            }
        });
  
        // Respond with success
        return NextResponse.json(
            { message: 'Graph generated successfully'},
            { status: 200 }
        );
    } catch (error) {
      console.error('Error generating graph:', error);
  
      // Send a failure response
      return NextResponse.json(
        { status: 500 }
      );
    }

    // You can now return the collected responses from the FastAPI calls
    // return NextResponse.json({
    //   message: 'File forwarded to FastAPI',
    //   responses: 200,
    // });
}