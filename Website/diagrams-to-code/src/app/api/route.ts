import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    message: 'Site is up and running!',
  });
}
