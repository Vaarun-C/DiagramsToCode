import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { NextRequest, NextResponse } from 'next/server';

type CommandResponse = [{ message: string }, { status: number }];

function execCommand(command: string): Promise<CommandResponse> {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing command: ${stderr}`);
        reject([{ message: 'Command execution failed' }, { status: 500 }]); // Reject with detailed error info
      } else {
        resolve([{ message: 'Graph generated successfully' }, { status: 200 }]);
      }
    });
  });
}

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const yamlCode = formData.get('GeneratedTemplate') as string;
  const uuid = formData.get('UUID') as string;
  const filePath = path.join(process.cwd(), 'public', 'output.yaml');
  const outputPath = path.join(process.cwd(), 'public', 'graph', uuid);
  const outputPathConcat = path.join('graph', uuid);

  // const indexPath = path.join(outputPath, 'index.html');
  // const dataJsPath = path.join(outputPath, 'data.js');
  // const iconsJsPath = path.join(outputPath, 'icons.js');

  try {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });

    // Write the data to the file
    fs.writeFileSync(filePath, yamlCode, 'utf8');

    // Construct the command
    const command = `npx cfn-dia h -c -t ${filePath} -o ${outputPath}`;

    // Execute the command
    return execCommand(command)
      .then((result: CommandResponse) => {
        try {
          // const htmlContent = fs.readFileSync(indexPath, 'utf8');
          // const dataContent = fs.readFileSync(dataJsPath, 'utf8');
          // const iconContent = fs.readFileSync(iconsJsPath, 'utf8');
          return NextResponse.json(
            {
              message: result[0],
              // htmlContent: htmlContent,
              // dataContent: dataContent,
              // iconContent: iconContent,
              uuid: uuid,
              outputPath: outputPathConcat,
            },
            result[1]
          );
        } catch (err) {
          console.log(err);
          return NextResponse.json(
            { message: 'failed to read file ' },
            { status: 500 }
          );
        }
        // return result;
      })
      .catch((result: CommandResponse) => {
        return NextResponse.json(result[0], result[1]);
      });

    // Respond with success
  } catch (error) {
    console.error('Error generating graph:', error);

    // Send a failure response
    return NextResponse.json({ status: 500 });
  }

  // You can now return the collected responses from the FastAPI calls
  // return NextResponse.json({
  //   message: 'File forwarded to FastAPI',
  //   responses: 200,
  // });
}
